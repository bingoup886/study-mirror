# 🚀 GitHub 提交指南

本文档说明如何将本项目提交到 GitHub。

## 📋 前置条件

- 已安装 Git
- 拥有 GitHub 账户
- 已在本地初始化 Git 仓库（已完成 ✅）

## 🔧 步骤 1：创建 GitHub 仓库

### 1.1 登录 GitHub
访问 [GitHub](https://github.com) 并登录你的账户

### 1.2 创建新仓库
1. 点击右上角的 `+` 图标
2. 选择 "New repository"
3. 填写仓库信息：
   - **Repository name**: `study-mirror`
   - **Description**: AI-powered learning psychology diagnostic tool
   - **Public/Private**: 选择 Public（公开）
   - **Initialize this repository with**: 不勾选（因为我们已有本地仓库）
4. 点击 "Create repository"

### 1.3 复制仓库 URL
创建完成后，复制 HTTPS 或 SSH URL（推荐 HTTPS）
```
https://github.com/yourusername/study-mirror.git
```

## 🔗 步骤 2：添加远程仓库

在本地项目目录执行：

```bash
cd /Users/yinjianbin/Projects/ai/study-mirror

# 添加远程仓库
git remote add origin https://github.com/yourusername/study-mirror.git

# 验证远程仓库
git remote -v
```

## 📤 步骤 3：推送代码到 GitHub

### 3.1 重命名主分支（如需要）
```bash
# 如果本地分支是 master，改为 main
git branch -M main
```

### 3.2 推送代码
```bash
# 首次推送，设置上游分支
git push -u origin main

# 后续推送
git push
```

## ✅ 步骤 4：验证提交

1. 访问你的 GitHub 仓库页面
2. 确认所有文件都已上传
3. 检查 README.md 是否正确显示

## 📝 常用 Git 命令

### 查看状态
```bash
git status
```

### 查看提交历史
```bash
git log --oneline
```

### 查看远程仓库
```bash
git remote -v
```

### 修改远程 URL
```bash
git remote set-url origin https://github.com/yourusername/study-mirror.git
```

## 🔐 SSH 密钥配置（可选）

如果想使用 SSH 而不是 HTTPS：

### 1. 生成 SSH 密钥
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

### 2. 添加到 SSH Agent
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

### 3. 添加到 GitHub
1. 复制公钥内容：`cat ~/.ssh/id_ed25519.pub`
2. 访问 GitHub Settings → SSH and GPG keys
3. 点击 "New SSH key"
4. 粘贴公钥内容

### 4. 修改远程 URL 为 SSH
```bash
git remote set-url origin git@github.com:yourusername/study-mirror.git
```

## 🎯 后续工作流

### 创建新分支开发功能
```bash
# 创建并切换到新分支
git checkout -b feature/new-feature

# 进行开发...

# 提交更改
git add .
git commit -m "Add new feature"

# 推送到 GitHub
git push origin feature/new-feature

# 在 GitHub 上创建 Pull Request
```

### 更新本地代码
```bash
# 拉取最新代码
git pull origin main
```

## 📊 项目统计

```bash
# 查看代码行数
wc -l app.py

# 查看 Git 统计
git log --stat
```

## 🐛 常见问题

### Q: 如何修改最后一次提交？
```bash
git commit --amend -m "New commit message"
git push -f origin main  # 强制推送（谨慎使用）
```

### Q: 如何撤销最后一次提交？
```bash
git reset --soft HEAD~1  # 保留更改
git reset --hard HEAD~1  # 丢弃更改
```

### Q: 如何删除远程分支？
```bash
git push origin --delete branch-name
```

### Q: 如何克隆项目？
```bash
git clone https://github.com/yourusername/study-mirror.git
cd study-mirror
pip install -r requirements.txt
streamlit run app.py
```

## 📚 相关资源

- [GitHub 官方文档](https://docs.github.com)
- [Git 官方文档](https://git-scm.com/doc)
- [GitHub Desktop](https://desktop.github.com)（图形化工具）

## 🎉 完成！

恭喜！你已经成功将项目提交到 GitHub。现在你可以：

1. ⭐ 邀请朋友给项目 Star
2. 🔗 分享项目链接
3. 📝 编写项目文档
4. 🤝 接受 Pull Request
5. 🐛 管理 Issues

---

**Happy coding! 🚀**

