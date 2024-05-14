import random
from datetime import datetime
from tkinter import *
import sched, time

from classes import *
from commands import *


class Game:
    population = {
        Job.Child: [],
        Job.Laborer: [],
        Job.Farmer: [],
        Job.Shepard: [],
        Job.Miner: [],
        Job.Lumberjack: [],
        Job.Smith: [],
        Job.Builder: [],
        Job.Tailor: []
    }

    timeDelta = 0

    houses = []
    farms = []
    livestock = []

    paused = False

    inventory = {
        Resources.Food: 50,
        Resources.Wood: 50,
        Resources.Stone: 0,
        Resources.BuildingMaterials: 0,
        Resources.Metal: 0,
        Resources.Tools: 1,
        Resources.Textiles: 0,
        Resources.Clothes: 0
    }

    outputBuffer = []

    def endGame(self):
        self.outputBuffer.append("***YOU LOOSE***")

    def pausePlay(self, buttonVariable):
        if self.paused:
            buttonVariable.set("►")
            self.paused = False
            pauseButton.config(background="light gray")
        else:
            buttonVariable.set("||")
            pauseButton.config(background="gray")
            self.paused = True

    def getPopulation(self):
        count = 0
        for list in self.population.values():
            count += len(list)
        return count

    def getAdultPopulation(self):
        return self.getPopulation() - len(self.population[Job.Child])

    def getPopulationLimit(self):
        count = 0
        for house in self.houses:
            count += house.levelSize()
        return count

    def __init__(self):
        self.startDate = datetime.now()

        self.houses.append(House(0))
        self.houses.append(House(1))
        self.houses.append(House(2))

        self.population[Job.Laborer].append(Person(random.randint(18, 48), random.randint(0, 12)))
        self.population[Job.Laborer].append(Person(random.randint(18, 48), random.randint(0, 12)))
        self.population[Job.Laborer].append(Person(random.randint(18, 48), random.randint(0, 12)))
        self.population[Job.Laborer].append(Person(random.randint(18, 48), random.randint(0, 12)))

    def getDate(self):
        self.timeDelta += 1
        daysdelta = int(self.timeDelta) // 20
        year = 1000 + daysdelta // 12
        month = daysdelta % 12
        season = month // 3
        seasonModifier = month % 3
        return seasonTime[seasonModifier] + seasons[season] + " " + str(year)

    def getMonth(self):
        daysdelta = int(self.timeDelta) // 20
        return daysdelta % 12

    def build(self, building, *args):
        if len(self.population[Job.Builder]) > 0:
            if self.inventory[Resources.Wood] >= 50:
                buildingName = ""
                match building:
                    case Building.House:
                        constructed = House(len(self.houses))
                        self.houses.append(constructed)
                        buildingName = constructed.name
                    case Building.Farm:
                        constructed = Field(args[0], len(self.farms))
                        self.farms.append(constructed)
                        buildingName = constructed.name
                    case Building.Livestock:
                        constructed = Livestock(args[0], len(self.livestock))
                        self.livestock.append(constructed)
                        buildingName = constructed.name
                self.inventory[Resources.Wood] -= 50
                self.outputBuffer.append(f"{buildingName} Constructed")
            else:
                self.outputBuffer.append("Not Enough Wood")
        else:
            self.outputBuffer.append("No Builders Available")

    def upgrade(self, house):
        match house.level:
            case 0:
                resourceCheck = Resources.Stone
            case 1:
                resourceCheck = Resources.BuildingMaterials
            case _:
                return False
        if self.inventory[resourceCheck] >= 50:
            self.houses.remove(house)
            house.upgrade()
            self.houses.append(house)
            self.inventory[resourceCheck] -= 50
        else:
            return False

    def addToInventory(self, stuff):
        for key, value in stuff.items():
            if key in self.inventory.keys():
                if value > 0:
                    self.outputBuffer.append(f"Collected {value} {key.name}")
                    self.inventory[key] += value
            else:
                print("BUG : RESOURCE NOT IN INVENTORY")

    def timestep(self):
        if len([person for job in self.population.values() for person in job]) == 0:
            self.endGame()
            return
        availableTools = self.inventory[Resources.Tools]
        enoughTools = False
        for key, value in self.population.items():
            match key:
                case Job.Farmer:
                    for farmer, farm in zip(value, self.farms):
                        if farmer.doHarvest():
                            self.addToInventory(farm.harvest())
                case Job.Shepard:
                    for shepard, livestock in zip(value, self.livestock):
                        if shepard.doHarvest():
                            self.addToInventory(livestock.harvest())
                case Job.Miner:
                    for miner in value:
                        if availableTools > 0:
                            availableTools -= 1
                            if miner.doHarvest():
                                self.addToInventory({Resources.Stone: 5,
                                                     Resources.Metal: random.choices(
                                                         [0, 1, 2],
                                                         weights=[0.75, 0.2, 0.05],
                                                         k=1
                                                     )[0]})
                        else:
                            if not enoughTools:
                                print("Not Enough Tools")
                                enoughTools = False
                case Job.Lumberjack:
                    for jack in value:
                        if availableTools > 0:
                            availableTools -= 1
                            if jack.doHarvest():
                                self.addToInventory({Resources.Wood: 5})
                        else:
                            if not enoughTools:
                                print("Not Enough Tools")
                                enoughTools = False
                case Job.Smith:
                    for _ in value:
                        if self.inventory[Resources.Metal] >= 15:
                            self.inventory[Resources.Metal] -= 15
                            self.inventory[Resources.Tools] += 1
                case Job.Tailor:
                    for _ in value:
                        if self.inventory[Resources.Textiles] >= 25:
                            self.inventory[Resources.Textiles] -= 25
                            self.inventory[Resources.Clothes] += 1
                # case Job.Builder:
                #     for _ in value:
                #         if self.inventory[Resources.Wood] >= 15 & self.inventory[Resources.Stone] >= 15:
                #             self.inventory[Resources.Wood] -= 15
                #             self.inventory[Resources.Stone] -= 15
                #             self.inventory[Resources.BuildingMaterials] += 1
        if self.getPopulationLimit() > self.getPopulation() & self.getAdultPopulation() >= 2:
            if random.choices([True, False], weights=[0.05, 0.95], k=1)[0]:
                self.outputBuffer.append("A new child was born!")
                self.population[Job.Child].append(Person(0, self.getMonth()))
        deadPeople = []
        for person in [person for job in self.population.values() for person in job]:
            diedAge = person.ageUp(self.getMonth())
            needsFood, diedFood = person.live()
            if diedAge:
                self.outputBuffer.append("Some Died of Old Age")
                deadPeople.append(person)
            elif diedFood:
                self.outputBuffer.append("Someone Starved to Death")
                deadPeople.append(person)
            elif needsFood:
                if self.inventory[Resources.Food] > 0:
                    self.inventory[Resources.Food] -= 1
                    person.eat()
        for person in deadPeople:
            personsJob = person.job
            self.population[personsJob].remove(person)

    def moveWorked(self, fjob, tjob):
        if fjob == Job.Child:
            self.outputBuffer.append("Cant Assign Job to Child")
            return False
        elif tjob == Job.Child:
            self.outputBuffer.append("Cant Assign Job of Child to Adult")
            return False
        try:
            person = self.population[fjob].pop()
            self.population[tjob].append(person)
            self.outputBuffer.append(f"{fjob.name} reasigned to {tjob.name}")
            return True
        except:
            self.outputBuffer.append(f"No {fjob.name}s to reassign")
            return False

    def printResources(self):
        size = max(list(map(lambda x: len(str(x)), self.inventory.values())))
        string = ""
        for key, value in self.inventory.items():
            change = size - len(str(value))

            string += ((' ' * change) + str(value) + " " + key.name + "\n")
        return string

    def printPopulation(self):
        size = max(list(map(lambda x: len(str(len(x))), self.population.values())))
        string = ""
        for key, value in self.population.items():
            amount = len(value)
            change = size - len(str(amount))
            string += (' ' * change) + str(amount) + ' ' + key.name + "\n"
        return string

    def printBuildings(self):
        houseAmount = [0, 0, 0]
        for house in self.houses:
            houseAmount[house.level] += 1
        return f"{houseAmount[0]} Small House\n{houseAmount[1]} Medium House\n{houseAmount[2]} Large House\n{len(self.farms)} Farms\n{len(self.livestock)} Livestock"

    def getOutputBuffer(self):
        temp = self.outputBuffer.copy()
        self.outputBuffer = []
        return temp

    def input(self, str):
        inputString = str.get()
        str.set("")
        commands = inputString.split(" ")
        match commands[0]:
            case "assign":
                if len(commands) > 2:
                    self.moveWorked(jobs[commands[1]], jobs[commands[2]])
                else:
                    self.moveWorked(Job.Laborer, jobs[commands[1]])
            case "build":
                match building[commands[1]]:
                    case Building.House:
                        self.build(Building.House)
                    case Building.Farm:
                        self.build(Building.Farm, crops[commands[2]])
                    case Building.Livestock:
                        self.build(Building.Livestock, animals[commands[2]])
            case "upgrade":
                level = int(commands[1]) - 1
                if level == 2:
                    self.outputBuffer.append(f"Cannot Upgrade Level 3 Houses")
                    return
                for house in self.houses:
                    if house.level == level:
                        self.upgrade(house)
                        return
                self.outputBuffer.append(f"No Level {level + 1} House To Upgrade")
            case "info":
                try:
                    self.outputBuffer.append(f"{infos[commands[1]]}")
                except:
                    self.outputBuffer.append(f"{commands[1]} is not a Valid Info Category.")


root = Tk()
root.title("Wordshire")

inputCommand = StringVar()
infoVariable = StringVar()
dateVariable = StringVar()
outputVariable = StringVar()
pauseVariable = StringVar()

pauseVariable.set("►")
outputVariable.set(
    "**WELCOME TO WORDSHIRE**\n\nThis game uses text commands to control villagers in your village, can you keep "
    "everyone alive and grow Wordshire into a prospering town!\n\n**GUI**\n\nThis pane will give you updates into whats "
    "happening on your town.\nThe pane to your left will show you an overview of your town, including the population "
    "and resources.\n The pane at the top will show the current date.\nThe text input at the botton is where you "
    "supply commands!\n\n**Commands**\n\n`assign <worker> <worker>`\nThis command reasigns a villager from the first "
    "job to the second \n\n`build <type> <subtype>`\nBuild a new building in your village. The type can be 'house',"
    "'farm' or 'livestock'.\n\n'upgrade <level>'\nUpdate a House of the inputed level. Valid levels are '1' and '2'\n\n'info <category>'\nGives information about a command or part of the game.\n\n")

info = Label(root, textvariable=infoVariable, height=30, width=20, anchor="nw", justify="left",
             font=("TkFixedFont",))
info.grid(row=1, column=0)

dateTime = Label(root, textvariable=dateVariable).grid(row=0, column=1)

pauseButton = Button(root, textvariable=pauseVariable, command=lambda: game.pausePlay(pauseVariable))
pauseButton.grid(row=0, column=2)

output = Label(root, textvariable=outputVariable, height=30, width=80, anchor="sw", justify="left", wraplength=600,
               font=("TkFixedFont",))
output.grid(row=1, column=1, columnspan=2)
inputEntry = Entry(root, width=90, textvariable=inputCommand)
inputEntry.grid(row=2, columnspan=2)
inputEntry.bind("<Return>", lambda _: game.input(inputCommand))

Scrollbar(output)

Button(root, width=10, text="Submit", command=lambda: game.input(inputCommand)).grid(row=2, column=2)

game = Game()


def logic_loop(scheduler):
    scheduler.enter(1, 1, logic_loop, (scheduler,))
    if not game.paused:
        game.timestep()
        infoVariable.set(
            "Resources:\n" + game.printResources() + "\nPopulation:\n" + game.printPopulation() + "\nBuildings\n" + game.printBuildings())
        dateVariable.set(game.getDate())
    root.update()


def ui_loop(scheduler):
    scheduler.enter(0.05, 1, ui_loop, (scheduler,))
    outputBuffer = game.getOutputBuffer()
    if outputBuffer:
        outputVariable.set(outputVariable.get() + "\n" + "\n".join(outputBuffer))
    root.update()


my_scheduler = sched.scheduler(time.time, time.sleep)
my_scheduler.enter(1, 1, logic_loop, (my_scheduler,))
my_scheduler.enter(0.05, 1, ui_loop, (my_scheduler,))
my_scheduler.run()
