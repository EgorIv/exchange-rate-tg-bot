class Currency:
    def __init__(self, char_code, name, value):
        self.char_code = char_code
        self.name = name
        self.value = value

    def show_currency(self):
        return f"{self.char_code}\n{self.name}\n{round(float(self.value), 2)} ₽"