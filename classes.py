import random
from enums import *


class House:
    level = 0

    residents = []

    name = "house"

    def __init__(self, number):
        self.name = "House" + str(number)

    def levelSize(self):
        return self.level + 2

    def upgrade(self):
        self.level += 1


class Person:
    job = Job.Laborer

    age = 0
    birthday = 0
    happiness = 1.0
    hunger = 1.0

    workDelay = 0

    doneBirthday = True

    def __init__(self, age, birthday):
        self.age = age
        if age < 18:
            self.job = Job.Child
        self.birthday = birthday

    def ageUp(self, month):
        if month == self.birthday and not self.doneBirthday:
            self.doneBirthday = True
            self.age += 1
            if self.age == 18:
                self.job = Job.Laborer
            deathProbability = self.age ** 2 / 15000
            livingProbability = 1 - deathProbability
            die = random.choices(
                [True, False],
                weights=[deathProbability, livingProbability],
                k=1
            )

            return die
        elif month == (self.birthday + 1) % 12 and self.doneBirthday:
            self.doneBirthday = False

    def doHarvest(self):
        if self.workDelay == 0:
            self.workDelay = random.randint(3, 7)
            return True
        else:
            self.workDelay -= 1
            return False

    def live(self):
        self.hunger -= random.randint(0, 15) / 100
        if self.hunger < 0:
            return True, True
        elif self.hunger < 0.4:
            return True, False
        else:
            return False, False

    def eat(self):
        self.hunger += random.randint(40, 60) / 100


class Livestock:
    type = Animal.Cattle

    name = "Livestock"

    def __init__(self, species, number):
        self.type = species
        self.name = species.name + str(number)

    def harvest(self):
        output = {}
        match self.type:
            case Animal.Cattle:
                output[Resources.Food] = 4
                output[Resources.Textiles] = 1
            case Animal.Sheep:
                output[Resources.Food] = 1
                output[Resources.Textiles] = 4
            case Animal.Chickens:
                output[Resources.Food] = 2
                output[Resources.Textiles] = 2
        return output


class Field:
    type = Crop.Wheat
    name = "Field"

    def __init__(self, type, number):
        self.type = type
        self.name = type.name + str(number)

    def harvest(self):
        return {Resources.Food: 5}
