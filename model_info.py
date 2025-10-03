class ModelInfo:
    def __init__(self):
        self._info = {
            'sentiment': 'DistilBERT for sentiment analysis.',
            'image': 'CLIP for image classification.',
            'text_to_image': 'Stable Diffusion v1-5 for text-to-image.'
        }

    def get_info(self, model_type):
        return self._info.get(model_type, 'No info available')
