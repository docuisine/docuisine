from typing import TYPE_CHECKING, List, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, Entity

if TYPE_CHECKING:
    from .recipes import RecipeIngredient
    from .stores import Store


class Ingredient(Base, Entity):
    """
    Ingredient model representing an ingredient in a recipe.

    Attributes
    ----------
    id : int
        Primary key identifier for the ingredient.
    name : str
        Name of the ingredient.
    description : Optional[str]
        Description of the ingredient.
    recipes : List[Recipe]
        Recipes that use this ingredient.
    stores : List[Store]
        Stores that stock this ingredient.
    """

    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)

    recipes: Mapped[List["RecipeIngredient"]] = relationship(back_populates="ingredients")
    stores: Mapped[List["Store"]] = relationship(
        "Store", secondary="shelves", back_populates="ingredients"
    )
