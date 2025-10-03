import os
from transformers import pipeline
from diffusers import StableDiffusionPipeline

class BaseModel:
    def __init__(self):
        self.pipe = None

    def load(self):
        pass

    def predict(self, input_data):
        pass

class SentimentModel(BaseModel):
    def load(self):
        self.pipe = pipeline("sentiment-analysis")

    def predict(self, text):
        if not isinstance(text, str):
            raise ValueError("Sentiment model requires text input")
        return self.pipe(text)[0]['label']

class ImageModel(BaseModel):
    def load(self):
        self.pipe = pipeline("image-classification")

    def predict(self, image_path):
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        return self.pipe(image_path)[0]['label']

class TextToImageModel(BaseModel):
    def load(self):
        self.pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
        self.pipe = self.pipe.to("cpu")

    def predict(self, text):
        if not isinstance(text, str):
            raise ValueError("Text-to-image model requires text input")
        image = self.pipe(text).images[0]
        image.save("generated_image.png")
        return "Image generated and saved as generated_image.png"
