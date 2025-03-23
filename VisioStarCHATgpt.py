from openai import OpenAI
import requests
import json

class GPTNode:
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
                "gpt_model": (["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"],),
                "instruction_title": ("STRING", {
                    "multiline": False,
                    "default": "↓↓↓ 输入指令 ↓↓↓"
                }),
                "instruction": ("STRING", {
                    "multiline": True,
                    "default": "Optimize the AI instruction..."
                }),
                "prompt_topic_title": ("STRING", {
                    "multiline": False,
                    "default": "↓↓↓ 输入主题 ↓↓↓"
                }),
                "prompt_topic": ("STRING", {
                    "multiline": True,
                    "default": "一个女人在沙滩上"
                }),
                "temperature": ("FLOAT", {
                    "default": 0.7,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1
                }),
                "max_tokens": ("INT", {
                    "default": 512,
                    "min": 1,
                    "max": 4096,
                    "step": 1
                }),
                "top_p": ("FLOAT", {
                    "default": 0.9,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("response",)
    FUNCTION = "process"
    CATEGORY = "VisioStar"

    def process(self, api_url, api_key, gpt_model, instruction_title, instruction, prompt_topic_title, prompt_topic, temperature, max_tokens, top_p):
        combined_text = f"{instruction}\n{prompt_topic}"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": gpt_model,
            "messages": [
                {"role": "user", "content": combined_text}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p
        }

        try:
            response = requests.post(api_url, json=payload, headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                content = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
            else:
                content = f"API Error: {response.status_code} - {response.text}"

            return (content,)

        except Exception as e:
            return (f"Error: {str(e)}",)

NODE_CLASS_MAPPINGS = {
    "GPTNode": GPTNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GPTNode": "GPT API Node"
}
