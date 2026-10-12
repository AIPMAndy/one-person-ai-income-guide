# 发布到 GitHub 的最短路径

**建议仓库名：** `one-person-ai-income-guide`；**建议项目简介：** `一个人一台电脑，靠 AI 找客户、完成交付、获得第一笔付费收入的免费开源保姆级攻略。含7种业务 SOP、30天任务、Prompt与离线工具。`

**话题标签（Topics）：** `ai`、`solopreneur`、`side-project`、`career`、`productivity`、`awesome-cn`、`中文教程`（以GitHub实际可接受的topic格式为准）。

目标仓库：[AIPMAndy/one-person-ai-income-guide](https://github.com/AIPMAndy/one-person-ai-income-guide)；在线入口：[互动指南](https://aipmandy.github.io/one-person-ai-income-guide/)。部署状态以 Actions 与正式网址验收为准。

## 1. 本地检查

```bash
python3 build.py
python3 -m unittest discover -s tests -v
```

## 2. 创建空仓库

在 GitHub 账号 `AIPMAndy` 新建**公开**空仓库 `one-person-ai-income-guide`，先不要勾选“Add a README / .gitignore / License”。如果你安装并认证了 GitHub CLI，可以在项目根目录：

```bash
git init -b main
git add .
git commit -m "docs: release practical AI solo income guide"
gh repo create AIPMAndy/one-person-ai-income-guide --public --source=. --remote=origin --push
```

这些命令仅在你本地运行后才真正创建远程仓库；文件包不会自动发布。若仓库已创建，改用普通 `git remote add origin ...` 和 `git push -u origin main`。

## 3. 开启 GitHub Pages

仓库 `Settings → Pages → Build and deployment → Deploy from a branch → main / (root) → Save`。静态 HTML 可以使用 root 发布。官方文档：https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

等实际发布验证成功后，才能对外提供 GitHub Pages 链接；仓库存在≠站点已开启。不要把尚未发布的网址写成“在线可用”。

## 4. 发布当日传播

**标题示例：**《一个人，一台电脑，靠AI赚钱，我把整套方法开源了》。必须真实说明：免费、包含哪些模板、适合谁、不能保证赚钱。封面可使用 `assets/social-preview.svg` 导出 PNG。

**渠道动作：**

1. GitHub：README开头明确一键进入、7条路线、免费模板和安全边界。
2. 公众号：讲自己为什么做这份教程，展示样稿、三张关键流程图，附真实仓库链接。
3. 小红书/抖音：3:4图文/字幕视频，先讲最有用的三条路线，再展示模板和网页；按平台规范披露AI生成内容，不发布站外违规导流内容。
4. 评论区：优先回答“我应该从哪条路线开始”，不强迫先加微信。

**可衡量的指标：** 仓库 Stars、独立访问（若有合法可用统计）、模板使用反馈、有效咨询人数、真实付费客户数、交付通过率。不要拿一个高播放量证明赚钱方法有效。工具网页默认不埋点，不能凭空提供其访问数据。

## 5. 咨询承接与去商业化风险

免费教程涵盖完整步骤，私信和咨询只解决个性化疑难。作者微信 `AIPMAndy`、官网 `https://metaver.vip/`。禁止“只有购买课程才能拿模板”、虚假名额倒计时和虚构案例。

## 真实案例发布检查（新增）

对外写数字前，逐一核查 [真人案例库](cases/REAL-CASE-INDEX.md)、[专项审查](cases/CASE-AUDIT.md)：公开内容必须包含**人物/业务、来源链接、报告口径、起点和不能推断**。自报数额要加「受访者称」；客户业务额、媒体报价、网站播放量不能写成本人净利润；不得复制未获授权的新闻图片。
