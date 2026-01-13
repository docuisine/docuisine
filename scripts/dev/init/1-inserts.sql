BEGIN;

-- =====================
-- USERS
-- =====================
INSERT INTO users (id, username, email, password, role, preview_img, img)
VALUES
    -- password: DevPassword1P!
    (1, 'dev-user', 'dev-user@docuisine.org', '1920b94cd7cee322eaa299e703301f6a446c5ffe8da65e09b110880c9a02747e', 'user', '77c3107c63694a592bb7d552d396deb7.jpeg', '54fb11d2466243c02cf9f17bb9e058be.jpeg'),
    -- password: DevPassword2P!
    (2, 'dev-admin', 'dev-admin@docuisine.org', '752b50d7be2843f1f3b2f6879e5c4fc235c32109781c21fdc938d1f1ce2b17be', 'admin', '18057b0823b72c16fa84730a4513dc7e.png', 'eddbbb83c1c0350d3bfae72864068088.png');

-- =====================
-- INGREDIENTS
-- =====================
INSERT INTO ingredients (id, name, preview_img, img)
VALUES
    (1, 'Salt', NULL, NULL),
    (2, 'Sugar', NULL, NULL),
    (3, 'Flour', NULL, NULL),
    (4, 'Butter', NULL, NULL),
    (5, 'Egg', NULL, NULL);

-- =====================
-- CATEGORIES
-- =====================
INSERT INTO categories (id, name, preview_img, img)
VALUES
  (1, 'Burgers',   '6d09f8822c80eb62e132959bb5244be6.png', 'fa11338d685c087703beef9986cdcadb.png'),
  (2, 'Pizza',    '849da211034cc5c30f294b946ff2c7a7.png', 'ea49a6b4e34a55fbcac0c0e1fba40128.png'),
  (3, 'Filipino', 'd5687c04b9b97bb4e4a06e005221fd23.png', 'e4676820229d699e26f934412baf76c9.png'),
  (4, 'Milk Tea', '110781fe2c14e3dc55e42f5362e017b2.png', 'db87fbdb93459399fcf316893d1203fa.png'),
  (5, 'Cakes',    '34078960e3281927dd727c8b773fd0d9.png', '4bd269213efc61c4aba593ecf977a7b2.png'),
  (6, 'Chicken',  'e43559dc9192bfd9544b025df1836236.png', '2dea993b83df301c2bb8191cd0c1f208.png'),
  (7, 'Japanese', '5ffa35a9a5db83df3c5acd2100087ba8.png', 'cd0164c47476256e46e728bc26348917.png'),
  (8, 'Seafood',  'f866e56564ebfd74212fdad4092c7c1b.png', '8e71b0668ccac4f68362d64daa897c7a.png'),
  (9, 'Noodles',  '00d3f8f653b2c1c5cb82fff10ef89ac8.png', 'e319f82af82e431624ce51d0390f5e85.png'),
  (10, 'Breakfast','eb1a7ee95a49bfe8ccc03bb9930a9161.png', 'a5b866f581d9566ecbf92f88ad1e953d.png'),
  (11, 'Broth',   '346e7bd123f2f830910954f7de28e104.png', 'abbc757a4b66cbfb633000b7ce6c0f39.png'),
  (12, 'Chinese', 'beb6e25b8070e654afcde96e8b036fcd.png', '5dd20caef5423fd64bbc8c1b407ebd16.png'),
  (13, 'Bread',   'c1cdccc3ced4062f1e52b31954519428.png', 'e4084870b5137c9f6b716c368ba886d3.png'),
  (14, 'Western', '863897689b91e0abf47177bedb4c9016.png', 'ad89d0870ec8dd30908eda6d637ad186.png');


-- =====================
-- RECIPES
-- =====================
INSERT INTO recipes (
    id,
    user_id,
    name,
    cook_time_sec,
    prep_time_sec,
    non_blocking_time_sec,
    servings,
    preview_img,
    img
)
VALUES
    (1, 1, 'Pancakes', 600, 300, 0, 4, NULL, NULL),
    (2, 2, 'Scrambled Eggs', 300, 120, 0, 2, NULL, NULL);

-- =====================
-- RECIPE STEPS
-- =====================
INSERT INTO recipe_steps (recipe_id, step_number, description)
VALUES
    (1, 1, 'Mix all dry ingredients together.'),
    (1, 2, 'Add wet ingredients and stir until smooth.'),
    (1, 3, 'Cook on a hot pan until golden brown.'),

    (2, 1, 'Crack eggs into a bowl and whisk.'),
    (2, 2, 'Cook eggs in a pan over low heat while stirring.');

-- =====================
-- RECIPE INGREDIENTS
-- =====================
INSERT INTO recipe_ingredients (
    recipe_id,
    ingredient_id,
    amount_grams,
    amount_readable
)
VALUES
    (1, 1, 5, '1 tsp salt'),
    (1, 2, 20, '2 tbsp sugar'),
    (1, 3, 200, '2 cups flour'),
    (1, 4, 30, '2 tbsp butter'),
    (1, 5, 100, '2 eggs'),

    (2, 1, 2, 'A pinch of salt'),
    (2, 4, 15, '1 tbsp butter'),
    (2, 5, 150, '3 eggs');

-- =====================
-- RECIPE CATEGORIES
-- =====================
INSERT INTO recipe_categories (recipe_id, category_id)
VALUES
    (1, 1), -- Pancakes → Dessert
    (1, 2), -- Pancakes → Breakfast
    (2, 2), -- Scrambled Eggs → Breakfast
    (2, 3); -- Scrambled Eggs → Quick Meals

-- =====================
-- STORES
-- =====================
INSERT INTO stores (
    id,
    name,
    longitude,
    latitude,
    address,
    phone,
    website,
    preview_img,
    img
)
VALUES
    (1, 'Fresh Market', 121.0437, 14.6760, '123 Main St, City', '555-1234', 'https://freshmarket.example', NULL, NULL),
    (2, 'Daily Grocer', 121.0500, 14.6800, '456 Side St, City', NULL, NULL, NULL, NULL);

-- =====================
-- SHELF (STORE INVENTORY)
-- =====================
INSERT INTO shelf (
    store_id,
    ingredient_id,
    quantity
)
VALUES
    (1, 1, 100), -- Salt
    (1, 2, 50),  -- Sugar
    (1, 3, 200), -- Flour
    (1, 4, 40),  -- Butter
    (2, 5, 60);  -- Eggs

COMMIT;


-- Reset sequences to match current data
SELECT setval(pg_get_serial_sequence('users', 'id'),
              (SELECT MAX(id) FROM users),
              true);

SELECT setval(pg_get_serial_sequence('ingredients', 'id'),
              (SELECT MAX(id) FROM ingredients),
              true);

SELECT setval(pg_get_serial_sequence('categories', 'id'),
              (SELECT MAX(id) FROM categories),
              true);

SELECT setval(pg_get_serial_sequence('recipes', 'id'),
              (SELECT MAX(id) FROM recipes),
              true);

SELECT setval(pg_get_serial_sequence('stores', 'id'),
              (SELECT MAX(id) FROM stores),
              true);
