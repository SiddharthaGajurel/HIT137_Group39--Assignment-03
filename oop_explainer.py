class OOPExplainer:
    def _explain_multiple_inheritance(self):
        return "Multiple inheritance: AIModel inherits from Logging and BaseModel."

    def _explain_method_overriding(self):
        return "Subclasses override load() and predict() from BaseModel."

    def _explain_polymorphism(self):
        return "Polymorphism: predict() works differently in each subclass."

    def _explain_encapsulation(self):
        return "Encapsulation: ModelInfo hides data in a private dict."

    def _explain_multiple_decorators(self):
        return "Decorators add extra behavior to functions."

    def get_explanations(self):
        return "\n\n".join([
            self._explain_multiple_inheritance(),
            self._explain_method_overriding(),
            self._explain_polymorphism(),
            self._explain_encapsulation(),
            self._explain_multiple_decorators()
        ])
