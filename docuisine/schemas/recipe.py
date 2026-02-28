from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class _RecipeIngredient(BaseModel):
    ingredient_id: int = Field(..., description="ID of the ingredient", examples=[1])
    quantity: Optional[float] = Field(None, description="Quantity of the ingredient", examples=[2.5])
    unit: Optional[str] = Field(None, description="Unit of measurement for the ingredient", examples=["cups"])
    notes: Optional[str] = Field(None, description="Additional notes about the ingredient", examples=["sifted"])

class _RecipeStep(BaseModel):
    step_number: int = Field(..., description="Step number in the recipe", examples=[1])
    instruction: str = Field(..., description="Instruction for the step", examples=["Preheat the oven to 350°F."])


class RecipeCreate(BaseModel):
    name: str = Field(..., description="Recipe name", examples=["Chocolate Cake"])
    cook_time_sec: Optional[int] = Field(
        None, description="Cooking time in seconds", examples=[3600]
    )
    prep_time_sec: Optional[int] = Field(
        None, description="Preparation time in seconds", examples=[1200]
    )
    non_blocking_time_sec: Optional[int] = Field(
        None, description="Non-blocking time in seconds", examples=[600]
    )
    servings: Optional[int] = Field(None, description="Number of servings", examples=[8])
    description: Optional[str] = Field(
        None, description="Recipe description", examples=["Delicious chocolate cake"]
    )
    ingredients: Optional[list[_RecipeIngredient]] = Field(
        None, description="List of ingredients for the recipe"
    )
    steps: Optional[list[_RecipeStep]] = Field(
        None, description="List of steps for preparing the recipe"
    )


class RecipeUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Recipe name")
    cook_time_sec: Optional[int] = Field(None, description="Cooking time in seconds")
    prep_time_sec: Optional[int] = Field(None, description="Preparation time in seconds")
    non_blocking_time_sec: Optional[int] = Field(None, description="Non-blocking time in seconds")
    servings: Optional[int] = Field(None, description="Number of servings")
    description: Optional[str] = Field(None, description="Recipe description")


class RecipeOut(BaseModel):
    id: int = Field(..., description="Recipe's unique identifier", examples=[1])
    user_id: int = Field(..., description="ID of the user who created the recipe", examples=[1])
    name: str = Field(..., description="Recipe name", examples=["Chocolate Cake"])
    cook_time_sec: Optional[int] = Field(None, description="Cooking time in seconds")
    prep_time_sec: Optional[int] = Field(None, description="Preparation time in seconds")
    non_blocking_time_sec: Optional[int] = Field(None, description="Non-blocking time in seconds")
    servings: Optional[int] = Field(None, description="Number of servings")
    description: Optional[str] = Field(None, description="Recipe description")

    model_config = ConfigDict(from_attributes=True)
