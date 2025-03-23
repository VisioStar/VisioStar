# 让 ComfyUI 识别 VisioStar 目录下所有节点
from .product_selector import ProductSelector
from .MultiImageSaver import MultiImageSaver
from .deepseek import DeepSeekNode
from .VisioStarCHATgpt import GPTNode
from .VisioStardeepseekPRO import VisioStardeepseekPRO
from .VisioStarGPTPRO import VisioStarGPTPRO
from .VisioStarIMAGING import VisioStarIMAGING  # 图像多提示词节点
from .VisioStarVISIONSinglePrompt import VisioStarVISIONSinglePrompt  # ✅ 新增单提示词节点

NODE_CLASS_MAPPINGS = {
    "Product Selector": ProductSelector,
    "MultiImageSaver": MultiImageSaver,
    "DeepSeekNode": DeepSeekNode,
    "GPTNode": GPTNode,
    "VisioStardeepseekPRO": VisioStardeepseekPRO,
    "VisioStarGPTPRO": VisioStarGPTPRO,
    "VisioStarIMAGING": VisioStarIMAGING,
    "VisioStarVISIONSinglePrompt": VisioStarVISIONSinglePrompt,  # ✅ 注册新节点
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Product Selector": "🛒 产品选择器",
    "MultiImageSaver": "🖼 保存多个图像",
    "DeepSeekNode": "☆VisioStar Deepseek API",
    "GPTNode": "GPT API Node",
    "VisioStardeepseekPRO": "VisioStar DeepSeek PRO",
    "VisioStarGPTPRO": "🤖 VisioStar GPT PRO",
    "VisioStarIMAGING": "🖼 VisioStar 图像智能提示词",
    "VisioStarVISIONSinglePrompt": "🖼 VisioStar 单提示词生成 (Vision)",  # ✅ UI 显示名称
}
