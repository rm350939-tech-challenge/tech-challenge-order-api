import pytest
from domain.exceptions import EntityNotFoundException, EntityAlreadyExistsException


def test_entity_not_found_exception():
    message = "Entity not found"
    with pytest.raises(EntityNotFoundException) as exc_info:
        raise EntityNotFoundException(message)
    assert str(exc_info.value) == message
    assert exc_info.value.message == message


def test_entity_already_exists_exception():
    message = "Entity already exists"
    with pytest.raises(EntityAlreadyExistsException) as exc_info:
        raise EntityAlreadyExistsException(message)
    assert str(exc_info.value) == message
    assert exc_info.value.message == message
