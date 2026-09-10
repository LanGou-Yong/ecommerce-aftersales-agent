# 电商售后工单助手（脱敏 Demo）

面向商家客服坐席的最小可行性 Demo：政策问答走知识库，查单走模拟订单库，退款必须人工点头。

这是公开技术验证，不是已上线客服系统，不接真实支付/退款通道。

## 30 秒看懂

| 你问 | 系统怎么走 | 用来证明什么 |
|---|---|---|
| 七天无理由怎么退？ | 政策 RAG / FAQ | 答复带来源，不空口政策 |
| 订单 A1001 到哪了？ | 只读查单工具 | 订单不靠模型编 |
| 订单 A1001 我要退款 | 草稿 + 待人工审核 | Agent 不能自己打款 |

## 这个 Demo 做了 / 没做

**已实现**

- 意图分流：政策 / 查单 / 退款 / 转人工
- 本地政策切片检索（关键词 + 重叠）
- SQLite 模拟订单只读查询
- 退款工单进入 `needs_approval`，调用批准接口后才标记完成

**刻意没做**

- 真实电商平台、支付、短信
- Redis / 登录鉴权 / 并发压测
- 自动执行退款

## 快速开始

需要 Python 3.10+。**下面请一行行执行**（每步成功后再做下一步）。

1. 进入本目录，创建虚拟环境并安装依赖：

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

成功：`python -c "import fastapi, streamlit"` 无输出。

2. 启动：

```bash
python start_demo.py
```

Windows 也可双击 `start.bat`。

成功：终端出现 `Backend ready`，浏览器打开 http://localhost:8511

停止：启动窗口 `Ctrl+C`。

## 接口

- `GET /health`
- `POST /ticket`  `{"query":"...","order_id":"A1001"}`
- `POST /approve_refund`  `{"ticket_id":"..."}`  （演示人审）

## 免责声明

仅供学习与技术演示。样例订单与政策为虚构数据。
