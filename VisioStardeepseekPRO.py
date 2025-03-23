import requests
import json
import re

class VisioStardeepseekPRO:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "instruction_title": ("STRING", {
                    "multiline": False,
                    "default": "↓↓↓ 输入指令 ↓↓↓"
                }),
                "instruction": ("STRING", {
                    "multiline": True,
                    "default": "你是一个AI提示词优化大师，请用自然语言优化这个提示词，"
                               "要求生成 3 个不同方向的高质量提示词，并按照以下格式返回：\n\n"
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
                "api_key": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
                "api_choice": (["deepseek", "siliconflow"],),
                "model": ("STRING", {
                    "multiline": False,
                    "default": "deepseek-reasoner"
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
                    "default": 0.7,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1
                }),
            },
            "optional": {
                "top_k": ("INT", {
                    "default": 50,
                    "min": 1,
                    "max": 100,
                    "step": 1
                }),
                "frequency_penalty": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("response_1", "response_2", "response_3")
    FUNCTION = "process"
    CATEGORY = "VisioStar"

    def process(self, instruction_title, instruction, prompt_topic_title, prompt_topic, api_key, api_choice, model, temperature, max_tokens, top_p, top_k=50, frequency_penalty=0.5):
        combined_text = f"{instruction}\n提示词主题：{prompt_topic}"

        try:
            if api_choice == "deepseek":
                # ========== DeepSeek API 调用 ==========
                url = "https://api.deepseek.com/v1/chat/completions"
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

                response = requests.post(url, headers=headers, json=payload)
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        choices = data.get("choices", [])
                        if choices:
                            full_response = choices[0].get("message", {}).get("content", "No response content")
                        else:
                            full_response = "Empty response from DeepSeek"
                    except json.JSONDecodeError:
                        full_response = "Failed to parse DeepSeek response JSON"
                else:
                    full_response = f"DeepSeek API Error: {response.status_code} - {response.text}"

            elif api_choice == "siliconflow":
                # ========== SiliconFlow API 调用 ==========
                url = "https://api.siliconflow.cn/v1/chat/completions"
                if model == "deepseek-reasoner":
                    model = "Qwen/QwQ-32B"
                
                payload = {
                    "model": model,
                    "messages": [{"role": "user", "content": combined_text}],
                    "stream": False,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "top_p": top_p,
                    "top_k": top_k,
                    "frequency_penalty": frequency_penalty,
                    "n": 1,
                    "response_format": {"type": "text"}
                }
                headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
                response = requests.post(url, json=payload, headers=headers)

                if response.status_code == 200:
                    try:
                        response_data = response.json()
                        choices = response_data.get("choices", [])
                        if choices:
                            full_response = choices[0].get("message", {}).get("content", "No response content")
                        else:
                            full_response = "Empty response from SiliconFlow"
                    except json.JSONDecodeError:
                        full_response = "Failed to parse SiliconFlow response JSON"
                else:
                    full_response = f"SiliconFlow API Error: {response.status_code} - {response.text}"
            else:
                raise ValueError("Invalid API choice")

            # **解析返回的 3 个提示语**
            match_1 = re.search(r"提示1:\s*(.+)", full_response)
            match_2 = re.search(r"提示2:\s*(.+)", full_response)
            match_3 = re.search(r"提示3:\s*(.+)", full_response)

            response_1 = match_1.group(1) if match_1 else "Error: Missing response_1"
            response_2 = match_2.group(1) if match_2 else "Error: Missing response_2"
            response_3 = match_3.group(1) if match_3 else "Error: Missing response_3"

            return (response_1, response_2, response_3)

        except Exception as e:
            error_message = f"Error: {str(e)}"
            return (error_message, error_message, error_message)

NODE_CLASS_MAPPINGS = {
    "VisioStardeepseekPRO": VisioStardeepseekPRO
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VisioStardeepseekPRO": "VisioStar DeepSeek PRO"
}
