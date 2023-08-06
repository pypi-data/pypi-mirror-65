class Value:
    def __init__(self, *args):
        args = set(args)
        args = list(args)
        args.sort()
        self.__value = args

    def __str__(self):
        return self.__value.__str__()

    def __repr__(self):
        return self.__value.__repr__()

    def __iter__(self):
        return self.__value.__iter__()

    def __hash__(self):
        return hash(self.__repr__())

    def __bool__(self):
        return len(self.__value) > 0

    def __lt__(self, other):
        return Value(Value()) if self.__value < other.__value else Value()

    def __eq__(self, value):
        if len(self.__value) != len(value.__value):
            return Value()

        for x, y in zip(self.__value, value.__value):
            if x != y:
                return Value()

        return Value(Value())

    def __add__(self, other):
        return Value(*self.__value, other)

    def __sub__(self, other):
        return Value(*[v for v in self.__value if v != other])

    def __mod__(self, other):
        return Value(*[v for v in self.__value if v not in other])

    def __and__(self, other):
        return Value(*[v for v in self.__value if v in other])

    def __or__(self, other):
        return Value(*self.__value, *other.__value)
