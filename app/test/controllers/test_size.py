import pytest
from app.controllers import SizeController


def test_create_size_when_function_have_a_dict_should_return_a_created_size(app, size: dict):
    created_size, error = SizeController.create(size)
    pytest.assume(error is None)
    for param, value in size.items():
        pytest.assume(param in created_size)
        pytest.assume(value == created_size[param])
        pytest.assume(created_size["_id"])


def test_update_when_function_have_a_dict_should_return_a_updated_size(app, size: dict):
    created_size, _ = SizeController.create(entry=size)
    updated_fields = {"name": "updated", "price": 10}
    updated_size, error = SizeController.update(
        new_values={"_id": created_size["_id"], **updated_fields}
    )
    pytest.assume(error is None)
    for param, value in updated_fields.items():
        pytest.assume(updated_size[param] == value)


def test_get_by_id_when_function_have_a_dict_should_return_a_size(app, size: dict):
    created_size, _ = SizeController.create(entry=size)
    size_from_db, error = SizeController.get_by_id(_id=created_size["_id"])
    pytest.assume(error is None)
    for param, value in created_size.items():
        pytest.assume(size_from_db[param] == value)


def test_get_all_sizes_when_function_have_a_dict_should_return_all_sizes(app, sizes: list):
    created_sizes = []
    for size in sizes:
        created_size, _ = SizeController.create(entry=size)
        created_sizes.append(created_size)

    sizes_from_db, error = SizeController.get_all()
    searchable_sizes = {db_size["_id"]: db_size for db_size in sizes_from_db}
    pytest.assume(error is None)
    for created_size in created_sizes:
        current_id = created_size["_id"]
        assert current_id in searchable_sizes
        for param, value in created_size.items():
            pytest.assume(searchable_sizes[current_id][param] == value)
