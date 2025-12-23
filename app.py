import streamlit as st
import plotly.graph_objects as go
import json
from datetime import datetime
from typing import Dict, List, Optional
import re
import requests

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

    /* ===== 对话气泡 - 微信风格 ===== */

    /* 对话消息行 */
    .chat-message {
        display: flex;
        margin: 12px 0;
        align-items: flex-end;
        gap: 8px;
    }

    /* AI 消息（左对齐） */
    .chat-message-ai {
        justify-content: flex-start;
    }

    /* 用户消息（右对齐） */
    .chat-message-user {
        justify-content: flex-end;
    }

    /* 头像 */
    .chat-avatar {
        font-size: 24px;
        min-width: 32px;
        text-align: center;
    }

    /* 消息内容容器 */
    .chat-content {
        max-width: 70%;
        display: flex;
        flex-direction: column;
    }

    /* AI 消息内容 */
    .chat-content-ai {
        align-items: flex-start;
    }

    /* 用户消息内容 */
    .chat-content-user {
        align-items: flex-end;
    }

    /* 气泡样式 */
    .chat-bubble {
        border-radius: 16px;
        padding: 12px 16px;
        word-wrap: break-word;
        font-size: 14px;
        line-height: 1.6;
        color: #333;
    }

    /* AI 气泡 */
    .chat-bubble-ai {
        background: #f0f0f0;
        border-radius: 16px 16px 16px 4px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    }

    /* 用户气泡 */
    .chat-bubble-user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px 16px 4px 16px;
        color: white;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }

    /* 用户气泡中的文字 */
    .chat-bubble-user strong {
        color: white;
        font-weight: 600;
        display: none;
    }

    /* AI 气泡中的文字 */
    .chat-bubble-ai strong {
        color: #3f51b5;
        font-weight: 600;
        display: none;
    }

    /* 时间戳 */
    .chat-timestamp {
        font-size: 12px;
        color: #999;
        margin-top: 4px;
        text-align: center;
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

    /* 首页场景卡片 */
    .home-scenario-card {
        background: white;
        border-radius: 12px;
        padding: 32px 24px;
        border: 1px solid #f0f0f0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
        cursor: pointer;
        text-align: center;
    }

    .home-scenario-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        border-color: #e8e8e8;
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

    if "initialized" not in st.session_state:
        st.session_state.initialized = False

    if "question_count" not in st.session_state:
        st.session_state.question_count = 0

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
# 硅基流动 API 配置
# ============================================================================
SILICONFLOW_API_KEY = "sk-kvkkpoisfmvkumunkdfnlungbsenuzcvgxpreqasamasefcp"
SILICONFLOW_API_URL = "https://api.siliconflow.cn/v1/chat/completions"
MODEL_NAME = "deepseek-ai/DeepSeek-V3"

# ============================================================================
# 调用硅基流动 API
# ============================================================================
def call_deepseek_api(prompt: str, max_retries: int = 2) -> str:
    """
    调用硅基流动的 DeepSeek-V3 模型，参考官方 API 调用示例
    """
    import time

    for attempt in range(max_retries):
        try:
            headers = {
                "Authorization": f"Bearer {SILICONFLOW_API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": MODEL_NAME,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "stream": False,
                "max_tokens": 1000,
                "temperature": 0.7,
                "top_p": 0.7,
                "top_k": 50,
                "frequency_penalty": 0.5,
                "n": 1,
                "response_format": {"type": "text"}
            }

            response = requests.post(SILICONFLOW_API_URL, json=payload, headers=headers, timeout=30)
            response.raise_for_status()

            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                return ""

        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            else:
                st.warning("⚠️ API 请求超时，使用预设回复")
                return ""
        except requests.exceptions.ConnectionError:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            else:
                st.warning("⚠️ 网络连接失败，使用预设回复")
                return ""
        except requests.exceptions.HTTPError as e:
            error_code = e.response.status_code

            if error_code == 503:
                if attempt < max_retries - 1:
                    st.info("⏳ API 服务暂时不可用，正在重试...")
                    time.sleep(3)
                    continue
                else:
                    st.warning("⚠️ API 服务暂时不可用，使用预设回复")
                    return ""
            elif error_code == 401:
                st.error("❌ API 认证失败：请检查 API Key 是否正确")
                return ""
            elif error_code == 429:
                if attempt < max_retries - 1:
                    st.info("⏳ API 请求过于频繁，正在重试...")
                    time.sleep(5)
                    continue
                else:
                    st.warning("⚠️ API 请求过于频繁，使用预设回复")
                    return ""
            else:
                st.warning(f"⚠️ API 错误 (HTTP {error_code})，使用预设回复")
                return ""
        except Exception as e:
            st.warning(f"⚠️ API 调用异常，使用预设回复")
            return ""

    return ""

# ============================================================================
# AI 响应函数（使用真实 API）
# ============================================================================
def simulate_ai_response(user_input: str, scenario: str, round_num: int, is_init: bool = False) -> Dict:
    """
    模拟 AI 返回结构化数据
    实际应用中，这里会调用九章/GPT-4o API

    参数：
    - user_input: 用户输入
    - scenario: 场景名称
    - round_num: 轮数
    - is_init: 是否是初始化（生成欢迎语和第一个问题）
    """

    # 欢迎语
    welcome_messages = {
        "失意之径": "你好，我是你的心理咨询师。我看到你最近经历了一次考试失利，我能理解这种失望的感受。让我们一起来探索一下你的想法和感受。",
        "深谷挑战": "你好，我是你的心理咨询师。我看到你在深夜做题时遇到了困难，这确实是一个挑战。让我们一起来理解你现在的状态。",
        "意志荒漠": "你好，我是你的心理咨询师。我看到你现在感到疲惫，想要放弃学习。这是很多学生都会经历的感受。让我们一起来探索一下。"
    }

    # 模拟 AI 的对话回复（3 个问题）
    responses = {
        "失意之径": [
            "我能感受到你现在的失落。考试没有达到预期，这确实让人难受。能告诉我，你在准备这次考试时，花了多少时间复习？",
            "感谢你的分享。我注意到你提到了这些。那么，你觉得这次失利主要是因为什么呢？是知识掌握不够，还是考试时的状态问题？",
            "我理解。这种感受很常见。现在让我问你一个不同的角度：如果下次考试前，你能改变一件事，你会改变什么？"
        ],
        "深谷挑战": [
            "深夜做题遇到难题，这种感受我理解。能描述一下这道题的难点在哪里吗？",
            "感谢分享。那么，当你遇到这样的难题时，你通常会怎么处理？",
            "我看到了。你的这个方法很有思考。那么，你觉得自己有能力解决这类问题吗？"
        ],
        "意志荒漠": [
            "我能感受到你的疲惫。学习到一定程度确实会感到乏力。能告诉我，你现在最想放弃的原因是什么？",
            "感谢你的坦诚。那么，你觉得学习对你来说意味着什么呢？",
            "我理解。那么，如果你坚持下去，你期待会得到什么？"
        ]
    }

    # 分析总结（3 个问题后）
    analysis_summary = {
        "失意之径": "通过我们的对话，我看到了你的反思能力和成长潜力。你对失败的理解正在逐步深化，这是非常积极的信号。",
        "深谷挑战": "你展现出了很强的问题解决意识和坚持精神。即使在困难面前，你也在思考如何应对，这说明你的元认知能力很强。",
        "意志荒漠": "你的对话让我看到，你内心其实还是有目标和动力的。疲惫是暂时的，而你的坚持能力是真实存在的。"
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

    # 如果是初始化，返回欢迎语 + 第一个问题
    if is_init:
        welcome = welcome_messages.get(scenario, "你好，我是你的心理咨询师。")
        # 使用 API 生成第一个问题
        prompt = f"你是一位专业的心理咨询师。用户选择了'{scenario}'场景。请生成一个开放式的心理咨询问题，帮助用户探索他们的心理状态。问题应该简洁、同情、专业。只返回问题本身，不要有其他内容。"
        first_question = call_deepseek_api(prompt)
        if not first_question:
            first_question = scenario_responses[0]
        dialogue = f"{welcome}\n\n{first_question}"
        is_finished = False
        question_count = 1
    else:
        # 3 个问题完成后，开始分析
        if round_num >= 3:
            is_finished = True
            # 使用 API 生成分析总结
            prompt = f"用户在'{scenario}'场景中完成了3轮心理咨询对话。用户的回答显示了他们的心理状态。请生成一个专业的、鼓励性的分析总结（2-3句话），评价用户的心理状态和成长潜力。"
            summary = call_deepseek_api(prompt)
            if not summary:
                summary = analysis_summary.get(scenario, "")
            dialogue = f"{summary}\n\n现在让我为你生成详细的心理诊断报告..."
        else:
            is_finished = False
            # 使用 API 生成下一个问题
            prompt = f"你是一位专业的心理咨询师。用户在'{scenario}'场景中。用户之前的回答是：'{user_input}'。这是第{round_num + 1}个问题。请生成一个后续的心理咨询问题，深入探索用户的心理状态。问题应该基于用户的回答，更深入地了解他们的想法和感受。只返回问题本身，不要有其他内容。"
            dialogue = call_deepseek_api(prompt)
            if not dialogue:
                # 如果 API 调用失败，使用预设的问题
                question_idx = min(round_num, len(scenario_responses) - 1)
                dialogue = scenario_responses[question_idx]

        question_count = round_num + 1

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
        "is_finished": is_finished,
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
    """渲染首页 - 按照设计图一比一实现"""

    # 顶部导航栏
    nav_col1, nav_col2, nav_col3 = st.columns([1, 3, 1])
    with nav_col1:
        st.markdown("""
        <div style='font-size: 24px; font-weight: bold; color: #ff6b6b;'>❤️</div>
        """, unsafe_allow_html=True)

    with nav_col2:
        st.markdown("""
        <div style='text-align: left;'>
            <div style='font-size: 18px; font-weight: bold; color: #333;'>心理透镜</div>
            <div style='font-size: 12px; color: #999;'>Psyche Lens</div>
        </div>
        """, unsafe_allow_html=True)

    with nav_col3:
        st.markdown("""
        <div style='text-align: right; font-size: 14px; color: #666;'>
            欢迎，ding &nbsp; <span style='color: #ff6b6b;'>➜</span> &nbsp; 登出
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 主标题
    st.markdown("""
    <div style='text-align: center; padding: 40px 0 20px 0;'>
        <h1 style='font-size: 42px; margin: 0; color: #333;'>
            选择你的<span style='color: #ff6b6b;'>心境场景</span>
        </h1>
    </div>
    """, unsafe_allow_html=True)

    # 副标题
    st.markdown("""
    <div style='text-align: center; margin-bottom: 50px;'>
        <p style='font-size: 16px; color: #666; margin: 0;'>
            通过 3-5 轮温暖对话，我们将深入理解你的学习心理状态
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 三列布局 - 场景卡片
    col1, col2, col3 = st.columns(3, gap="large")

    # 场景 1：失意之径
    with col1:
        st.markdown("""
        <div class='home-scenario-card' onclick="document.querySelector('[data-scenario=1]').click();" style='cursor: pointer;'>
            <div style='font-size: 56px; text-align: center; margin-bottom: 16px;'>😔</div>
            <h3 style='text-align: center; margin: 0 0 6px 0; font-size: 18px; color: #333; font-weight: 600;'>失意之径</h3>
            <p style='text-align: center; margin: 0 0 12px 0; font-size: 13px; color: #999;'>努力后却考砸了</p>
            <p style='text-align: center; margin: 0 0 20px 0; font-size: 12px; color: #aaa; line-height: 1.5;'>
                当付出努力后却未获得预期成果，内心的失落与困惑油然而生...
            </p>
            <div style='text-align: center;'>
                <span style='color: #667eea; font-size: 13px; font-weight: 500;'>进入此场景 →</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("进入失意之径", key="btn_scenario_1", width="stretch", use_container_width=True):
            st.session_state.page = "dialogue"
            st.session_state.scenario = "失意之径"
            st.session_state.dialogue_history = []
            st.session_state.scores_history = []
            st.session_state.round_count = 0
            st.session_state.question_count = 0
            st.session_state.initialized = False
            st.rerun()

    # 场景 2：深谷挑战
    with col2:
        st.markdown("""
        <div class='home-scenario-card' onclick="document.querySelector('[data-scenario=2]').click();" style='cursor: pointer;'>
            <div style='font-size: 56px; text-align: center; margin-bottom: 16px;'>🤔</div>
            <h3 style='text-align: center; margin: 0 0 6px 0; font-size: 18px; color: #333; font-weight: 600;'>深谷挑战</h3>
            <p style='text-align: center; margin: 0 0 12px 0; font-size: 13px; color: #999;'>深夜遇难题卡住</p>
            <p style='text-align: center; margin: 0 0 20px 0; font-size: 12px; color: #aaa; line-height: 1.5;'>
                面对困难题目，感到无助和困顿，思维陷入僵局...
            </p>
            <div style='text-align: center;'>
                <span style='color: #667eea; font-size: 13px; font-weight: 500;'>进入此场景 →</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("进入深谷挑战", key="btn_scenario_2", width="stretch", use_container_width=True):
            st.session_state.page = "dialogue"
            st.session_state.scenario = "深谷挑战"
            st.session_state.dialogue_history = []
            st.session_state.scores_history = []
            st.session_state.round_count = 0
            st.session_state.question_count = 0
            st.session_state.initialized = False
            st.rerun()

    # 场景 3：意志荒漠
    with col3:
        st.markdown("""
        <div class='home-scenario-card' onclick="document.querySelector('[data-scenario=3]').click();" style='cursor: pointer;'>
            <div style='font-size: 56px; text-align: center; margin-bottom: 16px;'>📱</div>
            <h3 style='text-align: center; margin: 0 0 6px 0; font-size: 18px; color: #333; font-weight: 600;'>意志荒漠</h3>
            <p style='text-align: center; margin: 0 0 12px 0; font-size: 13px; color: #999;'>想放弃去刷视频</p>
            <p style='text-align: center; margin: 0 0 20px 0; font-size: 12px; color: #aaa; line-height: 1.5;'>
                学习动力消退，诱惑不断增加，坚持变得困难...
            </p>
            <div style='text-align: center;'>
                <span style='color: #667eea; font-size: 13px; font-weight: 500;'>进入此场景 →</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("进入意志荒漠", key="btn_scenario_3", width="stretch", use_container_width=True):
            st.session_state.page = "dialogue"
            st.session_state.scenario = "意志荒漠"
            st.session_state.dialogue_history = []
            st.session_state.scores_history = []
            st.session_state.round_count = 0
            st.session_state.question_count = 0
            st.session_state.initialized = False
            st.rerun()

    # 底部 - 四个核心维度（缩放到 70%，更窄更高）
    st.markdown("""<div style='margin-top: 60px; padding: 40px 48px; background: #fdf0f5; border-radius: 12px; text-align: center; transform: scale(0.7); transform-origin: top center; margin-bottom: -30px; width: 85%; margin-left: auto; margin-right: auto;'><h2 style='font-size: 20px; color: #333; margin: 0 0 36px 0;'>我们将评估<span style='color: #ff6b6b;'>四个核心维度</span></h2><div style='display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px;'><div style='background: white; padding: 28px 20px; border-radius: 8px; text-align: center;'><div style='font-size: 16px; font-weight: 600; color: #ff6b6b; margin-bottom: 12px;'>归因风格</div><div style='font-size: 14px; color: #666; line-height: 1.5;'>如何解释失败</div></div><div style='background: white; padding: 28px 20px; border-radius: 8px; text-align: center;'><div style='font-size: 16px; font-weight: 600; color: #52c41a; margin-bottom: 12px;'>自我效能感</div><div style='font-size: 14px; color: #666; line-height: 1.5;'>对自己的信心</div></div><div style='background: white; padding: 28px 20px; border-radius: 8px; text-align: center;'><div style='font-size: 16px; font-weight: 600; color: #faad14; margin-bottom: 12px;'>认知负荷</div><div style='font-size: 14px; color: #666; line-height: 1.5;'>心理压力程度</div></div><div style='background: white; padding: 28px 20px; border-radius: 8px; text-align: center;'><div style='font-size: 16px; font-weight: 600; color: #1890ff; margin-bottom: 12px;'>元认知</div><div style='font-size: 14px; color: #666; line-height: 1.5;'>学习意识能力</div></div></div></div>""", unsafe_allow_html=True)

# ============================================================================
# 对话页面：左图右谈
# ============================================================================
def render_dialogue_page():
    """渲染对话页面 - 左图右谈"""

    # ========== 初始化：发送欢迎语和第一个问题 ==========
    if not st.session_state.initialized:
        ai_response = simulate_ai_response(
            user_input="",
            scenario=st.session_state.scenario,
            round_num=0,
            is_init=True
        )

        dialogue, scores, is_finished, semantic_log = parse_ai_response(ai_response)

        # 添加 AI 的欢迎语和第一个问题
        st.session_state.dialogue_history.append({
            "role": "assistant",
            "content": dialogue
        })

        # 更新状态
        st.session_state.current_scores = scores
        st.session_state.semantic_log = semantic_log
        st.session_state.initialized = True
        st.session_state.question_count = 1

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

        # 对话历史显示 - 微信风格
        st.markdown("""
        <div class='chat-container'>
        """, unsafe_allow_html=True)

        for msg in st.session_state.dialogue_history:
            if msg["role"] == "user":
                # 用户消息（右对齐）
                st.markdown(f"""
                <div class='chat-message chat-message-user'>
                    <div class='chat-content chat-content-user'>
                        <div class='chat-bubble chat-bubble-user'>
                            {msg["content"]}
                        </div>
                    </div>
                    <div class='chat-avatar'>👤</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # AI 消息（左对齐）
                st.markdown(f"""
                <div class='chat-message chat-message-ai'>
                    <div class='chat-avatar'>🧠</div>
                    <div class='chat-content chat-content-ai'>
                        <div class='chat-bubble chat-bubble-ai'>
                            {msg["content"]}
                        </div>
                    </div>
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
                        st.session_state.round_count,
                        is_init=False
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

                    # 如果完成 3 个问题，标记为完成
                    if st.session_state.round_count >= 3:
                        st.session_state.is_finished = True

                    st.rerun()

        with col_btn2:
            if st.button("🏠 返回", width="stretch"):
                st.session_state.page = "home"
                st.rerun()

        # 生成报告按钮（3 个问题完成后显示）
        if st.session_state.round_count >= 3:
            st.markdown("---")
            st.success("✅ 诊断完成！现在可以查看你的心理诊断报告。")
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

