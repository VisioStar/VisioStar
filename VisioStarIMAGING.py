
import requests
import json
import re
import base64
from io import BytesIO
from PIL import Image
import numpy as np

class VisioStarIMAGING:
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
                    "default": 1024, "min": 1, "max": 4096, "step": 1
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

    def run(self, image, api_url, api_key, model, temperature, max_tokens, top_p):
        try:
            np_image = image[0].cpu().numpy()
            np_image = (np_image * 255).clip(0, 255).astype("uint8")
            pil_image = Image.fromarray(np_image)
            buffered = BytesIO()
            pil_image.save(buffered, format="JPEG")
            encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
        except Exception as e:
            return (f"❌ 图像编码失败: {str(e)}", "", "")

        vision_prompt = (
            "根据图像内容生成三个不同方向的英文提示词，每个控制在400字符以内，"
            "请直接以如下格式返回：\n"
            "提示1: ...\n提示2: ...\n提示3: ...\n"
            "请勿返回任何额外内容，也不要提及图像分辨率或模糊词汇。"
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
            else:
                full_response = f"❌ API Error: {response.status_code} - {response.text}"

            matches = re.findall(r"(提示\d:|Prompt\s*\d:|^\d[.、])\s*(.+)", full_response, re.MULTILINE)
            response_1 = matches[0][1] if len(matches) > 0 else "❌ 提示1 解析失败"
            response_2 = matches[1][1] if len(matches) > 1 else "❌ 提示2 解析失败"
            response_3 = matches[2][1] if len(matches) > 2 else "❌ 提示3 解析失败"

            return (response_1, response_2, response_3)
        except Exception as e:
            return (f"❌ 请求失败: {str(e)}", "", "")


NODE_CLASS_MAPPINGS = {
    "VisioStarIMAGING": VisioStarIMAGING
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VisioStarIMAGING": "🖼 VisioStar 图像智能提示词 (Vision)"
}
