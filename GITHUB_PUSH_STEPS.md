# 📤 将项目提交到 GitHub - 完整步骤

## 🎯 目标
将本地的 `study-mirror` 项目上传到 GitHub

## ✅ 当前状态
- ✅ 本地代码已完成
- ✅ Git 仓库已初始化
- ✅ 所有文件已提交
- ⏳ **还需要**：在 GitHub 上创建仓库并推送代码

---

## 📋 完整步骤（总共 5 分钟）

### 第 1 步：在 GitHub 上创建新仓库

#### 1.1 打开 GitHub
访问 [https://github.com](https://github.com)，登录你的账户

#### 1.2 创建新仓库
点击右上角的 **`+`** 图标 → 选择 **"New repository"**

#### 1.3 填写仓库信息

| 字段 | 值 |
|------|-----|
| Repository name | `study-mirror` |
| Description | `AI-powered learning psychology diagnostic tool` |
| Visibility | **Public** (公开) |
| Initialize | **不勾选** ❌ |

**重要**：不要勾选任何初始化选项，因为我们已有本地仓库

#### 1.4 点击 "Create repository"

---

### 第 2 步：复制仓库 URL

创建完成后，你会看到一个页面，上面显示：

```
Quick setup — if you've done this kind of thing before
```

点击绿色的 **"Code"** 按钮，确保选择 **"HTTPS"**，复制 URL：

```
https://github.com/yourusername/study-mirror.git
```

**⚠️ 重要**：将 `yourusername` 替换为你的 GitHub 用户名

---

### 第 3 步：在本地添加远程仓库

打开终端，执行以下命令：

```bash
cd /Users/yinjianbin/Projects/ai/study-mirror

# 添加远程仓库（替换 yourusername）
git remote add origin https://github.com/yourusername/study-mirror.git

# 验证是否添加成功
git remote -v
```

**预期输出**：
```
origin  https://github.com/yourusername/study-mirror.git (fetch)
origin  https://github.com/yourusername/study-mirror.git (push)
```

---

### 第 4 步：推送代码到 GitHub

执行以下命令：

```bash
git push -u origin main
```

**首次推送时会提示输入凭证**：
- **Username**: 你的 GitHub 用户名
- **Password**: 你的 GitHub 密码

⚠️ **注意**：如果使用了两步验证，需要使用 **Personal Access Token** 而不是密码

---

### 第 5 步：验证上传成功

1. 刷新 GitHub 仓库页面
2. 确认所有文件都已上传
3. 检查提交历史

---

## 🔐 如果遇到密码问题

### 方案 A：使用 Personal Access Token（推荐）

#### A1. 生成 Token

1. 访问 [https://github.com/settings/tokens](https://github.com/settings/tokens)
2. 点击 **"Generate new token"** → **"Generate new token (classic)"**
3. 填写信息：
   - **Note**: `study-mirror`
   - **Expiration**: 选择 90 days
   - **Scopes**: 勾选 `repo`
4. 点击 **"Generate token"**
5. **复制生成的 token**（只会显示一次！）

#### A2. 使用 Token 推送

```bash
git push -u origin main

# 当提示输入密码时，粘贴你的 token
```

### 方案 B：保存凭证（简化后续操作）

```bash
# 配置 Git 记住凭证
git config --global credential.helper osxkeychain

# 然后推送
git push -u origin main

# 输入用户名和密码/token，之后会自动保存
```

---

## 📝 完整命令清单

### 一次性执行所有命令

```bash
#!/bin/bash

# 进入项目目录
cd /Users/yinjianbin/Projects/ai/study-mirror

# 设置你的 GitHub 用户名
GITHUB_USERNAME="yourusername"

# 添加远程仓库
git remote add origin https://github.com/$GITHUB_USERNAME/study-mirror.git

# 验证
echo "=== Remote repositories ==="
git remote -v

# 推送代码
echo "=== Pushing code to GitHub ==="
git push -u origin main

echo "✅ Done! Your project is now on GitHub."
echo "📍 Visit: https://github.com/$GITHUB_USERNAME/study-mirror"
```

### 分步执行

```bash
# 1. 进入项目目录
cd /Users/yinjianbin/Projects/ai/study-mirror

# 2. 添加远程仓库
git remote add origin https://github.com/yourusername/study-mirror.git

# 3. 验证
git remote -v

# 4. 推送代码
git push -u origin main
```

---

## ✅ 验证清单

推送完成后，检查以下项目：

- [ ] GitHub 仓库已创建
- [ ] 所有文件都已上传（app.py, README.md 等）
- [ ] 提交历史正确显示（应该有 4 个提交）
- [ ] README.md 在仓库首页正确显示
- [ ] .gitignore 文件已上传
- [ ] 可以访问仓库页面

---

## 🎯 推送后的操作

### 1. 添加项目描述和标签

在 GitHub 仓库页面：
1. 点击右侧的 **"About"** 齿轮图标
2. 填写 **Description**: `AI-powered learning psychology diagnostic tool`
3. 添加 **Topics**: `ai`, `education`, `psychology`, `streamlit`, `python`
4. 点击 **"Save changes"**

### 2. 邀请朋友

分享仓库链接：
```
https://github.com/yourusername/study-mirror
```

邀请朋友给项目 ⭐ Star

### 3. 后续开发

创建新分支开发功能：
```bash
# 创建新分支
git checkout -b feature/ai-integration

# 进行开发...

# 提交更改
git add .
git commit -m "Add AI API integration"

# 推送到 GitHub
git push origin feature/ai-integration

# 在 GitHub 上创建 Pull Request
```

---

## 🐛 常见问题

### Q1: 提示 "fatal: remote origin already exists"

**原因**：远程仓库已经存在

**解决方案**：
```bash
# 删除现有的远程仓库
git remote remove origin

# 重新添加
git remote add origin https://github.com/yourusername/study-mirror.git
```

### Q2: 推送时提示 "Permission denied (publickey)"

**原因**：SSH 密钥配置问题

**解决方案**：使用 HTTPS 而不是 SSH
```bash
git remote set-url origin https://github.com/yourusername/study-mirror.git
```

### Q3: 推送时提示 "fatal: refusing to merge unrelated histories"

**原因**：本地和远程仓库历史不一致

**解决方案**：
```bash
git push -u origin main --force
```

### Q4: 忘记了 GitHub 用户名

访问 [https://github.com/settings/profile](https://github.com/settings/profile) 查看

### Q5: 如何修改已推送的提交？

```bash
# 修改最后一次提交信息
git commit --amend -m "New message"

# 强制推送（谨慎使用）
git push -f origin main
```

---

## 📊 项目信息

**项目名称**：Study Mirror（学习心理诊断工具）

**项目描述**：
```
AI-powered learning psychology diagnostic tool.
Diagnose students' learning psychology through 3-5 rounds of deep dialogue.
Quantify four core psychological dimensions: attribution style, self-efficacy,
cognitive load, and metacognition.
```

**主要文件**：
- `app.py` - 主应用程序（600 行）
- `requirements.txt` - 依赖管理
- `README.md` - 项目文档
- `LICENSE` - MIT 许可证

**技术栈**：
- Python 3.11+
- Streamlit 1.32+
- Plotly 5.18+

---

## 🎉 完成！

恭喜！你已经成功将项目上传到 GitHub。

现在你可以：
1. ⭐ 邀请朋友给项目 Star
2. 🔗 分享项目链接
3. 📝 编写项目文档
4. 🤝 接受 Pull Request
5. 🐛 管理 Issues
6. 📊 查看项目统计

---

## 📚 相关文档

- [README.md](README.md) - 项目完整文档
- [QUICK_START.md](QUICK_START.md) - 快速开始指南
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - 项目总结
- [UPLOAD_TO_GITHUB.md](UPLOAD_TO_GITHUB.md) - 详细上传指南

---

**Happy coding! 🚀**

