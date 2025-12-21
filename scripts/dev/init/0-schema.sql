CREATE TABLE default_table (
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE entity (
    preview_img TEXT,
    img TEXT
) INHERITS (default_table);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL
) INHERITS (entity);


CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name TEXT NOT NULL UNIQUE,
    cook_time_sec INTEGER CHECK (cook_time_sec >= 0),
    prep_time_sec INTEGER CHECK (prep_time_sec >= 0),
    non_blocking_time_sec INTEGER CHECK (non_blocking_time_sec >= 0),
    servings INTEGER CHECK (servings >= 0),
    description TEXT
) INHERITS (entity);

CREATE TABLE recipe_steps (
    recipe_id INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    step_number INTEGER NOT NULL CHECK (step_number >= 1),
    description TEXT NOT NULL,

    PRIMARY KEY (recipe_id, step_number)
) INHERITS (default_table);

CREATE TABLE ingredients (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    recipe_id INTEGER REFERENCES recipes(id) ON DELETE SET NULL
) INHERITS (entity);

CREATE TABLE recipe_ingredients (
    recipe_id INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    ingredient_id INTEGER NOT NULL REFERENCES ingredients(id) ON DELETE CASCADE,
    amount_grams REAL CHECK (amount_grams >= 0),
    amount_readable TEXT NOT NULL,

    PRIMARY KEY (recipe_id, ingredient_id)
) INHERITS (default_table);


CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT
) INHERITS (entity);

CREATE TABLE recipe_categories (
    recipe_id INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE,

    PRIMARY KEY (recipe_id, category_id)
) INHERITS (default_table);

CREATE TABLE stores (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    longitude DOUBLE PRECISION CHECK (longitude >= -180 AND longitude <= 180),
    latitude DOUBLE PRECISION CHECK (latitude >= -90 AND latitude <= 90),
    address TEXT NOT NULL,
    phone TEXT,
    website TEXT,
    description TEXT
) INHERITS (entity);


CREATE TABLE shelf (
    store_id INTEGER NOT NULL REFERENCES stores(id) ON DELETE CASCADE,
    ingredient_id INTEGER NOT NULL REFERENCES ingredients(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL CHECK (quantity >= 0),

    PRIMARY KEY (store_id, ingredient_id)
) INHERITS (default_table);


CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_updated_at
BEFORE UPDATE ON default_table
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();
