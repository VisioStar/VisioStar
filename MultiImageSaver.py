class MultiImageSaver:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_1": ("IMAGE",),
                "image_2": ("IMAGE",),
                "image_3": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("combined_images",)
    FUNCTION = "combine"
    CATEGORY = "VisioStar"

    def combine(self, image_1, image_2, image_3):
        all_images = []

        for img in [image_1, image_2, image_3]:
            if img is not None:
                all_images.extend(img)

        return (all_images,)


NODE_CLASS_MAPPINGS = {
    "MultiImageSaver": MultiImageSaver
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MultiImageSaver": "图像批次合并"
}