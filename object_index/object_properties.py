def name(self) -> str:
    """
    GET THE NAMe name naame name

    """
    return self._name


@property
def ageP(self):
    """
    Get THE AGE.AGE AGE AGE
    """
    return self._age


class Person:
    def __init__(self, name, age):
        self._name = name
        self._age = age
        self.age = ageP

    @property
    def face(self):
        """GET THE FACE!"""
        return "FACE"

    def case(self):
        """GET THE CASE"""
        return "CASE"

    case = property(case)

    name = property(name)


class House:
    def __init__(self, name):
        self._name = name

        self.name = name


bob = Person('bob', 5)
cat = Person('cat', 85)
home = House('my home')
other = House('Some other home')

print(bob.age)

bob.name
