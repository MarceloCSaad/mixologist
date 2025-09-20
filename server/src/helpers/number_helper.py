import inflect

from typing import Optional
from decimal import Decimal

from src.models.constants import PLURALIZABLE_MEASURING_UNITS, MeasuringUnit


def pluralize_word(word: str) -> str:
    """
    Pluralizes a given word using the inflect library.
    """
    eng = inflect.engine()
    return eng.plural(word)


def quantity_to_normalized_string(quantity: Optional[int] = None) -> str:
    """
    Returns a human-readable string for the quantity, removing unnecessary trailing zeros.
    """
    if quantity is None:
        return None
    normalized_quantity = Decimal(quantity).normalize()
    quantity_str = format(normalized_quantity, 'f').rstrip('0').rstrip('.') if '.' in format(normalized_quantity, 'f') else format(normalized_quantity, 'f')
    return quantity_str


def measured_quantity_to_pluralized_string(measuring_unit: Optional[MeasuringUnit] = None, quantity: Optional[float] = None) -> Optional[str]:
    """
    Converts a measuring quantity enum value to a human-readable string.
    """
    normalized_quantity = quantity_to_normalized_string(quantity)
    if not normalized_quantity:
        return None
    if not measuring_unit:
        return normalized_quantity
    if measuring_unit in PLURALIZABLE_MEASURING_UNITS and quantity != 1:
        pluralized_unit = pluralize_word(measuring_unit.value)
        return f"{normalized_quantity} {pluralized_unit}"
    return f"{normalized_quantity} {measuring_unit.value}"


def measured_ingredient_to_pluralized_string(ingredient_name: str, measuring_unit: Optional[MeasuringUnit] = None, quantity: Optional[float] = None) -> Optional[str]:
    """
    Converts a measured ingredient to a human-readable string.

    Examples inputs:
        ingredient_name="angostura", measuring_unit=MeasuringUnit.DASH, quantity=1
        ingredient_name="ice", measuring_unit=MeasuringUnit.CUBE, quantity=2
        ingredient_name="vodka", measuring_unit=MeasuringUnit.OZ, quantity=3.5
        ingredient_name="vodka", measuring_unit=None, quantity=None

    Examples outputs (respectively):
        "1 dash of angostura"
        "2 cubes of ice"
        "3.5 oz of vodka"
        "vodka"
    """
    if not ingredient_name:
        return None
    
    if not measuring_unit and quantity is not None and quantity != 1:
        ingredient_name = pluralize_word(ingredient_name)

    pluralized_measured_quantity = measured_quantity_to_pluralized_string(measuring_unit=measuring_unit, quantity=quantity)
    if pluralized_measured_quantity:
        return f"{pluralized_measured_quantity}{" of " if measuring_unit else " "}{ingredient_name}"
    return ingredient_name
