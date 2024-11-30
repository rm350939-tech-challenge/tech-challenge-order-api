CREATE SCHEMA IF NOT EXISTS service_order;

CREATE SEQUENCE service_order.orders_sequences_id_seq;

CREATE TABLE service_order.order_sequences (
	id INTEGER NOT NULL DEFAULT nextval('service_order.orders_sequences_id_seq'),
	last_order_id int8 NOT NULL,
	CONSTRAINT order_sequences_pkey PRIMARY KEY (id),
	CONSTRAINT order_sequences_unique UNIQUE (last_order_id)
);

CREATE SEQUENCE service_order.orders_id_seq;

CREATE TABLE service_order.orders (
	id INTEGER NOT NULL DEFAULT nextval('service_order.orders_id_seq'),
	customer_id int4 NOT NULL,
	"number" varchar NOT NULL,
	status int2 NOT NULL,
	total numeric NOT NULL,
	created_at timestamp NOT NULL,
	updated_at timestamp NULL,
	CONSTRAINT orders_pkey PRIMARY KEY (id)
);

CREATE SEQUENCE service_order.order_items_id_seq;

CREATE TABLE service_order.order_items (
	id INTEGER NOT NULL DEFAULT nextval('service_order.order_items_id_seq'),
	product_id int4 NOT NULL,
	order_id int4 NOT NULL,
	price numeric NOT NULL,
	quantity numeric NOT NULL,
	description text NULL,
	CONSTRAINT order_items_pkey PRIMARY KEY (id),
	CONSTRAINT order_items_order_id_fkey FOREIGN KEY (order_id) REFERENCES service_order.orders(id)
);

INSERT INTO service_order.orders (id, customer_id, "number", status, total, created_at, updated_at)
VALUES (nextval('service_order.orders_id_seq'), 1, 'DEMO-001', 1, 35.40, NOW(), NULL);

INSERT INTO service_order.orders (id, customer_id, "number", status, total, created_at, updated_at)
VALUES (nextval('service_order.orders_id_seq'), 2, 'DEMO-002', 1, 10.00, NOW(), NULL);

INSERT INTO service_order.order_items (id, product_id, order_id, price, description, quantity)
VALUES (nextval('service_order.order_items_id_seq'), 1, 1, 18.90, 'Description demo', 1.0);
