-- Strong Entities

INSERT INTO users (username, password, role) VALUES
('admin123', '$2b$12$adminhashedpassword', 'admin'),
('aliceInWakanda', '$2b$12$alicehashedpassword', 'user'),
('bob@aji', '$2b$12$bobhashedpassword', 'user');

INSERT INTO tags (name) VALUES
('vegan'),
('vegetarian'),
('gluten-free'),
('dessert'),
('quick'),
('spicy');

INSERT INTO store (name, location) VALUES
('FreshMart', 'Downtown'),
('Green Valley Market', 'Uptown'),
('Corner Grocery', 'East Side');



-- Weak Entities

INSERT INTO recipes (user_id, title, instructions) VALUES
(2, 'Vegan Lentil Soup', 'Simmer lentils with vegetables and spices for 30 minutes.'),
(2, 'Quick Avocado Toast', 'Toast bread, mash avocado, season, and serve.'),
(3, 'Spicy Chicken Curry', 'Cook chicken with curry paste, coconut milk, and spices.');

INSERT INTO ingredients (name) VALUES
('Lentils'),
('Carrot'),
('Onion'),
('Garlic'),
('Bread'),
('Avocado'),
('Salt'),
('Olive Oil'),
('Chicken'),
('Curry Paste'),
('Coconut Milk'),
('Chili');