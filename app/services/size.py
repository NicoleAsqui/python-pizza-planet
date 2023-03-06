from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request

from app.services.service import base_service

from ..controllers import SizeController

size = Blueprint('size', __name__)


@size.route('/', methods=POST)
@base_service
def create_size():
    return SizeController.create(request.json)


@size.route('/', methods=PUT)
@base_service
def update_size():
    return SizeController.update(request.json)


@size.route('/id/<_id>', methods=GET)
@base_service
def get_size_by_id(_id: int):
    return SizeController.get_by_id(_id)


@size.route('/', methods=GET)
@base_service
def get_sizes():
    return SizeController.get_all()