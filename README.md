[中文版说明](README-zh.md)

Cerebras is an AI chat interface provider. As of February 1, 2025, they offer three models:
- llama3.1-8b
- llama-3.3-70b
- deepseek-r1-distill-llama-70b

This project allows you to connect these models to any AI chat client (tested with Chatbox).

# How to Use

Run `python serve.py`

Before running, you need to complete the following preparations:

## Get Token:

Register and log in to [Cerebras](https://inference.cerebras.ai/)

Open the browser developer panel by pressing `Ctrl`+`Shift`+`I` in your browser.

For example, in Chrome, select Application -> Cookies, and find `authjs.session-token`.

![Chatbox Setting](/how-to-get-token.png)

Record its value (in the format: `a1b2c3d4-5e6f-1a2b-3c4d-12345678abcd`)

This token is valid for one month.

## Configure the Interface

### Set Token (the value obtained from the browser)

Method 1: Set the environment variable `AUTHJS_SESSION_TOKEN`

`set AUTHJS_SESSION_TOKEN=authjs.session-token`

Method 2: Modify the value of `authjs_session_token` in the `serve.py` file.

Method 3: Access the /renew?key={api key}&token={token} endpoint.

For example: http://127.0.0.1:7860/renew?key=my-api-key&token=a1b2c3d4-5e6f-1a2b-3c4d-12345678abcd

Method 3 supports replacing the token at any time without interrupting the program.

### Set API Key

Method 1: Set the environment variable `SERVER_API_KEY`

`set SERVER_API_KEY=my-api-key`

Method 2: Modify the value of `server_api_key` in the `serve.py` file.

The `api key` is used for chat application verification and hot-swapping session tokens. It is not a Cerebras API key. You can set it to any value you like (without spaces).

# Note:

Each token has a limit on the number of accesses per minute/hour/day, and each token has a limit on the response length per day.

If the response is empty, the threshold may have been triggered. Please try again later.

# Deploy on Huggingface

1. [Duplicate this Space](https://huggingface.co/spaces/tastypear/Cerebras-API?duplicate=true), and set `SERVER_API_KEY` to your API key.

2. Select `Embed this Space` from the top-right menu.  The `{Direct URL}/api` is the interface. The Demo's interface address is: `https://tastypear-cerebras-api.hf.space/api`

3. In Settings, set `SPACE_URL` to your `Direct URL` to prevent the Space from automatically stopping.

4. Once the Space has started, update your token using `Method 3` under "Set Token". For example, the Demo's update address is: https://tastypear-cerebras-api.hf.space/renew?……

# Client Settings Demo (using Chatbox as an example)

![Chatbox Setting](/client-setting.png)
