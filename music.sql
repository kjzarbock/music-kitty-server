UPDATE auth_user
SET is_staff = 1
WHERE username = 'admin';

UPDATE musickittyapi_cat
SET image = 'https://i.imgur.com/uk2wFzh.jpg'
WHERE id = 6;

CREATE TABLE product_locations (
    product_id INT,
    location_id INT,
    PRIMARY KEY (product_id, location_id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (location_id) REFERENCES locations(id)
);

INSERT INTO product_locations (product_id, location_id) VALUES (1, 1);
INSERT INTO product_locations (product_id, location_id) VALUES (1, 2);
