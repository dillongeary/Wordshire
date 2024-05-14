from enum import Enum


class Job(Enum):
    Child = 0,
    Laborer = 1,
    Farmer = 2,
    Shepard = 3,
    Miner = 4,
    Lumberjack = 5,
    Smith = 6,
    Builder = 7,
    Tailor = 8,
    Dead = 9


class Building(Enum):
    House = 0,
    Farm = 1,
    Livestock = 2


class Animal(Enum):
    Cattle = 0,
    Sheep = 1,
    Chickens = 2


class Crop(Enum):
    Wheat = 0,
    Barley = 1,
    Oats = 2,
    Cabbages = 3,
    Onions = 4,
    Beans = 5,
    Apples = 6,
    Pears = 7


class Resources(Enum):
    Food = 0,
    Wood = 1,
    Stone = 3,
    BuildingMaterials = 4,
    Ore = 5,
    Metal = 6,
    Tools = 7,
    Textiles = 8,
    Clothes = 9
