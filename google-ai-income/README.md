# Google AI 赚钱保姆级实战攻略

> **Google AI Income Handbook — Free, open-source, evidence-first.** 2026-11-23 更新。

**在线网站：** https://aipmandy.github.io/one-person-ai-income-guide/google-ai-income/  
**完整 PDF：** [下载离线电子书](pdf/google-ai-income-handbook.pdf)  
**源码位置：** https://github.com/AIPMAndy/one-person-ai-income-guide/tree/main/google-ai-income

**作者：** AI 酋长 Andy / 星觉科技  
**微信：** `AIPMAndy`（可在网站首页、内容、页脚一键复制）  
**个人官网：** https://metaver.vip/  
**企业官网：** https://www.a6no1.cn/  
**咨询与陪跑：** https://metaver.vip/services

## 先看路线

| 方向 | 买家 | 最小可验收交付 |
| --- | --- | --- |
| 企业情报/竞品研究 | 产品/营销负责人 | 12 页报告 + 可追溯来源台账 |
| 本地商家内容 | 门店负责人 | 7 条可编辑脚本 + 核验清单 |
| Flow 视频交付 | 品牌/个人 IP | 15–30 秒样片 + 版权与披露记录 |
| AI Studio 微工具 | 企业团队 | 可访问工具 + 源码 + 10 条测试 |
| Opal/Sheets 流程 | 运营/客服 | 有人工审批的可停止工作流 |
| 企业培训 | 业务/培训负责人 | 2 小时课程 + 20 页 SOP |
| 跨境内容本地化 | 跨境公司 | 双语落地页 + 术语和质量对照 |
| YouTube 原创/IP | 观众/品牌 | 原创深度内容 + 商业服务入口 |

**没有可靠证据时不承诺订单和收入。** 这是一套真实需求验证与经营利润的练习工具，不是“Google 给你发钱”的项目。

## 内容

- `index.html`：响应式、无构建依赖的互动网站。
- `assets/data.js`：8 条业务路线、22 章、16 套 Prompt、30 天清单、12 条官方来源。
- `chapters/COMPLETE-GUIDE.md`：完整步骤和示范；新手可直接照做。
- `chapters/PROMPTS.md`：16 套可复制工作指令。
- `chapters/30-DAY-PLAN.md`：每日执行清单。
- `chapters/SOURCES.md`：官方资料和政策核查说明。
- `templates/`：需求访谈、SOW/验收、QA、线索、经营成本和证据台账。
- `print.html`：无依赖全文打印页面，可保存 PDF。
- `pdf/google-ai-income-handbook.pdf`：带目录的完整中文电子书。
- `tests/`：离线数据、链接和安全验收脚本。

## 免费实用功能

1. 八条路线筛选 + 启发式路线选择器。
2. 22 章可搜索的阅读器，逐章操作与验收。
3. 16 套 Prompt 过滤、展开和一键复制。
4. 订单直接贡献/有效时薪计算器，月目标产能压力测试。
5. 30 天每日勾选进度，本地保存、JSON 导出和恢复。
6. 生成第一份一页式服务说明，下载 `.txt`。
7. 微信号 `AIPMAndy` 一键复制，PDF/模板与官网免费访问。

所有计算、进度与填写内容都只在浏览器本地运行，不会通过本网站上传数据。无追踪 SDK、无远程 AI 模型调用、无用户注册；无痕窗口的本地存储可能无法持久保存。

## 运行、测试和 PDF 构建

```bash
# 不需要 npm install：直接在浏览器打开 index.html
python3 -m http.server 8000
# 打开 http://localhost:8000

# 检查数据完整性和安全
python3 -m unittest discover -s tests -v
node --check assets/app.js

# 再版 PDF（Python + ReportLab）
python3 -m pip install reportlab
python3 make_pdf.py
```

打包发布只需复制 `google-ai-income/` 目录。GitHub Pages 采用本仓库现有主站的静态目录发布配置，本项目与主站其他文件无侵入耦合。**`python3 build.py` 是父仓库已有站点生成流程，不能在本项目目录下替代执行。**

## 关于 2026 最新版 Google 工具

- NotebookLM 于 2026-07-16 正式更名 **Gemini Notebook**。
- **Firebase Studio 自 2026-06-22 起停止新建**；2027-03-22 下线。新项目优先使用 Google AI Studio Build 或 Google Antigravity。
- AI Studio Build 的 `GEMINI_API_KEY` 应只放在服务端 Secrets。任何公开仓库或浏览器端都不能保存私有密钥。
- Gemini App/Flow/API 免费额度、模型可用性、价格、地区以及付费政策可能变化。交易前必须核对 [官方来源](chapters/SOURCES.md)。
- YouTube 对高度重复、缺少原创价值的量产内容有变现限制；逼真合成内容按规则标识。

## 开源授权与边界

原创代码 MIT；原创文字 CC BY 4.0。各第三方 Google 产品名称、商标和文档归其权利人。**本站是独立学习资料，未获 Google 赞助或官方认可。** 价格、案例和收入等一律不作保证，报告中所有虚构案例已标示。涉及法律、税务、隐私和知识产权的问题需按当地规则进一步核查。

欢迎纠错，优先提交：失效的官方链接、无法复现的步骤、移动端阅读问题、安全问题或实际可复核的业务数据。不要在 Issue 中公开客户个人数据或密钥。