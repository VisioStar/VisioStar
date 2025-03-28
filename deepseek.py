import requests
import json

class DeepSeekNode:
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

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("response",)
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
                            content = choices[0].get("message", {}).get("content", "No response content")
                        else:
                            content = "Empty response from DeepSeek"
                    except json.JSONDecodeError:
                        content = "Failed to parse DeepSeek response JSON"
                else:
                    content = f"DeepSeek API Error: {response.status_code} - {response.text}"

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
                            content = choices[0].get("message", {}).get("content", "No response content")
                        else:
                            content = "Empty response from SiliconFlow"
                    except json.JSONDecodeError:
                        content = "Failed to parse SiliconFlow response JSON"
                else:
                    content = f"SiliconFlow API Error: {response.status_code} - {response.text}"
            else:
                raise ValueError("Invalid API choice")

            return (content,)

        except Exception as e:
            error_message = f"Error: {str(e)}"
            return (error_message,)

NODE_CLASS_MAPPINGS = {
    "DeepSeekNode": DeepSeekNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DeepSeekNode": "☆VisioStar Deepseek API"
}
