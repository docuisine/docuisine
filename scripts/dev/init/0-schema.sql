CREATE TABLE entity (
    preview_img TEXT,
    img TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL
) INHERITS (entity);


CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title TEXT NOT NULL,
    instructions TEXT NOT NULL
) INHERITS (entity);


CREATE TABLE ingredients (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
) INHERITS (entity);

CREATE TABLE recipe_ingredients (
    recipe_id INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    ingredient_id INTEGER NOT NULL REFERENCES ingredients(id) ON DELETE CASCADE,
    quantity TEXT,

    PRIMARY KEY (recipe_id, ingredient_id)
);


CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
) INHERITS (entity);

CREATE TABLE store (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT
) INHERITS (entity);


CREATE INDEX idx_user_email ON users(email);

CREATE INDEX idx_recipe_ingredients_recipe
    ON recipe_ingredients(recipe_id);

CREATE INDEX idx_recipe_ingredients_ingredient
    ON recipe_ingredients(ingredient_id);
