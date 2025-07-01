import requests
import hashlib
import random

class VisioStarTranslate:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "请输入需要翻译的文本，或左侧接入字符串节点"
                }),
            },
            "optional": {
                "api_type": (["baidu"], {"default": "baidu"}),
                "from_translate": (["auto", "zh", "en"], {"default": "zh"}),
                "to_translate": (["zh", "en"], {"default": "en"}),
                "baidu_appid": ("STRING", {"multiline": False, "default": ""}),
                "baidu_key": ("STRING", {"multiline": False, "default": ""})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("translated_text",)
    FUNCTION = "translate"
    CATEGORY = "VisioStar"

    def translate(self, text, api_type="baidu", from_translate="zh", to_translate="en", baidu_appid="", baidu_key=""):
        if not text or not text.strip():
            return ("[ERROR] Please enter text to translate.",)

        if api_type == "baidu":
            if not baidu_appid or not baidu_key:
                return ("[ERROR] Please provide both Baidu App ID and Key.",)

            salt = str(random.randint(32768, 65536))
            sign_str = baidu_appid + text + salt + baidu_key
            sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
            url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
            params = {
                "q": text,
                "from": from_translate,
                "to": to_translate,
                "appid": baidu_appid,
                "salt": salt,
                "sign": sign
            }
            try:
                response = requests.get(url, params=params, timeout=10)
                result = response.json()
                if "trans_result" in result:
                    return (result["trans_result"][0]["dst"],)
                elif "error_msg" in result:
                    return (f"[ERROR] Baidu API: {result['error_msg']}",)
                else:
                    return ("[ERROR] Unknown response format from Baidu API.",)
            except Exception as e:
                return (f"[ERROR] Exception occurred: {str(e)}",)
        else:
            return ("[ERROR] Only Baidu API is supported for now.",)

NODE_CLASS_MAPPINGS = {
    "VisioStarTranslate": VisioStarTranslate,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VisioStarTranslate": "VisioStar Translate",
}
