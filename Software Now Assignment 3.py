import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import base64
import threading

# Mock transformers import (would be real in actual implementation)
# from transformers import pipeline

class BaseModel:
    """Base class for AI models demonstrating inheritance and encapsulation"""
    def __init__(self, model_name, category, description):
        self._model_name = model_name  # Encapsulated attribute
        self._category = category
        self._description = description
        self._model = None
        
    def load_model(self):
        """Polymorphic method to be overridden by subclasses"""
        raise NotImplementedError("Subclasses must implement load_model()")
    
    def process_input(self, input_data):
        """Polymorphic method to be overridden by subclasses"""
        raise NotImplementedError("Subclasses must implement process_input()")
    
    def get_info(self):
        """Encapsulated method to get model information"""
        return {
            "name": self._model_name,
            "category": self._category,
            "description": self._description
        }


class TextToImageModel(BaseModel):
    """Text-to-Image model demonstrating inheritance"""
    def __init__(self):
        super().__init__(
            "CompVis/stable-diffusion-v1-4", 
            "Text-to-Image", 
            "Generates images from text descriptions using diffusion model"
        )
    
    def load_model(self):
        """Method overriding - load the specific model"""
        try:
            # In a real implementation:
            # self._model = pipeline("text-to-image", model=self._model_name)
            print(f"Loaded model: {self._model_name}")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def process_input(self, text_input):
        """Method overriding - process text to generate image"""
        try:
            # Simulate processing delay
            # In a real implementation:
            # result = self._model(text_input)
            # return result.images[0]
            
            # For demo purposes, return a placeholder image
            print(f"Processing text: {text_input}")
            return self._generate_placeholder_image(text_input)
        except Exception as e:
            print(f"Error processing input: {e}")
            return None
    
    def _generate_placeholder_image(self, text):
        """Generate a placeholder image for demo purposes"""
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new('RGB', (256, 256), color=(73, 109, 137))
        d = ImageDraw.Draw(img)
        
        # Try to use a default font
        try:
            font = ImageFont.load_default()
        except:
            font = None
            
        # Add text to image
        text = text[:20] + "..." if len(text) > 20 else text
        d.text((10, 10), f"Generated from:\n{text}", fill=(255, 255, 255), font=font)
        return img


class TextClassificationModel(BaseModel):
    """Text Classification model demonstrating inheritance"""
    def __init__(self):
        super().__init__(
            "distilbert-base-uncased-finetuned-sst-2-english", 
            "Text Classification", 
            "Classifies text into positive/negative sentiments"
        )
    
    def load_model(self):
        """Method overriding - load the specific model"""
        try:
            # In a real implementation:
            # self._model = pipeline("sentiment-analysis", model=self._model_name)
            print(f"Loaded model: {self._model_name}")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def process_input(self, text_input):
        """Method overriding - process text classification"""
        try:
            # Simulate processing
            # In a real implementation:
            # result = self._model(text_input)
            # return result[0]
            
            print(f"Classifying text: {text_input}")
            # Simulate sentiment analysis
            positive_keywords = ['good', 'great', 'awesome', 'excellent', 'love', 'like']
            negative_keywords = ['bad', 'terrible', 'awful', 'hate', 'dislike']
            
            score = 0
            words = text_input.lower().split()
            for word in words:
                if word in positive_keywords:
                    score += 1
                elif word in negative_keywords:
                    score -= 1
            
            label = "POSITIVE" if score > 0 else "NEGATIVE" if score < 0 else "NEUTRAL"
            confidence = min(0.99, abs(score) / 10 + 0.5)
            
            return {"label": label, "score": confidence}
        except Exception as e:
            print(f"Error processing input: {e}")
            return None


class ModelLoader:
    """Utility class for loading models - demonstrates composition"""
    @staticmethod
    def load_model_by_type(model_type):
        if model_type == "text-to-image":
            return TextToImageModel()
        elif model_type == "text-classification":
            return TextClassificationModel()
        else:
            raise ValueError(f"Unknown model type: {model_type}")


# Multiple decorators example
def log_execution(func):
    """Decorator to log function execution"""
    def wrapper(*args, **kwargs):
        print(f"Executing {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


def handle_errors(func):
    """Decorator to handle errors gracefully"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error in {func.__name__}: {e}")
            return None
    return wrapper


class AIGUI(tk.Tk):
    """Main GUI class demonstrating OOP concepts"""
    def __init__(self):
        super().__init__()
        self.title("AI Model Integration GUI")
        self.geometry("1000x700")
        self.resizable(True, True)
        
        # Available models
        self.models = {
            "text-to-image": TextToImageModel(),
            "text-classification": TextClassificationModel()
        }
        
        self.current_model = None
        self.output_image = None
        
        self._create_widgets()
        self._layout_widgets()
        
    def _create_widgets(self):
        """Create all GUI widgets - demonstrates encapsulation"""
        # Menu bar
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)
        
        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Exit", command=self.quit)
        
        # Models menu
        self.models_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Models", menu=self.models_menu)
        self.models_menu.add_command(label="Load Text-to-Image", 
                                   command=lambda: self.load_model("text-to-image"))
        self.models_menu.add_command(label="Load Text Classification", 
                                   command=lambda: self.load_model("text-classification"))
        
        # Help menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_about)
        
        # Main frames
        self.top_frame = ttk.Frame(self, padding="10")
        self.middle_frame = ttk.Frame(self, padding="10")
        self.bottom_frame = ttk.Frame(self, padding="10")
        
        # Model selection
        self.model_label = ttk.Label(self.top_frame, text="Select Model:")
        self.model_var = tk.StringVar()
        self.model_combo = ttk.Combobox(
            self.top_frame, 
            textvariable=self.model_var,
            values=list(self.models.keys()),
            state="readonly"
        )
        self.model_combo.bind("<<ComboboxSelected>>", self.on_model_selected)
        
        self.load_btn = ttk.Button(
            self.top_frame, 
            text="Load Model", 
            command=self.on_load_model
        )
        
        # Input section
        self.input_label = ttk.Label(self.middle_frame, text="Input Text:")
        self.input_text = scrolledtext.ScrolledText(self.middle_frame, height=5, width=50)
        
        self.process_btn = ttk.Button(
            self.middle_frame, 
            text="Process Input", 
            command=self.on_process_input
        )
        
        # Output section
        self.output_label = ttk.Label(self.middle_frame, text="Output:")
        self.output_text = scrolledtext.ScrolledText(self.middle_frame, height=5, width=50)
        self.output_text.config(state=tk.DISABLED)
        
        self.image_label = ttk.Label(self.middle_frame, text="Generated Image:")
        self.image_display = ttk.Label(self.middle_frame, background="white", 
                                      text="Image will appear here")
        
        # Info section
        self.info_notebook = ttk.Notebook(self.bottom_frame)
        
        self.model_info_frame = ttk.Frame(self.info_notebook, padding="10")
        self.oop_info_frame = ttk.Frame(self.info_notebook, padding="10")
        
        self.info_notebook.add(self.model_info_frame, text="Model Information")
        self.info_notebook.add(self.oop_info_frame, text="OOP Concepts")
        
        # Model info
        self.model_info_text = scrolledtext.ScrolledText(self.model_info_frame, height=10)
        self.model_info_text.insert(tk.END, "Select a model to see information")
        self.model_info_text.config(state=tk.DISABLED)
        
        # OOP concepts info
        self.oop_info_text = scrolledtext.ScrolledText(self.oop_info_frame, height=10)
        oop_info = """
        OOP Concepts Used in This Application:
        
        1. Inheritance:
           - TextToImageModel and TextClassificationModel inherit from BaseModel
           - This allows code reuse and polymorphic behavior
        
        2. Encapsulation:
           - Model attributes are private (prefixed with _)
           - Public methods provide controlled access to functionality
        
        3. Polymorphism:
           - Both model types implement load_model() and process_input()
           - The GUI can interact with any model without knowing its specific type
        
        4. Method Overriding:
           - Each model overrides the base class methods to provide specific implementations
        
        5. Multiple Decorators:
           - @log_execution and @handle_errors are applied to methods
           - This adds functionality without modifying the original methods
        """
        self.oop_info_text.insert(tk.END, oop_info)
        self.oop_info_text.config(state=tk.DISABLED)
    
    def _layout_widgets(self):
        """Layout all GUI widgets"""
        self.top_frame.pack(fill=tk.X)
        self.middle_frame.pack(fill=tk.BOTH, expand=True)
        self.bottom_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top frame layout
        self.model_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.model_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.load_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # Middle frame layout
        self.input_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.input_text.grid(row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
        
        self.process_btn.grid(row=2, column=0, padx=5, pady=5)
        
        self.output_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.output_text.grid(row=1, column=1, padx=5, pady=5, sticky=tk.NSEW)
        
        self.image_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.image_display.grid(row=4, column=0, padx=5, pady=5, sticky=tk.NSEW)
        
        # Configure grid weights for resizing
        self.middle_frame.grid_columnconfigure(0, weight=1)
        self.middle_frame.grid_columnconfigure(1, weight=1)
        self.middle_frame.grid_rowconfigure(1, weight=1)
        self.middle_frame.grid_rowconfigure(4, weight=1)
        
        # Bottom frame layout
        self.info_notebook.pack(fill=tk.BOTH, expand=True)
        self.model_info_text.pack(fill=tk.BOTH, expand=True)
        self.oop_info_text.pack(fill=tk.BOTH, expand=True)
    
    @log_execution
    @handle_errors
    def load_model(self, model_type):
        """Load the selected model"""
        self.model_var.set(model_type)
        self.on_load_model()
    
    def on_model_selected(self, event):
        """Handle model selection from dropdown"""
        model_type = self.model_var.get()
        if model_type in self.models:
            self.current_model = self.models[model_type]
            self.update_model_info()
    
    @log_execution
    @handle_errors
    def on_load_model(self):
        """Handle load model button click"""
        model_type = self.model_var.get()
        if not model_type:
            messagebox.showerror("Error", "Please select a model type first")
            return
        
        if model_type in self.models:
            self.current_model = self.models[model_type]
            # Run model loading in a separate thread to avoid GUI freezing
            threading.Thread(target=self._load_model_thread).start()
        else:
            messagebox.showerror("Error", f"Unknown model type: {model_type}")
    
    def _load_model_thread(self):
        """Thread function for loading model"""
        self.process_btn.config(state=tk.DISABLED)
        success = self.current_model.load_model()
        if success:
            messagebox.showinfo("Success", f"Model {self.current_model._model_name} loaded successfully")
            self.process_btn.config(state=tk.NORMAL)
            self.update_model_info()
        else:
            messagebox.showerror("Error", "Failed to load model")
    
    def update_model_info(self):
        """Update model information display"""
        if self.current_model:
            info = self.current_model.get_info()
            self.model_info_text.config(state=tk.NORMAL)
            self.model_info_text.delete(1.0, tk.END)
            self.model_info_text.insert(tk.END, 
                                      f"Model Name: {info['name']}\n"
                                      f"Category: {info['category']}\n"
                                      f"Description: {info['description']}")
            self.model_info_text.config(state=tk.DISABLED)
    
    @log_execution
    @handle_errors
    def on_process_input(self):
        """Handle process input button click"""
        if not self.current_model:
            messagebox.showerror("Error", "Please load a model first")
            return
        
        input_data = self.input_text.get(1.0, tk.END).strip()
        if not input_data:
            messagebox.showerror("Error", "Please enter some input text")
            return
        
        # Run processing in a separate thread to avoid GUI freezing
        threading.Thread(target=self._process_input_thread, args=(input_data,)).start()
    
    def _process_input_thread(self, input_data):
        """Thread function for processing input"""
        self.process_btn.config(state=tk.DISABLED)
        result = self.current_model.process_input(input_data)
        
        # Update GUI in the main thread
        self.after(0, self._update_output, result, input_data)
        self.process_btn.config(state=tk.NORMAL)
    
    def _update_output(self, result, input_data):
        """Update output display with results"""
        if isinstance(result, Image.Image):
            # Display image
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Generated image from: {input_data}")
            self.output_text.config(state=tk.DISABLED)
            
            # Display image
            result.thumbnail((300, 300))
            self.output_image = ImageTk.PhotoImage(result)
            self.image_display.config(image=self.output_image)
        elif isinstance(result, dict):
            # Display text result
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Result: {result}")
            self.output_text.config(state=tk.DISABLED)
            
            # Clear image display
            self.image_display.config(image='')
        else:
            messagebox.showerror("Error", "Failed to process input")
    
    def show_about(self):
        """Show about information"""
        about_text = (
            "AI Model Integration GUI\n\n"
            "This application demonstrates integration of Hugging Face models\n"
            "using Object-Oriented Programming concepts in Python with Tkinter.\n\n"
            "Features:\n"
            "- Text-to-Image generation\n"
            "- Text classification\n"
            "- OOP concepts demonstration"
        )
        messagebox.showinfo("About", about_text)


if __name__ == "__main__":
    app = AIGUI()
    app.mainloop()