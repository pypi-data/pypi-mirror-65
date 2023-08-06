class StringMixin:
    def __str__(self):
        return f"<{self.__class__.__name__}>({', '.join(f'{i}={v}' for i,v in self.__dict__.items())})"

    def __repr__(self):
        return str(self)
