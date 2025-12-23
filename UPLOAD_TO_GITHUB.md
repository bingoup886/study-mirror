# 📤 上传项目到 GitHub - 完整步骤指南

## ✅ 当前状态

你的项目已经：
- ✅ 初始化了 Git 仓库
- ✅ 提交了所有代码文件
- ✅ 配置了 Git 用户信息
- ✅ 创建了 .gitignore 文件

现在需要将代码推送到 GitHub。

## 🚀 上传步骤

### 步骤 1：在 GitHub 上创建新仓库

#### 1.1 访问 GitHub
打开浏览器，访问 [https://github.com](https://github.com)

#### 1.2 登录你的账户
如果还没有账户，请先注册一个

#### 1.3 创建新仓库
1. 点击右上角的 **`+`** 图标
2. 选择 **"New repository"**

#### 1.4 填写仓库信息

```
Repository name: study-mirror
Description: AI-powered learning psychology diagnostic tool
Visibility: Public (公开)
```

**重要**：不要勾选 "Initialize this repository with a README"（因为我们已有本地仓库）

#### 1.5 点击 "Create repository"

创建完成后，你会看到一个页面，上面有仓库的 URL。

---

### 步骤 2：复制仓库 URL

在 GitHub 仓库页面，点击绿色的 **"Code"** 按钮，选择 **"HTTPS"**，复制 URL：

```
https://github.com/yourusername/study-mirror.git
```

**注意**：将 `yourusername` 替换为你的 GitHub 用户名

---

### 步骤 3：在本地添加远程仓库

在终端中执行以下命令：

```bash
cd /Users/yinjianbin/Projects/ai/study-mirror

# 添加远程仓库（将 yourusername 替换为你的用户名）
git remote add origin https://github.com/yourusername/study-mirror.git

# 验证远程仓库是否添加成功
git remote -v
```

**预期输出**：
```
origin  https://github.com/yourusername/study-mirror.git (fetch)
origin  https://github.com/yourusername/study-mirror.git (push)
```

---

### 步骤 4：推送代码到 GitHub

执行以下命令将本地代码推送到 GitHub：

```bash
# 首次推送，设置上游分支
git push -u origin main
```

**首次推送时可能需要输入 GitHub 凭证**：
- 用户名：你的 GitHub 用户名
- 密码：你的 GitHub 密码（或 Personal Access Token）

---

### 步骤 5：验证上传成功

1. 刷新 GitHub 仓库页面
2. 确认所有文件都已上传
3. 检查提交历史是否正确

---

## 🔐 如果遇到身份验证问题

### 方案 A：使用 Personal Access Token（推荐）

#### A1. 生成 Personal Access Token

1. 访问 [GitHub Settings - Tokens](https://github.com/settings/tokens)
2. 点击 "Generate new token"
3. 选择 "Generate new token (classic)"
4. 填写信息：
   - **Note**: `study-mirror-push`
   - **Expiration**: 选择合适的过期时间
   - **Scopes**: 勾选 `repo`（完整的仓库访问权限）
5. 点击 "Generate token"
6. **复制生成的 token**（只会显示一次）

#### A2. 使用 Token 推送

```bash
# 使用 token 作为密码
git push -u origin main

# 当提示输入密码时，粘贴你的 token
```

### 方案 B：使用 SSH 密钥

#### B1. 生成 SSH 密钥

```bash
# 生成 SSH 密钥
ssh-keygen -t ed25519 -C "your_email@example.com"

# 按 Enter 接受默认位置
# 输入密码（可选）
```

#### B2. 添加到 SSH Agent

```bash
# 启动 SSH Agent
eval "$(ssh-agent -s)"

# 添加私钥
ssh-add ~/.ssh/id_ed25519
```

#### B3. 添加公钥到 GitHub

1. 复制公钥：
```bash
cat ~/.ssh/id_ed25519.pub
```

2. 访问 [GitHub Settings - SSH Keys](https://github.com/settings/keys)
3. 点击 "New SSH key"
4. 粘贴公钥内容
5. 点击 "Add SSH key"

#### B4. 修改远程 URL 为 SSH

```bash
git remote set-url origin git@github.com:yourusername/study-mirror.git

# 验证
git remote -v
```

#### B5. 推送代码

```bash
git push -u origin main
```

---

## 📋 完整命令清单

### 一键上传脚本

如果你想一次性执行所有命令，可以使用以下脚本：

```bash
#!/bin/bash

# 进入项目目录
cd /Users/yinjianbin/Projects/ai/study-mirror

# 设置 GitHub 用户名（替换为你的用户名）
GITHUB_USERNAME="yourusername"

# 添加远程仓库
git remote add origin https://github.com/$GITHUB_USERNAME/study-mirror.git

# 验证远程仓库
echo "Remote repositories:"
git remote -v

# 推送代码
echo "Pushing code to GitHub..."
git push -u origin main

echo "Done! Your project is now on GitHub."
```

### 手动命令

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

上传完成后，检查以下项目：

- [ ] GitHub 仓库已创建
- [ ] 所有文件都已上传
- [ ] README.md 在仓库首页正确显示
- [ ] 提交历史正确显示
- [ ] 可以看到 2 个提交记录
- [ ] .gitignore 文件已上传

---

## 🎯 上传后的操作

### 1. 添加项目描述

在 GitHub 仓库页面：
1. 点击 "About" 齿轮图标
2. 填写 Description：`AI-powered learning psychology diagnostic tool`
3. 添加 Website（可选）
4. 添加 Topics：`ai`, `education`, `psychology`, `streamlit`

### 2. 启用 GitHub Pages（可选）

如果想创建项目网站：
1. 进入 Settings → Pages
2. 选择 Source 为 "main" 分支
3. 选择 folder 为 "/root"

### 3. 邀请协作者（可选）

1. 进入 Settings → Collaborators
2. 点击 "Add people"
3. 输入协作者的 GitHub 用户名

### 4. 设置 Branch Protection（可选）

1. 进入 Settings → Branches
2. 点击 "Add rule"
3. 设置保护规则

---

## 🐛 常见问题

### Q1: 提示 "fatal: remote origin already exists"

**解决方案**：
```bash
# 删除现有的远程仓库
git remote remove origin

# 重新添加
git remote add origin https://github.com/yourusername/study-mirror.git
```

### Q2: 推送时提示 "Permission denied"

**解决方案**：
- 检查 GitHub 用户名是否正确
- 使用 Personal Access Token 而不是密码
- 或者使用 SSH 密钥

### Q3: 推送时提示 "fatal: refusing to merge unrelated histories"

**解决方案**：
```bash
git push -u origin main --force
```

### Q4: 如何修改已推送的提交？

**解决方案**：
```bash
# 修改最后一次提交
git commit --amend -m "New message"

# 强制推送（谨慎使用）
git push -f origin main
```

### Q5: 如何删除远程仓库中的文件？

**解决方案**：
```bash
# 从 Git 中删除文件（但保留本地文件）
git rm --cached filename

# 提交更改
git commit -m "Remove filename"

# 推送
git push origin main
```

---

## 📚 后续工作流

### 日常开发流程

```bash
# 1. 创建新分支
git checkout -b feature/new-feature

# 2. 进行开发...

# 3. 提交更改
git add .
git commit -m "Add new feature"

# 4. 推送到 GitHub
git push origin feature/new-feature

# 5. 在 GitHub 上创建 Pull Request
# 6. 代码审查
# 7. 合并到 main 分支
```

### 更新本地代码

```bash
# 拉取最新代码
git pull origin main
```

### 查看提交历史

```bash
# 查看简洁的提交历史
git log --oneline

# 查看详细的提交历史
git log --stat
```

---

## 🎉 完成！

恭喜！你已经成功将项目上传到 GitHub。现在你可以：

1. ⭐ 邀请朋友给项目 Star
2. 🔗 分享项目链接
3. 📝 编写项目文档
4. 🤝 接受 Pull Request
5. 🐛 管理 Issues
6. 📊 查看项目统计

---

## 📞 需要帮助？

- 📖 [GitHub 官方文档](https://docs.github.com)
- 🔗 [Git 官方文档](https://git-scm.com/doc)
- 💬 [GitHub Community](https://github.community)

---

**Happy coding! 🚀**

