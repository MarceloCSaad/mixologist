from src.database.db_service import PGDatabaseService
from src.models.services.cocktail_service import CocktailService
from src.models.services.ingredient_service import IngredientService
from src.models.services.tag_service import TagService
from src.models.constants import MeasuringUnit, StepAction
from src.models.step import Step

db_service = PGDatabaseService()
db_service.create_tables()

with db_service.get_session() as session:
    # Create tags
    tag_service = TagService()
    tag1 = tag_service.get_or_create_tag(name="strong", session=session)
    tag2 = tag_service.get_or_create_tag(name="fruit", session=session)
    list_of_tags = [tag1, tag2]

    # Create ingredients
    ingredient_service = IngredientService()
    cachaca = ingredient_service.get_or_create_ingredient(
        name="Cachaça", session=session
    )
    lime = ingredient_service.get_or_create_ingredient(name="Lime", session=session)
    sugar = ingredient_service.get_or_create_ingredient(name="Sugar", session=session)
    ice = ingredient_service.get_or_create_ingredient(name="Ice", session=session)
    list_of_ingredients = [cachaca, lime, sugar, ice]

    # Build steps for the recipe
    steps = [
        Step(
            action=StepAction.ADD_INGREDIENT,
            ingredient=lime,
            measuring_unit=MeasuringUnit.PIECE,
            quantity=8,
        ),
        Step(action=StepAction.MUDDLE, ingredient=lime),
        Step(
            action=StepAction.ADD_INGREDIENT,
            ingredient=sugar,
            measuring_unit=MeasuringUnit.GRAM,
            quantity=20,
        ),
        Step(action=StepAction.ADD_INGREDIENT, ingredient=ice, quantity=5),
        Step(
            action=StepAction.ADD_INGREDIENT,
            ingredient=cachaca,
            measuring_unit=MeasuringUnit.ML,
            quantity=80,
        ),
    ]

    # Create cocktail and associate steps and tags
    cocktail_service = CocktailService()
    cocktail = cocktail_service.update_or_create(
        session=session,
        name="Caipirinha",
        description="Brazillian popular drink",
        tags=list_of_tags,
        steps=steps,
        validate=True,
    )

    session.add_all(
        [
            cocktail,
            *list_of_tags,
            *list_of_ingredients,
        ]
    )
    session.commit()
    session.refresh(cocktail)
    print(f"Created cocktail: {cocktail}")
    print(f"cocktail.all_steps: {cocktail.all_steps}")
    print(f"cocktail.first_step: {cocktail.first_step}")
    print(f"cocktail.steps: {cocktail.steps}")
    print(f"cocktail.cocktail_tag_associations: {cocktail.cocktail_tag_associations}")
    print(f"cocktail.tags: {cocktail.tags}")
    print(f"cocktail.last_step: {cocktail.last_step}")
    print("Recipe steps:")
    for step in cocktail.steps:
        print(f"- {step.get_human_readable_step_explanation()}")
