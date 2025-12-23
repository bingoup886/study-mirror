import streamlit as st
import plotly.graph_objects as go
import json
from datetime import datetime
from typing import Dict, List, Optional
import re

# ============================================================================
# 页面配置
# ============================================================================
st.set_page_config(
    page_title="学习心理诊断工具",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# 全局样式
# ============================================================================
st.markdown("""
<style>
    /* 主容器 - 限制宽度为 80% */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    .block-container {
        max-width: 80% !important;
        margin: 0 auto !important;
    }

    /* ===== 对话气泡 - 优化版 ===== */
    .chat-bubble-ai {
        background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
        border-radius: 16px;
        padding: 14px 18px;
        margin: 10px 0;
        border: 1px solid rgba(63, 81, 181, 0.2);
        box-shadow: 0 2px 8px rgba(63, 81, 181, 0.1);
        font-size: 14px;
        line-height: 1.6;
        color: #333;
    }

    .chat-bubble-ai strong {
        color: #3f51b5;
        font-weight: 600;
    }

    .chat-bubble-user {
        background: linear-gradient(135deg, #c8e6c9 0%, #e8f5e9 100%);
        border-radius: 16px;
        padding: 14px 18px;
        margin: 10px 0;
        border: 1px solid rgba(76, 175, 80, 0.2);
        box-shadow: 0 2px 8px rgba(76, 175, 80, 0.1);
        font-size: 14px;
        line-height: 1.6;
        color: #333;
    }

    .chat-bubble-user strong {
        color: #4caf50;
        font-weight: 600;
    }

    /* 对话容器 */
    .chat-container {
        background: white;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        max-height: 400px;
        overflow-y: auto;
        border: 1px solid #e0e0e0;
    }

    /* 卡片样式 */
    .scenario-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .scenario-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }

    /* 语义透视窗 - 优化版 */
    .semantic-window {
        font-size: 13px;
        color: #555;
        margin-top: 12px;
        padding: 12px 14px;
        background: linear-gradient(135deg, #fff9e6 0%, #fffde7 100%);
        border-radius: 8px;
        border-left: 4px solid #fbc02d;
        border: 1px solid rgba(251, 192, 45, 0.2);
        box-shadow: 0 2px 6px rgba(251, 192, 45, 0.1);
        font-weight: 500;
    }

    /* 分值卡片 - 优化版 */
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 16px 12px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .score-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
    }

    .score-card-label {
        font-size: 12px;
        opacity: 0.95;
        margin-bottom: 6px;
        font-weight: 500;
        letter-spacing: 0.5px;
    }

    .score-card-value {
        font-size: 24px;
        font-weight: bold;
        letter-spacing: 1px;
    }

    /* 输入框优化 */
    .stTextArea textarea {
        border-radius: 12px !important;
        border: 2px solid #e0e0e0 !important;
        padding: 12px 14px !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
    }

    .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }

    /* 按钮优化 */
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        transition: all 0.3s ease !important;
        border: none !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
    }

    /* 标题优化 */
    h3, h4 {
        color: #333 !important;
        font-weight: 700 !important;
        margin-bottom: 12px !important;
    }

    /* 分隔线优化 */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, #ddd, transparent) !important;
        margin: 16px 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# Session State 初始化
# ============================================================================
def init_session_state():
    """初始化 Session State"""
    if "page" not in st.session_state:
        st.session_state.page = "home"  # home, dialogue

    if "scenario" not in st.session_state:
        st.session_state.scenario = None  # 当前场景

    if "dialogue_history" not in st.session_state:
        st.session_state.dialogue_history = []  # 对话历史

    if "scores_history" not in st.session_state:
        st.session_state.scores_history = []  # 分值历史

    if "current_scores" not in st.session_state:
        st.session_state.current_scores = {
            "归因风格": 50,
            "自我效能感": 50,
            "认知负荷": 50,
            "元认知": 50
        }

    if "round_count" not in st.session_state:
        st.session_state.round_count = 0

    if "semantic_log" not in st.session_state:
        st.session_state.semantic_log = ""

init_session_state()

# ============================================================================
# 场景定义
# ============================================================================
SCENARIOS = {
    "失意之径": {
        "title": "失意之径",
        "emoji": "😔",
        "description": "努力后却考砸了",
        "system_prompt": """你是一位温暖、专业的心理咨询师。学生刚经历了一次考试失利，尽管他们付出了努力。
你的任务是通过深度对话，理解他们的心理状态，并评估以下四个维度：
1. 归因风格：他们如何解释失败（内部/外部、稳定/不稳定、全局/特定）
2. 自我效能感：他们对自己能力的信心程度
3. 认知负荷：当前的心理压力和信息处理能力
4. 元认知：他们对自己学习过程的认知和反思能力

请用温暖、鼓励的语气进行对话，每次回复都要包含一个澄清式追问。"""
    },
    "深谷挑战": {
        "title": "深谷挑战",
        "emoji": "🌙",
        "description": "深夜遇难题卡住",
        "system_prompt": """你是一位温暖、专业的心理咨询师。学生在深夜做题时遇到了难题，感到困顿和无力。
你的任务是通过深度对话，理解他们的心理状态，并评估以下四个维度：
1. 归因风格：他们如何看待这个难题（能力问题还是方法问题）
2. 自我效能感：他们对解决问题的信心
3. 认知负荷：深夜疲劳状态下的心理压力
4. 元认知：他们的学习策略和自我调节能力

请用温暖、鼓励的语气进行对话，帮助他们重新获得信心。"""
    },
    "意志荒漠": {
        "title": "意志荒漠",
        "emoji": "📱",
        "description": "想放弃去刷视频",
        "system_prompt": """你是一位温暖、专业的心理咨询师。学生感到学习疲惫，想要放弃学习去刷视频。
你的任务是通过深度对话，理解他们的心理状态，并评估以下四个维度：
1. 归因风格：他们如何看待学习的意义和价值
2. 自我效能感：他们对自己坚持能力的信心
3. 认知负荷：当前的心理压力和疲劳程度
4. 元认知：他们对自己学习动力的认知

请用温暖、鼓励的语气进行对话，帮助他们找到学习的内在动力。"""
    }
}

# ============================================================================
# AI 模拟函数（用于演示，后续替换为真实 API）
# ============================================================================
def simulate_ai_response(user_input: str, scenario: str, round_num: int) -> Dict:
    """
    模拟 AI 返回结构化数据
    实际应用中，这里会调用九章/GPT-4o API
    """

    # 模拟 AI 的对话回复
    responses = {
        "失意之径": [
            "我能感受到你现在的失落。考试没有达到预期，这确实让人难受。能告诉我，你在准备这次考试时，花了多少时间复习？",
            "感谢你的分享。我注意到你提到了'尽力了'。那么，你觉得这次失利主要是因为什么呢？是知识掌握不够，还是考试时的状态问题？",
            "我理解。这种感受很常见。现在让我问你一个不同的角度：如果下次考试前，你能改变一件事，你会改变什么？",
            "很好的思考。你的这个想法表明你已经在反思和成长。最后一个问题：你觉得自己有能力在下次考试中做得更好吗？"
        ],
        "深谷挑战": [
            "深夜做题遇到难题，这种感受我理解。能描述一下这道题的难点在哪里吗？",
            "感谢分享。那么，当你遇到这样的难题时，你通常会怎么处理？",
            "我看到了。你的这个方法很有思考。那么，你觉得自己有能力解决这类问题吗？",
            "很好。你的坚持精神值得肯定。现在，你觉得继续做题还是先休息会更有帮助？"
        ],
        "意志荒漠": [
            "我能感受到你的疲惫。学习到一定程度确实会感到乏力。能告诉我，你现在最想放弃的原因是什么？",
            "感谢你的坦诚。那么，你觉得学习对你来说意味着什么呢？",
            "我理解。那么，如果你坚持下去，你期待会得到什么？",
            "很好的思考。你的这个想法表明你内心还是有目标的。你觉得自己有能力坚持下去吗？"
        ]
    }

    # 模拟 AI 的评分逻辑（0-100 分）
    base_scores = {
        "归因风格": 50,
        "自我效能感": 50,
        "认知负荷": 50,
        "元认知": 50
    }

    # 根据用户输入长度和轮数调整分值
    input_length = len(user_input)

    if scenario == "失意之径":
        base_scores["归因风格"] += 8 * round_num
        base_scores["自我效能感"] += 6 * round_num
        base_scores["认知负荷"] -= 4 * round_num
    elif scenario == "深谷挑战":
        base_scores["元认知"] += 10 * round_num
        base_scores["自我效能感"] += 8 * round_num
    else:  # 意志荒漠
        base_scores["自我效能感"] += 12 * round_num
        base_scores["认知负荷"] -= 6 * round_num

    # 确保分值在 0-100 之间
    for key in base_scores:
        base_scores[key] = max(0, min(100, base_scores[key]))

    # 获取对应的对话
    scenario_responses = responses.get(scenario, responses["失意之径"])
    dialogue = scenario_responses[min(round_num - 1, len(scenario_responses) - 1)]

    # 模拟语义透视
    semantic_keywords = {
        "失意之径": ["能力内化归因", "自我反思能力", "恢复性思维"],
        "深谷挑战": ["问题解决策略", "坚持力评估", "疲劳管理"],
        "意志荒漠": ["内在动力激发", "目标清晰度", "自我约束能力"]
    }

    keywords = semantic_keywords.get(scenario, [])
    semantic_log = f"捕捉到：{', '.join(keywords[:2])}"

    return {
        "dialogue": dialogue,
        "scores": base_scores,
        "is_finished": round_num >= 4,
        "analysis_log": semantic_log
    }

# ============================================================================
# JSON 解析器
# ============================================================================
def parse_ai_response(response: Dict) -> tuple[str, Dict, bool, str]:
    """
    解析 AI 返回的 JSON 结构
    返回：(对话文本, 分值字典, 是否完成, 语义日志)
    """
    try:
        dialogue = response.get("dialogue", "")
        scores = response.get("scores", {})
        is_finished = response.get("is_finished", False)
        analysis_log = response.get("analysis_log", "")

        # 验证分值范围（0-100）
        for key in scores:
            scores[key] = max(0, min(100, int(float(scores[key]))))

        return dialogue, scores, is_finished, analysis_log
    except Exception as e:
        st.error(f"JSON 解析错误: {str(e)}")
        return "", {}, False, ""

# ============================================================================
# 雷达图生成函数
# ============================================================================
def create_radar_chart(scores: Dict) -> go.Figure:
    """
    创建动态雷达图（0-100 分值）
    """
    categories = list(scores.keys())
    values = list(scores.values())

    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(102, 126, 234, 0.3)',  # 半透明紫蓝色
        line=dict(color='rgba(102, 126, 234, 0.8)', width=2.5),
        marker=dict(size=8, color='#667eea'),
        name='当前维度'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10),
                gridcolor='rgba(200, 200, 200, 0.3)',
                ticksuffix=' 分'
            ),
            angularaxis=dict(
                tickfont=dict(size=11),
                gridcolor='rgba(200, 200, 200, 0.3)'
            ),
            bgcolor='rgba(240, 240, 240, 0.5)'
        ),
        showlegend=False,
        height=380,
        margin=dict(l=80, r=80, t=80, b=80),
        font=dict(family="Microsoft YaHei, SimHei, sans-serif", size=12),
        paper_bgcolor='rgba(255, 255, 255, 0.8)',
        plot_bgcolor='rgba(240, 240, 240, 0.3)'
    )

    return fig

# ============================================================================
# 首页：三扇门场景选择
# ============================================================================
def render_home_page():
    """渲染首页 - 三扇门"""
    st.markdown("""
    <div style='text-align: center; padding: 40px 0;'>
        <h1 style='font-size: 48px; margin-bottom: 10px;'>🧠 学习心理诊断工具</h1>
        <p style='font-size: 18px; color: #666;'>通过深度对话，发现你的学习心理密码</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div style='text-align: center; margin: 30px 0;'>
        <h3>选择你的场景，开启诊断之旅</h3>
    </div>
    """, unsafe_allow_html=True)

    # 三列布局
    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown(f"""
        <div class='scenario-card'>
            <div style='font-size: 48px; text-align: center; margin-bottom: 16px;'>
                {SCENARIOS["失意之径"]["emoji"]}
            </div>
            <h3 style='text-align: center; margin: 0;'>{SCENARIOS["失意之径"]["title"]}</h3>
            <p style='text-align: center; color: #666; margin: 8px 0;'>
                {SCENARIOS["失意之径"]["description"]}
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("进入失意之径", key="btn_scenario_1", width="stretch"):
            st.session_state.page = "dialogue"
            st.session_state.scenario = "失意之径"
            st.session_state.dialogue_history = []
            st.session_state.scores_history = []
            st.session_state.round_count = 0
            st.rerun()

    with col2:
        st.markdown(f"""
        <div class='scenario-card'>
            <div style='font-size: 48px; text-align: center; margin-bottom: 16px;'>
                {SCENARIOS["深谷挑战"]["emoji"]}
            </div>
            <h3 style='text-align: center; margin: 0;'>{SCENARIOS["深谷挑战"]["title"]}</h3>
            <p style='text-align: center; color: #666; margin: 8px 0;'>
                {SCENARIOS["深谷挑战"]["description"]}
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("进入深谷挑战", key="btn_scenario_2", width="stretch"):
            st.session_state.page = "dialogue"
            st.session_state.scenario = "深谷挑战"
            st.session_state.dialogue_history = []
            st.session_state.scores_history = []
            st.session_state.round_count = 0
            st.rerun()

    with col3:
        st.markdown(f"""
        <div class='scenario-card'>
            <div style='font-size: 48px; text-align: center; margin-bottom: 16px;'>
                {SCENARIOS["意志荒漠"]["emoji"]}
            </div>
            <h3 style='text-align: center; margin: 0;'>{SCENARIOS["意志荒漠"]["title"]}</h3>
            <p style='text-align: center; color: #666; margin: 8px 0;'>
                {SCENARIOS["意志荒漠"]["description"]}
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("进入意志荒漠", key="btn_scenario_3", width="stretch"):
            st.session_state.page = "dialogue"
            st.session_state.scenario = "意志荒漠"
            st.session_state.dialogue_history = []
            st.session_state.scores_history = []
            st.session_state.round_count = 0
            st.rerun()

# ============================================================================
# 对话页面：左图右谈
# ============================================================================
def render_dialogue_page():
    """渲染对话页面 - 左图右谈"""

    # 顶部导航栏
    nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
    with nav_col1:
        if st.button("← 返回首页", width="stretch"):
            st.session_state.page = "home"
            st.rerun()

    with nav_col2:
        st.markdown(f"""
        <div style='text-align: center; padding: 8px 0;'>
            <h2 style='margin: 0; color: #333;'>{SCENARIOS[st.session_state.scenario]['emoji']} {st.session_state.scenario}</h2>
        </div>
        """, unsafe_allow_html=True)

    with nav_col3:
        progress = min(st.session_state.round_count / 4, 1.0)
        st.markdown(f"""
        <div style='text-align: right; padding: 8px 0;'>
            <span style='color: #667eea; font-weight: 600; font-size: 14px;'>
                进度: {st.session_state.round_count}/4 轮
            </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 左右两列布局
    col_left, col_right = st.columns([1, 1.2], gap="large")

    # ========== 左侧：雷达图 + 语义透视窗 ==========
    with col_left:
        st.markdown("#### 📊 学习心理维度")

        # 创建并显示雷达图
        fig = create_radar_chart(st.session_state.current_scores)
        st.plotly_chart(fig, width="stretch", key=f"radar_{st.session_state.round_count}")

        # 语义透视窗
        if st.session_state.semantic_log:
            st.markdown(f"""
            <div class='semantic-window'>
                🔍 {st.session_state.semantic_log}
            </div>
            """, unsafe_allow_html=True)

        # 分值显示 - 两行紧凑布局
        st.markdown("#### 📈 维度分值")

        # 第一行：前两个维度
        score_cols1 = st.columns(2, gap="small")
        dimensions = list(st.session_state.current_scores.keys())

        with score_cols1[0]:
            st.markdown(f"""
            <div class='score-card'>
                <div class='score-card-label'>{dimensions[0]}</div>
                <div class='score-card-value'>{st.session_state.current_scores[dimensions[0]]}</div>
            </div>
            """, unsafe_allow_html=True)

        with score_cols1[1]:
            st.markdown(f"""
            <div class='score-card'>
                <div class='score-card-label'>{dimensions[1]}</div>
                <div class='score-card-value'>{st.session_state.current_scores[dimensions[1]]}</div>
            </div>
            """, unsafe_allow_html=True)

        # 第二行：后两个维度
        score_cols2 = st.columns(2, gap="small")

        with score_cols2[0]:
            st.markdown(f"""
            <div class='score-card'>
                <div class='score-card-label'>{dimensions[2]}</div>
                <div class='score-card-value'>{st.session_state.current_scores[dimensions[2]]}</div>
            </div>
            """, unsafe_allow_html=True)

        with score_cols2[1]:
            st.markdown(f"""
            <div class='score-card'>
                <div class='score-card-label'>{dimensions[3]}</div>
                <div class='score-card-value'>{st.session_state.current_scores[dimensions[3]]}</div>
            </div>
            """, unsafe_allow_html=True)

    # ========== 右侧：对话框 ==========
    with col_right:
        st.markdown("#### 💬 深度对话")

        # 对话历史显示 - 使用容器
        st.markdown("""
        <div class='chat-container'>
        """, unsafe_allow_html=True)

        for msg in st.session_state.dialogue_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class='chat-bubble-user'>
                    <strong>👤 你：</strong> {msg["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='chat-bubble-ai'>
                    <strong>🧠 心理咨询师：</strong> {msg["content"]}
                </div>
                """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # 用户输入
        st.markdown("---")
        user_input = st.text_area(
            "你的回答：",
            placeholder="请详细描述你的想法和感受...",
            height=90,
            label_visibility="collapsed"
        )

        # 提交按钮
        col_btn1, col_btn2 = st.columns([1.2, 1])

        with col_btn1:
            if st.button("📤 提交回答", width="stretch"):
                if not user_input.strip():
                    st.warning("⚠️ 请输入你的回答")
                elif len(user_input.strip()) < 5:
                    # 智能追问逻辑
                    st.info("💡 你的回答有点简短，能否详细一些呢？")
                else:
                    # 添加用户消息
                    st.session_state.dialogue_history.append({
                        "role": "user",
                        "content": user_input
                    })

                    # 调用 AI（模拟）
                    st.session_state.round_count += 1
                    ai_response = simulate_ai_response(
                        user_input,
                        st.session_state.scenario,
                        st.session_state.round_count
                    )

                    # 解析 AI 响应
                    dialogue, scores, is_finished, semantic_log = parse_ai_response(ai_response)

                    # 更新状态
                    st.session_state.dialogue_history.append({
                        "role": "assistant",
                        "content": dialogue
                    })
                    st.session_state.current_scores = scores
                    st.session_state.scores_history.append(scores)
                    st.session_state.semantic_log = semantic_log

                    st.rerun()

        with col_btn2:
            if st.button("🏠 返回", width="stretch"):
                st.session_state.page = "home"
                st.rerun()

        # 生成报告按钮
        if st.session_state.round_count >= 4 or (st.session_state.dialogue_history and st.session_state.dialogue_history[-1].get("is_finished")):
            st.markdown("---")
            if st.button("📋 生成深度透视报告", width="stretch", type="primary"):
                st.session_state.page = "report"
                st.rerun()

# ============================================================================
# 报告页面（占位符）
# ============================================================================
def render_report_page():
    """渲染报告页面"""
    st.markdown("### 📋 深度透视报告")
    st.info("报告生成功能开发中...")

    if st.button("← 返回对话"):
        st.session_state.page = "dialogue"
        st.rerun()

# ============================================================================
# 主程序入口
# ============================================================================
def main():
    """主程序"""
    if st.session_state.page == "home":
        render_home_page()
    elif st.session_state.page == "dialogue":
        render_dialogue_page()
    elif st.session_state.page == "report":
        render_report_page()

if __name__ == "__main__":
    main()

