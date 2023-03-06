from flask import Blueprint, request
from app.common.http_methods import GET, POST, PUT
from app.services.service import base_service

from ..controllers import IngredientController

ingredient = Blueprint('ingredient', __name__)


@ingredient.route('/', methods=POST)
@base_service
def create_ingredient():
    return IngredientController.create(request.json)


@ingredient.route('/', methods=PUT)
@base_service
def update_ingredient():
    return IngredientController.update(request.json)


@ingredient.route('/id/<_id>', methods=GET)
@base_service
def get_ingredient_by_id(_id: int):
    return IngredientController.get_by_id(_id)


@ingredient.route('/', methods=GET)
@base_service
def get_ingredients():
    return IngredientController.get_all()