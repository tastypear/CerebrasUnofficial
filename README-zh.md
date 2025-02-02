Cerebras 是 AI 聊天接口供应商，截至 2025 年 2 月 1 日，他们提供三个模型：
- llama3.1-8b
- llama-3.3-70b
- deepseek-r1-distill-llama-70b

通过本项目，你可以将以上模型接入任意AI聊天客户端（已测试Chatbox）

# 使用方式

运行 `python serve.py`

在实际运行前，你需要完成以下准备工作

## 获取 token：
注册并登录 [Cerebras](https://inference.cerebras.ai/)

在浏览器 `Ctrl`+`Shift`+`I` 打开浏览器开发者面板

以 Chrome 为例，选择应用 -> Cookie，找到 `authjs.session-token`

![Chatbox Setting](/how-to-get-token.png)

记录它的值（形如：`a1b2c3d4-5e6f-1a2b-3c4d-12345678abcd`）

该token的有效期为1个月。

## 设置接口

### 设置 token（即从浏览器获得的值）

方法一：设置环境变量 `SERVER_API_KEY`

`set SERVER_API_KEY=my-api-key`

方法二：修改 `serve.py` 文件中 `authjs_session_token` 的值

`set AUTHJS_SESSION_TOKEN=authjs.session-token`

方法三：访问 /renew?key={api key}&token={token} 接口

如：http://127.0.0.1:7860/renew?key=my-api-key&token=a1b2c3d4-5e6f-1a2b-3c4d-12345678abcd

方法三支持随时替换新的 token，而不必中断程序

### 设置 api key

方法一：设置环境变量 `SERVER_API_KEY`

`set SERVER_API_KEY=my-api-key`

方法二：修改 `serve.py` 文件中 `server_api_key` 的值

`api key` 用于聊天应用验证与热更新 session token，它不是 Cerebras 的 api key，你可以设定为你喜欢的值（不要带空格）

# 注意：

每个 token 每分钟/小时/天均有访问次数上限，每个 token 每天均有回应长度上限

如果回应结果为空，可能已触发阈值，请稍后再试

# 在 Huggingface 上部署

1. [Dumplicate this Space](https://huggingface.co/spaces/tastypear/Cerebras-API?duplicate=true)，将 `SERVER_API_KEY` 设置为你的 api key

2. 在右上角菜单选择 `Embed this Space`，`{Direct URL}/api` 即为接口。Demo 的接口地址为：`https://tastypear-cerebras-api.hf.space/api`

3. 在 Setting 中将 `SPACE_URL` 设置为你的 `Direct URL`，以防止 Space 自动停止

4. 当 Space 启动完成后，通过 `设置token` 中的 `方法三`，更新你的token。例如 Demo 的更新地址为 https://tastypear-cerebras-api.hf.space/renew?……

# 客户端设置演示（以Chatbox为例）

![Chatbox Setting](/client-setting.png)
