# Database

## Entity Relationship Diagram

```mermaid
erDiagram

    USER {
        int id PK
        text username
        text email
        text password
        text role
        text preview_img
        text img
        timestamp created_at
        timestamp updated_at
    }

    STORE {
        int id PK
        text name
        float longitude
        float latitude
        text address
        text description
        text preview_img
        text img
        timestamp created_at
        timestamp updated_at
    }

    INGREDIENT {
        int id PK
        text name
        text description
        int recipe_id
        text preview_img
        text img
        timestamp created_at
        timestamp updated_at
    }

    RECIPE {
        int id PK
        int user_id FK
        text name
        int cook_time_sec
        int prep_time_sec
        int non_blocking_sec
        int servings
        text description
        text preview_img
        text img
        timestamp created_at
        timestamp updated_at
    }

    CATEGORY {
        int id PK
        text name
        text description
        text preview_img
        text img
        timestamp created_at
        timestamp updated_at
    }

    RECIPE_CATEGORY {
        int recipe_id FK
        int category_id FK
    }

    SHELF {
        int store_id FK
        int ingredient_id FK
        int quantity
        timestamp created_at
        timestamp updated_at
    }

    RECIPE_INGREDIENT {
        int recipe_id FK
        int ingredient_id FK
        int amount_grams
        text amount_readable
        timestamp created_at
        timestamp updated_at
    }

    RECIPE_STEP {
        int recipe_id FK
        int step_num
        text description
        text preview_img
        text img
        timestamp created_at
        timestamp updated_at
    }

    %% Relationships

    USER ||--o{ RECIPE : creates

    RECIPE ||--o{ RECIPE_STEP : has
    RECIPE ||--o{ RECIPE_INGREDIENT : uses
    RECIPE ||--o{ RECIPE_CATEGORY : has
    CATEGORY ||--o{ RECIPE_CATEGORY : includes
    INGREDIENT ||--o{ RECIPE_INGREDIENT : included_in

    STORE ||--o{ SHELF : has
    INGREDIENT ||--o{ SHELF : stored_in
```

Tables that store real life objects should inherit from a superclass `Entity` that has columns `preview_img`, `img`. All tables including `Entity` then inherits from the `default_table` table that has columns `created_at` and `updated_at`.
