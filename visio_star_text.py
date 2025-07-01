class VisioStarText:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "输入或粘贴你的文本，可以作为字符串输出接入其他节点"
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "output"
    CATEGORY = "VisioStar"  # 可以自定义分组显示为 VisioStar

    def output(self, text):
        return (text,)

NODE_CLASS_MAPPINGS = {
    "VisioStarText": VisioStarText,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VisioStarText": "VisioStar Text",
}
