from models import SentimentModel, ImageModel, TextToImageModel

class Logging:
    def log(self, message):
        print(f"Log: {message}")

class AIModel(Logging):
    def __init__(self, model_type):
        self.model_type = model_type
        self.model_instance = self._create_model(model_type)

    def _create_model(self, typ):
        if typ == 'sentiment':
            return SentimentModel()
        elif typ == 'image':
            return ImageModel()
        elif typ == 'text_to_image':
            return TextToImageModel()
        return None

    def load(self):
        if self.model_instance:
            self.model_instance.load()
            self.log(f"{self.model_type} model loaded")

    def predict(self, input_data):
        if self.model_instance:
            return self.model_instance.predict(input_data)
        return "No model selected"
