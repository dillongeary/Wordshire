from enums import *

jobs = {
    "child": Job.Child,
    "laborer": Job.Laborer,
    "lumberjack": Job.Lumberjack,
    "miner": Job.Miner,
    "farmer": Job.Farmer,
    "shephard": Job.Shepard,
    "smith": Job.Smith,
    "builder": Job.Builder,
    "tailor": Job.Tailor
}

building = {
    "house": Building.House,
    "farm": Building.Farm,
    "livestock": Building.Livestock
}

animals = {
    "cow": Animal.Cattle,
    "sheep": Animal.Sheep,
    "chickens": Animal.Chickens
}

crops = {
    "wheat": Crop.Wheat,
    "barley": Crop.Barley,
    "oat": Crop.Oats,
    "cabbage": Crop.Cabbages,
    "onion": Crop.Onions,
    "beans": Crop.Beans,
    "apple": Crop.Apples,
    "pears": Crop.Pears
}

seasons = {
    0: "Spring",
    1: "Summer",
    2: "Autumn",
    3: "Winter"
}

seasonTime = {
    0: "Early ",
    1: "",
    2: "Late "
}

infos = {
    "buildings": "\nThere are three buildings in the game. These are Houses, Farms and Livestock (ik livestock isnt a building but 'pen' sounded weird). Each building requires 50 wood to builds, and upgradable building require 50 stone for the first upgrade, and 50 building materials for the second. Houses home residents, starting off with a capacity of 2 and increasing by 1 for each upgrade level (to a max of 4 residents). Farms employ 1 farmer, and when worked will producde 5 food per harvest. Livestock emply 1 shepard, and when worked will produce food and textiles in varying amounts dependant on their type. Both Farms and Livestock require a type, these being either a Crop or an Animal respectively.",
    "crops": "\nThere are 8 Crops in the game. They are Wheat, Barley, Oat, Cabbage, Onion, Beans, Apple and Pears. Fields require a type of crop when being built, but this is entirely aestetic.",
    "animals": "\nThere are 3 Animals in the game. They are Cow, Sheep and Chickens. Cows produce a large amount of food (4) and a small amount of textiles (1) on harvest. Sheep produce a small amount of food (1) and a large amount of textiles (4) on harvest. Chickens produce a medium amount of both on harvest (2 of each).",
    "jobs": "\nThere are 7 Specialist Jobs in the game, as well as laborer and child. These are Lumberjack, Miner, Farmer, Shepard, Smith, Builder and Tailor. Each of these has their own info page.",
    "lumberjack": "\nLumberjacks require tools to work. If there are enough tools in the village, they will produce 5 wood on harvest.",
    "miner": "\nMiners require tools to work. If there are enough tools in the village, they will produce 5 stone and have a change to produce metal on harvest.",
    "farmer": "\nFarmers work on fields. More info about fields can be found under 'buildings' and 'crops'.",
    "shepherd": "\nShepherds work on livestock. More info about livestock can be found under 'buildings' and 'animals'.",
    "smith": "\nSmiths (aka Blacksmiths) will turn 5 ore into 1 tools.",
    "tailor": "\nTailors will turn 15 textiles into 1 clothes.",
    "builders": "\nBuilders are required when building any building. They will also turn 15 stone and 15 wood into 1 building material."
}
