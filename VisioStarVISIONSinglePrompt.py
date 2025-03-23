import requests
import json
import base64
from io import BytesIO
from PIL import Image
import numpy as np

class VisioStarVISIONSinglePrompt:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "api_url": ("STRING", {
                    "multiline": False,
                    "default": "https://api.openai.com/v1/chat/completions"
                }),
                "api_key": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
                "model": (
                    ["gpt-4o", "gpt-4-turbo", "gpt-4-vision-preview"],
                    {"default": "gpt-4o"}
                ),
                "temperature": ("FLOAT", {
                    "default": 0.7, "min": 0.0, "max": 2.0, "step": 0.1
                }),
                "max_tokens": ("INT", {
                    "default": 512, "min": 1, "max": 2048, "step": 1
                }),
                "top_p": ("FLOAT", {
                    "default": 1.0, "min": 0.0, "max": 1.0, "step": 0.1
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "run"
    CATEGORY = "VisioStar"

    def run(self, image, api_url, api_key, model, temperature, max_tokens, top_p):
        try:
            # 将 ComfyUI 的 tensor 图像转为 base64 JPEG
            np_image = image[0].cpu().numpy()
            np_image = (np_image * 255).clip(0, 255).astype("uint8")
            pil_image = Image.fromarray(np_image)
            buffered = BytesIO()
            pil_image.save(buffered, format="JPEG")
            encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
        except Exception as e:
            return (f"❌ 图像编码失败: {str(e)}",)

        # 固定指令（中文描述）
        vision_prompt = (
            "根据图像描述高质量详细的自然语言的英文提示词，"
            "请勿提及图像的分辨率，请勿使用任何模棱两可的语言，"
            "其他根据你的经验和的特色进行个性化优化调整提示词。"
        )

        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_image}"
                            }
                        },
                        {
                            "type": "text",
                            "text": vision_prompt
                        }
                    ]
                }
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p
        }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(api_url, headers=headers, json=payload)
            if response.status_code == 200:
                data = response.json()
                full_response = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                return (full_response.strip(),)
            else:
                return (f"❌ API Error: {response.status_code} - {response.text}",)
        except Exception as e:
            return (f"❌ 请求失败: {str(e)}",)
