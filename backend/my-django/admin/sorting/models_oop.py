from dataclasses import dataclass

@dataclass
class Calculator(object):

    num1 = int
    num2 = int

    @property
    def num1(self)-> int: return self._num1
    @num1.setter
    def num1(self, num1): self._num1 = num1
    @property
    def num2(self) -> int: return self._num2
    @num1.setter
    def num2(self, num2): self._num2 = num2

    def add(self):
        return self.num1 + self.num2
    def subtract(self):
        return self.num1 - self.num2
    def mulitple(self):
        return self.num1 * self.num2
    def divice(self):
        return self.num2 / self.num2


@dataclass
class Contacts(object):

        def __init__(self, name, phone, email, address):
            self.name = name
            self.phone = phone
            self.email = email
            self.address = address

        def to_string(self):
            print(f'\n[InFor]\nname: {self.name} \nphone: {self.phone}\nemail: {self.email}\naddress: {self.address}')

        @staticmethod
        def set_contact(name, phone, email, address) -> object:
            return Contacts(name, phone, email, address)

        @staticmethod
        def get_contact(ls):
            for i in ls:
                i.to_string()
            return ls

        @staticmethod
        def del_contact(ls, name):
            for i, j in enumerate(ls):
                if name == j.name:
                    del ls[i]
            return ls



@dataclass
class Grade(object):
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def __init__(self, name, kor, eng, math):
        self.name = name
        self.kor = kor
        self.eng = eng
        self.math = math

    def sum(self):
        return self.kor + self.eng + self.math

    def avg(self):
        return self.sum() / 3

    def return_grade(self) -> str:
        aver = self.avg()
        if aver >= 90:
            return 'A'
        elif aver >= 80:
            return 'B'
        elif aver >= 70:
            return 'C'
        elif aver >= 60:
            return 'D'
        elif aver >= 50:
            return 'E'
        else:
            return 'F'















