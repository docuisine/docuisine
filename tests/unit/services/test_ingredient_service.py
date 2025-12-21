from unittest.mock import MagicMock

import pytest
from sqlalchemy.exc import IntegrityError

from docuisine.db.models import Ingredient
from docuisine.services import IngredientService
from docuisine.utils.errors import IngredientExistsError, IngredientNotFoundError


def test_create_ingredient(db_session: MagicMock):
    """Test creating a new ingredient."""
    service = IngredientService(db_session)
    ingredient: Ingredient = service.create_ingredient(name="Sugar", description="Sweetener")

    assert ingredient.name == "Sugar"
    assert ingredient.description == "Sweetener"
    db_session.add.assert_called_once_with(ingredient)
    db_session.commit.assert_called_once()


def test_create_ingredient_without_description(db_session: MagicMock):
    """Test creating an ingredient without a description."""
    service = IngredientService(db_session)
    ingredient: Ingredient = service.create_ingredient(name="Salt")

    assert ingredient.name == "Salt"
    assert ingredient.description is None
    db_session.add.assert_called_once_with(ingredient)
    db_session.commit.assert_called_once()


def test_create_ingredient_duplicate_name_raises_error(db_session: MagicMock):
    """Test that creating an ingredient with duplicate name raises IngredientExistsError."""
    service = IngredientService(db_session)
    db_session.commit.side_effect = IntegrityError(
        statement=None,
        params=None,
        orig=Exception(),
    )

    with pytest.raises(IngredientExistsError) as exc_info:
        service.create_ingredient(name="Sugar")

    assert "Sugar" in str(exc_info.value)
    db_session.add.assert_called_once()
    db_session.commit.assert_called_once()
    db_session.rollback.assert_called_once()


def test_get_ingredient_by_id(db_session: MagicMock, monkeypatch):
    """Test retrieving an ingredient by ID."""
    service = IngredientService(db_session)
    example_ingredient = Ingredient(id=1, name="Flour", description="All-purpose")
    monkeypatch.setattr(
        service,
        "_get_ingredient_by_id",
        lambda ingredient_id: example_ingredient,
    )

    retrieved: Ingredient = service.get_ingredient(ingredient_id=example_ingredient.id)

    assert retrieved.name == "Flour"


def test_get_ingredient_by_name(db_session: MagicMock, monkeypatch):
    """Test retrieving an ingredient by name."""
    service = IngredientService(db_session)
    created = Ingredient(id=1, name="Butter")
    monkeypatch.setattr(
        service,
        "_get_ingredient_by_name",
        lambda name: created,
    )

    retrieved: Ingredient = service.get_ingredient(name="Butter")

    assert retrieved.id == created.id
    assert retrieved.name == "Butter"


def test_get_ingredient_not_found_by_id_raises_error(db_session: MagicMock, monkeypatch):
    """Test that getting a non-existent ingredient by ID raises IngredientNotFoundError."""
    service = IngredientService(db_session)
    monkeypatch.setattr(service, "_get_ingredient_by_id", lambda ingredient_id: None)

    with pytest.raises(IngredientNotFoundError) as exc_info:
        service.get_ingredient(ingredient_id=999)

    assert "999" in str(exc_info.value)


def test_get_ingredient_not_found_by_name_raises_error(db_session: MagicMock, monkeypatch):
    """Test that getting a non-existent ingredient by name raises IngredientNotFoundError."""
    service = IngredientService(db_session)
    monkeypatch.setattr(service, "_get_ingredient_by_name", lambda name: None)

    with pytest.raises(IngredientNotFoundError) as exc_info:
        service.get_ingredient(name="NonExistent")

    assert "NonExistent" in str(exc_info.value)


def test_get_ingredient_without_params_raises_error(db_session: MagicMock):
    """Test that calling get_ingredient without parameters raises ValueError."""
    service = IngredientService(db_session)

    with pytest.raises(ValueError) as exc_info:
        service.get_ingredient()

    assert "Either ingredient ID or name must be provided" in str(exc_info.value)


def test_get_all_ingredients(db_session: MagicMock):
    """Test retrieving all ingredients."""
    service = IngredientService(db_session)
    ing1 = Ingredient(id=1, name="Milk")
    ing2 = Ingredient(id=2, name="Eggs")
    ing3 = Ingredient(id=3, name="Yeast")
    db_session.query.return_value.all.return_value = [ing1, ing2, ing3]

    all_ingredients = service.get_all_ingredients()

    assert len(all_ingredients) == 3
    ingredient_names = {ing.name for ing in all_ingredients}
    assert ingredient_names == {"Milk", "Eggs", "Yeast"}
    db_session.query.assert_called_once_with(Ingredient)
    db_session.query.return_value.all.assert_called_once()


def test_update_ingredient_name(db_session: MagicMock, monkeypatch):
    """Test updating an ingredient's name."""
    service = IngredientService(db_session)
    ingredient: Ingredient = Ingredient(id=1, name="Suagar", description="Sweetener")
    monkeypatch.setattr(service, "_get_ingredient_by_id", lambda x: ingredient)

    updated: Ingredient = service.update_ingredient(ingredient.id, name="Sugar")

    db_session.commit.assert_called_once()
    assert updated.id == ingredient.id
    assert updated.name == "Sugar"
    assert updated.description == ingredient.description


def test_update_ingredient_description(db_session: MagicMock, monkeypatch):
    """Test updating an ingredient's description."""
    service = IngredientService(db_session)
    ingredient: Ingredient = Ingredient(id=1, name="Salt", description="Old desc")
    monkeypatch.setattr(service, "_get_ingredient_by_id", lambda x: ingredient)

    updated: Ingredient = service.update_ingredient(ingredient.id, description="New desc")

    db_session.commit.assert_called_once()
    assert updated.id == ingredient.id
    assert updated.name == "Salt"
    assert updated.description == "New desc"


def test_update_ingredient_recipe_id(db_session: MagicMock, monkeypatch):
    """Test updating an ingredient's recipe_id."""
    service = IngredientService(db_session)
    ingredient: Ingredient = Ingredient(id=1, name="Butter", description=None, recipe_id=None)
    monkeypatch.setattr(service, "_get_ingredient_by_id", lambda x: ingredient)

    updated: Ingredient = service.update_ingredient(ingredient.id, recipe_id=42)

    db_session.commit.assert_called_once()
    assert updated.id == ingredient.id
    assert updated.recipe_id == 42


def test_update_ingredient_both_fields(db_session: MagicMock, monkeypatch):
    """Test updating multiple fields of an ingredient."""
    service = IngredientService(db_session)
    example: Ingredient = Ingredient(id=1, name="Flour", description="All-purpose", recipe_id=None)
    monkeypatch.setattr(service, "_get_ingredient_by_id", lambda x: example)

    updated = service.update_ingredient(
        example.id, name="00 Flour", description="Fine milled", recipe_id=7
    )
    db_session.commit.assert_called_once()
    assert updated.id == example.id
    assert updated.name == "00 Flour"
    assert updated.description == "Fine milled"
    assert updated.recipe_id == 7


def test_update_ingredient_not_found_raises_error(db_session: MagicMock, monkeypatch):
    """Test that updating a non-existent ingredient raises IngredientNotFoundError."""
    service = IngredientService(db_session)
    monkeypatch.setattr(service, "_get_ingredient_by_id", lambda x: None)

    with pytest.raises(IngredientNotFoundError) as exc_info:
        service.update_ingredient(999, name="NewName")

    assert "999" in str(exc_info.value)


def test_update_ingredient_duplicate_name_raises_error(db_session: MagicMock):
    """Test that updating to a duplicate name raises IngredientExistsError."""
    service = IngredientService(db_session)

    db_session.commit.side_effect = IntegrityError(
        statement=None,
        params=None,
        orig=Exception(),
    )
    with pytest.raises(IngredientExistsError) as exc_info:
        service.update_ingredient(1, name="Salt")

    assert "Salt" in str(exc_info.value)
    db_session.commit.assert_called_once()
    db_session.rollback.assert_called_once()


def test_delete_ingredient(db_session: MagicMock, monkeypatch):
    """Test deleting an ingredient."""
    service = IngredientService(db_session)
    example = Ingredient(id=1, name="ToDelete", description="To be deleted")
    monkeypatch.setattr(service, "_get_ingredient_by_id", lambda id: example)
    service.delete_ingredient(example.id)
    db_session.delete.assert_called_once_with(example)
    db_session.commit.assert_called_once()


def test_delete_ingredient_not_found_raises_error(db_session: MagicMock, monkeypatch):
    """Test that deleting a non-existent ingredient raises IngredientNotFoundError."""
    service = IngredientService(db_session)
    monkeypatch.setattr(service, "_get_ingredient_by_id", lambda x: None)

    with pytest.raises(IngredientNotFoundError) as exc_info:
        service.delete_ingredient(999)

    assert "999" in str(exc_info.value)


def test_get_ingredient_by_name_primitive(db_session: MagicMock):
    """
    Test retrieving an ingredient by name by testing correct
    calling procedure of primitive SQLAlchemy methods.
    """
    service = IngredientService(db_session)
    example_ingredient = Ingredient(id=1, name="Sugar", description="Sweetener")
    db_session.first.return_value = example_ingredient

    result = service._get_ingredient_by_name(name="Sugar")

    assert result == example_ingredient
    db_session.query.assert_called_once_with(Ingredient)
    db_session.filter_by.assert_called_with(name="Sugar")
    db_session.first.assert_called_once()


def test_get_ingredient_by_id_primitive(db_session: MagicMock):
    """
    Test retrieving an ingredient by ID by testing correct
    calling procedure of primitive SQLAlchemy methods.
    """
    service = IngredientService(db_session)
    example_ingredient = Ingredient(id=1, name="Salt", description="Mineral")
    db_session.first.return_value = example_ingredient

    result = service._get_ingredient_by_id(ingredient_id=1)

    assert result == example_ingredient
    db_session.query.assert_called_once_with(Ingredient)
    db_session.filter_by.assert_called_with(id=1)
    db_session.first.assert_called_once()
