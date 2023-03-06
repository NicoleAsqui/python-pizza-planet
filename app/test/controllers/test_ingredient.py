import pytest
from app.controllers import IngredientController


def test_create_when_function_have_a_dict_should_return_a_created_ingredient(app, ingredient: dict):
    created_ingredient, error = IngredientController.create(entry=ingredient)
    pytest.assume(error is None)
    for param, value in ingredient.items():
        pytest.assume(param in created_ingredient)
        pytest.assume(value == created_ingredient[param])
        pytest.assume(created_ingredient["_id"])


def test_update_when_function_have_a_dict_should_return_a_updated_ingredient(app, ingredient: dict):
    created_ingredient, _ = IngredientController.create(entry=ingredient)
    updated_fields = {"name": "updated", "price": 10}
    updated_ingredient, error = IngredientController.update(
        new_values={"_id": created_ingredient["_id"], **updated_fields}
    )
    pytest.assume(error is None)
    ingredient_from_database, error = IngredientController.get_by_id(
        _id=created_ingredient["_id"]
    )
    pytest.assume(error is None)
    for param, value in updated_fields.items():
        pytest.assume(updated_ingredient[param] == value)
        pytest.assume(ingredient_from_database[param] == value)


def test_get_by_id_when_function_have_a_dict_should_return_a_ingredient(app, ingredient: dict):
    created_ingredient, _ = IngredientController.create(entry=ingredient)
    ingredient_from_db, error = IngredientController.get_by_id(
        _id=created_ingredient["_id"]
    )
    pytest.assume(error is None)
    for param, value in created_ingredient.items():
        pytest.assume(ingredient_from_db[param] == value)


def test_get_all_ingredients_when_function_have_a_dict_should_return_all_ingredients(app, ingredients: list):
    created_ingredients = []
    for ingredient in ingredients:
        created_ingredient, _ = IngredientController.create(entry=ingredient)
        created_ingredients.append(created_ingredient)

    ingredients_from_db, error = IngredientController.get_all()
    searchable_ingredients = {
        db_ingredient["_id"]: db_ingredient for db_ingredient in ingredients_from_db
    }
    pytest.assume(error is None)
    for created_ingredient in created_ingredients:
        current_id = created_ingredient["_id"]
        assert current_id in searchable_ingredients
        for param, value in created_ingredient.items():
            pytest.assume(searchable_ingredients[current_id][param] == value)
