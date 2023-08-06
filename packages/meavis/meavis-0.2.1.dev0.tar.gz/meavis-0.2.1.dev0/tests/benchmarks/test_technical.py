class ClassA:
    pass


class ClassB:
    pass


class ClassC:
    pass


class ClassD:
    pass


class ClassE:
    pass


def make_frozenset(objects):
    result = set()
    for i in range(100):
        result.add(frozenset((type(obj).__name__, i) for obj in objects))


def test_frozenset(benchmark):
    objects = [ClassA(), ClassB(), ClassC(), ClassD(), ClassE()]
    benchmark(make_frozenset, objects)


class Item:
    def __hash__(self):
        result = 0
        for value in vars(self).values():
            result ^= hash(value)
        return result

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __neq__(self, other):
        return hash(self) != hash(other)


def make_setattr(objects):
    result = set()
    for i in range(100):
        item = Item()
        for obj in objects:
            setattr(item, type(obj).__name__, i)
        result.add(item)


def test_setattr(benchmark):
    objects = [ClassA(), ClassB(), ClassC(), ClassD(), ClassE()]
    benchmark(make_setattr, objects)
