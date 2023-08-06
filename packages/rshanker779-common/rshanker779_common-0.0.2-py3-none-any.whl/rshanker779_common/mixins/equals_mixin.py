class EqualsMixin:
    def __hash__(self):
        return hash(tuple(sorted(self.__immutable_repr(self.__dict__))))

    def __immutable_repr(self, value):
        if isinstance(value, list):
            return tuple(self.__immutable_repr(i) for i in value)
        if isinstance(value, dict):
            return tuple(
                sorted(
                    (self.__immutable_repr(i), self.__immutable_repr(v))
                    for i, v in value.items()
                )
            )
        return value

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return other.__dict__ == self.__dict__
