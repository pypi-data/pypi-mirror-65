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

    def __lt__(self, other):
        return self.__value < other.__value

    def __eq__(self, value):
        if len(self.__value) != len(value.__value):
            return False

        for x, y in zip(self.__value, value.__value):
            if x != y:
                return False

        return True

    def __add__(self, other):
        return Value(*self.__value, *other.__value)

    def __lshift__(self, other):
        return Value(*self.__value, other)

    def __rshift__(self, other):
        return Value(*[v for v in self.__value if v != other])
