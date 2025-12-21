from typing import Optional


class IngredientExistsError(Exception):
    """Exception raised when an ingredient already exists."""

    def __init__(self, name: str):
        self.name = name
        self.message = f"Ingredient with name '{self.name}' already exists."
        super().__init__(self.message)


class IngredientNotFoundError(Exception):
    """Exception raised when an ingredient is not found."""

    def __init__(self, ingredient_id: Optional[int] = None, name: Optional[str] = None):
        self.ingredient_id = ingredient_id
        self.name = name
        if name is not None:
            self.message = f"Ingredient with name '{name}' not found."
        else:
            self.message = f"Ingredient with ID {self.ingredient_id} not found."
        super().__init__(self.message)
