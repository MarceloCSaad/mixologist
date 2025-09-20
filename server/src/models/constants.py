from enum import Enum


class StepAction(Enum):
    ADD_INGREDIENT = "add_ingredient"
    MUDDLE = "muddle"
    SHAKE = "shake"
    BLEND = "blend"
    STIR = "stir"
    POUR = "pour"
    PEEL = "peel"
    GRATE = "grate"
    DECORATE = "decorate"

ActionToHumanReadableMapper = {
    StepAction.ADD_INGREDIENT: "add :ingredient",
    StepAction.MUDDLE: "muddle the :ingredient",
    StepAction.SHAKE: "shake the :object",
    StepAction.BLEND: "blend the :ingredient",
    StepAction.STIR: "stir the :object",
    StepAction.POUR: "pour into :glassware",
    StepAction.PEEL: "peel the :object",
    StepAction.GRATE: "grate the :object",
    StepAction.DECORATE: "decorate with :object",
}

class CocktailGlassware(Enum):
    MARGARITA = "margarita_glass"
    MARTINI = "martini_glass"
    COCKTAIL = "cocktail_glass"
    HIGHBALL = "highball_glass"
    COLLINS = "collins_glass"
    COUPE = "coupe_glass"
    HURRICANE = "hurricane_glass"
    SHOT = "shot_glass"
    OLD_FASHIONED = "old_fashioned_glass"
    SNIFTER = "snifter_glass"
    NICK_AND_NORA = "nick_and_nora_glass"
    IRISH_COFFEE = "irish_coffee_glass"
    COPPER_MUG = "copper_mug"
    SOUR = "sour_glass"
    CORDIAL = "cordial_glass"
    LOWBALL = "lowball_glass"
    WINE = "wine_glass"
    CHAMPAGNE = "champagne_glass"
    TIKI = "tiki_glass"
    BEER_MUG = "beer_mug"
    PINT = "pint_glass"
    GLENCAIRN = "glencairn_glass"
    JULEP = "julep"

class MeasuringUnit(Enum):
    ML = "ml"
    OZ = "oz"
    KG = "kg"
    LB = "lb"
    DASH = "dash"
    TSP = "teaspoon"
    TBSP = "tablespoon"
    CUP = "cup"
    PINT = "pint"
    QUART = "quart"
    GALLON = "gallon"
    LITER = "liter"
    GRAM = "gram"
    SLICE = "slice"
    WEDGE = "wedge"
    PIECE = "piece"
    CUBE = "cube"
    LEAF = "leaf"
    PINCH = "pinch"

PLURALIZABLE_MEASURING_UNITS = [
    MeasuringUnit.DASH,
    MeasuringUnit.TSP,
    MeasuringUnit.TBSP,
    MeasuringUnit.CUP,
    MeasuringUnit.PINT,
    MeasuringUnit.QUART,
    MeasuringUnit.GALLON,
    MeasuringUnit.LITER,
    MeasuringUnit.GRAM,
    MeasuringUnit.SLICE,
    MeasuringUnit.WEDGE,
    MeasuringUnit.PIECE,
    MeasuringUnit.CUBE,
    MeasuringUnit.LEAF,
    MeasuringUnit.PINCH,
]

class MixologyTool(Enum):
    COCKTAIL_SHAKER = "cocktail_shaker"
    HAWTHORNE_STRAINER = "hawthorne_strainer"
    JULEP_STRAINER = "julep_strainer"
    FINE_MESH_STRIANER = "fine_mesh_strainer"
    PEELER = "peeler"
    GRATER = "grater"
    BLENDER = "blender"
    MUDDLER = "muddler"
    JIGGER = "jigger"
    STIRRING_SPOON = "stirring_spoon"
    STIRRING_JAR = "stirring_jar"
