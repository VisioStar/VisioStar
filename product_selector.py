import os
import json
from typing import Tuple

class ProductSelector:
    """
    ComfyUI 产品选择器
    让用户通过 **更美观的 UI（下拉单选）** 选择产品，并自动加载 JSON 文件中的提示词
    """

    @classmethod
    def INPUT_TYPES(cls):
        # 读取 JSON 目录
        products_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "products"))
        file_path = os.path.join(products_dir, "product_prompts.json")

        # 读取 JSON 文件，获取所有产品名称
        products = []
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                product_data = json.load(f)
                products = [item["name"] for item in product_data if "name" in item and "prompt" in item]

        # 确保至少有一个选项，否则 UI 可能崩溃
        if not products:
            products = ["未找到产品"]

        return {
            "required": {
                "product": (products, {"default": products[0], "widget": "dropdown"})  # **使用 dropdown 替代 radio**
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    CATEGORY = "VisioStar"
    FUNCTION = "run"

    def run(self, product: str) -> Tuple[str]:
        """ 读取 JSON 里的产品提示词 """
        products_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "products"))
        file_path = os.path.join(products_dir, "product_prompts.json")

        if not os.path.exists(file_path):
            print(f"⚠️ [ProductSelector] JSON 文件未找到: {file_path}")
            return ("",)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                product_data = json.load(f)

            # 查找匹配的产品提示词
            prompt = next((item["prompt"] for item in product_data if item["name"] == product), "")
            return (prompt,)
        except Exception as e:
            print(f"❌ [ProductSelector] 读取 JSON 出错: {e}")
            return ("",)
