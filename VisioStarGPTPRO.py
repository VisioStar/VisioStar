import requests
import json
import re

class VisioStarGPTPRO:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "api_url": ("STRING", {
                    "multiline": False,
                    "default": "https://api.openai.com/v1/chat/completions"
                }),
                "api_key": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
                "model": (
                    ["gpt-4o", "gpt-4o-mini", "gpt-4", "gpt-4-turbo", "gpt-3.5-turbo", "gpt-3.5-turbo-16k"],
                    {"default": "gpt-4o"}
                ),
                "instruction_title": ("STRING", {
                    "multiline": False,
                    "default": "↓↓↓ 输入指令 ↓↓↓"
                }),
                "instruction": ("STRING", {
                    "multiline": True,
                    "default": "你是一个AI提示词优化大师，请用自然语言优化这个提示词，要求生成 3 个不同方向的高质量提示词，并按照以下格式返回：\n\n"
                               "提示1: (第一个提示语)\n"
                               "提示2: (第二个提示语)\n"
                               "提示3: (第三个提示语)\n"
                               "请直接返回英文提示词，不要返回多余的内容。"
                }),
                "prompt_topic_title": ("STRING", {
                    "multiline": False,
                    "default": "↓↓↓ 输入主题 ↓↓↓"
                }),
                "prompt_topic": ("STRING", {
                    "multiline": True,
                    "default": "一个女人在海里"
                }),
                "temperature": ("FLOAT", {
                    "default": 0.7, "min": 0.0, "max": 2.0, "step": 0.1
                }),
                "max_tokens": ("INT", {
                    "default": 512, "min": 1, "max": 4096, "step": 1
                }),
                "top_p": ("FLOAT", {
                    "default": 1.0, "min": 0.0, "max": 1.0, "step": 0.1
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("response_1", "response_2", "response_3")
    FUNCTION = "run"
    CATEGORY = "VisioStar"

    def run(self, api_url, api_key, model, instruction_title, instruction, prompt_topic_title, prompt_topic,
            temperature, max_tokens, top_p):

        combined_text = f"{instruction}\n提示词主题：{prompt_topic}"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "messages": [{"role": "user", "content": combined_text}],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p
        }

        try:
            response = requests.post(api_url, json=payload, headers=headers)

            if response.status_code == 200:
                try:
                    data = response.json()
                    full_response = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                except json.JSONDecodeError:
                    full_response = "⚠️ 无法解析 GPT 响应 JSON"
            else:
                full_response = f"❌ API Error: {response.status_code} - {response.text}"

            # 提取提示词内容
            match_1 = re.search(r"提示1:\s*(.+)", full_response)
            match_2 = re.search(r"提示2:\s*(.+)", full_response)
            match_3 = re.search(r"提示3:\s*(.+)", full_response)

            response_1 = match_1.group(1) if match_1 else "❌ 提示1 解析失败"
            response_2 = match_2.group(1) if match_2 else "❌ 提示2 解析失败"
            response_3 = match_3.group(1) if match_3 else "❌ 提示3 解析失败"

            return (response_1, response_2, response_3)

        except Exception as e:
            return (f"Error: {str(e)}", f"Error: {str(e)}", f"Error: {str(e)}")

# 注册节点
NODE_CLASS_MAPPINGS = {
    "VisioStarGPTPRO": VisioStarGPTPRO
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VisioStarGPTPRO": "🤖 VisioStar GPT PRO"
}
