def button_click_decorator(func):
    def wrapper(self, *args, **kwargs):
        print("Button clicked!")
        return func(self, *args, **kwargs)
    return wrapper
