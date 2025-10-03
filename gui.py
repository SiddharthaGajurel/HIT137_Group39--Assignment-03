import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from model_info import ModelInfo
from oop_explainer import OOPExplainer
from ai_model import AIModel
from decorators import button_click_decorator

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
        model_type = self.model_var.get()
        self.current_model = AIModel(model_type)
        info = self.model_info.get_info(model_type)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, info)

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
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")
