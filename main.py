import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from transformers import pipeline
import torch
import os
from diffusers import StableDiffusionPipeline

class ModelInfo:
    def __init__(self):
        self._info = {
            'sentiment': 'DistilBERT for sentiment analysis: Classifies text as positive/negative.',
            'image': 'CLIP for image classification: Describes or classifies images.',
            'text_to_image': 'Stable Diffusion v1-5: Generates images from text.'
        }

    def get_info(self, model_type):
        return self._info.get(model_type, 'No info available')

class BaseModel:
    def __init__(self):
        self.pipe = None

    def load(self):
        pass

    def predict(self, input_data):
        pass

class SentimentModel(BaseModel):
    def load(self):
        try:
            self.pipe = pipeline("sentiment-analysis")
        except Exception as e:
            raise Exception(f"Failed to load sentiment model: {str(e)}")

    def predict(self, text):
        if not isinstance(text, str):
            raise ValueError("Sentiment model requires text input")
        return self.pipe(text)[0]['label']

class ImageModel(BaseModel):
    def load(self):
        try:
            self.pipe = pipeline("image-classification")
        except Exception as e:
            raise Exception(f"Failed to load image model: {str(e)}")

    def predict(self, image_path):
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        return self.pipe(image_path)[0]['label']

class TextToImageModel(BaseModel):
    def load(self):
        try:
            self.pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
            self.pipe = self.pipe.to("cpu")
        except Exception as e:
            raise Exception(f"Failed to load text-to-image model: {str(e)}")

    def predict(self, text):
        if not isinstance(text, str):
            raise ValueError("Text-to-image model requires text input")
        try:
            if self.pipe:
                image = self.pipe(text).images[0]
                image.save("generated_image.png")
                return "Image generated and saved as generated_image.png"
            else:
                raise Exception("Text-to-image model not loaded")
        except Exception as e:
            raise Exception(f"Text-to-image prediction failed: {str(e)}")

class Logging:
    def log(self, message):
        print(f"Log: {message}")

class AIModel(Logging, BaseModel):
    def __init__(self, model_type):
        super().__init__()
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
            try:
                self.model_instance.load()
                self.log(f"{self.model_type} model loaded")
            except Exception as e:
                raise Exception(f"Model loading failed: {str(e)}")

    def predict(self, input_data):
        if self.model_instance:
            try:
                return self.model_instance.predict(input_data)
            except Exception as e:
                raise Exception(f"Prediction failed: {str(e)}")
        return "No model selected"

def button_click_decorator(func):
    def wrapper(self, *args, **kwargs):
        print("Button clicked!")
        return func(self, *args, **kwargs)
    return wrapper

class OOPExplainer:
    def _explain_multiple_inheritance(self):
        return "Multiple inheritance: AIModel inherits from Logging and BaseModel."

    def _explain_method_overriding(self):
        return "Method overriding: Subclasses override load() and predict() from BaseModel."

    def _explain_polymorphism(self):
        return "Polymorphism: Each model subclass uses the same predict() interface but processes inputs differently."

    def _explain_encapsulation(self):
        return "Encapsulation: ModelInfo hides _info dict; accessed via get_info()."

    def _explain_multiple_decorators(self):
        return "Multiple decorators: button_click_decorator logs button clicks."

    def get_explanations(self):
        exps = [self._explain_multiple_inheritance(),
                self._explain_method_overriding(),
                self._explain_polymorphism(),
                self._explain_encapsulation(),
                self._explain_multiple_decorators()]
        return "\n\n".join(exps)

class AIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Model GUI with OOP")
        self.model_info = ModelInfo()
        self.explainer = OOPExplainer()
        self.current_model = None
        self.input_data = None
        self.setup_ui()

    def setup_ui(self):
        ttk.Label(self.root, text="Select Input Type:").pack(pady=5)
        self.input_type = ttk.Combobox(self.root, values=['Text', 'Image'])
        self.input_type.pack()
        self.input_type.bind('<<ComboboxSelected>>', self.on_type_change)

        ttk.Button(self.root, text="Load File", command=self.load_file).pack(pady=5)

        ttk.Label(self.root, text="Select Model:").pack(pady=5)
        self.model_var = tk.StringVar(value="sentiment")
        models = [('Sentiment Analysis', 'sentiment'), ('Image Classification', 'image'), ('Text to Image', 'text_to_image')]
        for text, val in models:
            ttk.Radiobutton(self.root, text=text, variable=self.model_var, value=val, command=self.on_model_change).pack()

        self.run_btn = ttk.Button(self.root, text="Run Model", command=self._decorated_run_model)
        self.run_btn.pack(pady=10)

        ttk.Label(self.root, text="Output:").pack()
        self.output_text = scrolledtext.ScrolledText(self.root, height=5, width=50)
        self.output_text.pack(pady=5)

        ttk.Label(self.root, text="Model Info:").pack(pady=(20,5))
        self.info_text = scrolledtext.ScrolledText(self.root, height=4, width=50)
        self.info_text.pack()

        ttk.Label(self.root, text="OOP Explanations:").pack(pady=(20,5))
        self.exp_text = scrolledtext.ScrolledText(self.root, height=10, width=70)
        self.exp_text.pack()
        self.exp_text.insert(tk.END, self.explainer.get_explanations())

        self.on_model_change()

    @button_click_decorator
    def _decorated_run_model(self):
        try:
            if not self.input_data:
                messagebox.showerror("Error", "Please load an input file!")
                return
            if not self.current_model:
                messagebox.showerror("Error", "Please select a model!")
                return
            if (self.model_var.get() == 'image' and self.input_type.get() != 'Image') or \
               (self.model_var.get() in ['sentiment', 'text_to_image'] and self.input_type.get() != 'Text'):
                messagebox.showerror("Error", "Input type does not match model requirements!")
                return
            self.current_model.load()
            result = self.current_model.predict(self.input_data)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, str(result))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run model: {str(e)}")

    def on_model_change(self):
        try:
            model_type = self.model_var.get()
            self.current_model = AIModel(model_type)
            info = self.model_info.get_info(model_type)
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, info)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to switch model: {str(e)}")

    def on_type_change(self, event=None):
        self.input_data = None
        self.output_text.delete(1.0, tk.END)

    def load_file(self):
        try:
            typ = self.input_type.get()
            if typ == 'Text':
                file = filedialog.askopenfilename(filetypes=[("Text", "*.txt")])
                if file:
                    with open(file, 'r') as f:
                        self.input_data = f.read()
            elif typ == 'Image':
                file = filedialog.askopenfilename(filetypes=[("Image", "*.jpg *.png")])
                if file:
                    self.input_data = file
            else:
                messagebox.showerror("Error", "Please select an input type!")
        except FileNotFoundError:
            messagebox.showerror("Error", "Selected file not found!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = AIApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Application failed to start: {str(e)}")
