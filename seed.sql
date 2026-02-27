
-- Airline
INSERT INTO airline (airline_name) VALUES ('CSCI Air');

-- Airports
INSERT INTO airport (airport_name, airport_city) VALUES
('SFO', 'San Francisco'),
('LAX', 'Los Angeles'),
('SEA', 'Seattle');

-- Airplanes
INSERT INTO airplane (airline_name, airplane_id, seats) VALUES
('CSCI Air', 1, 180);

-- Flights
INSERT INTO flight (
  airline_name, flight_num, departure_airport, departure_time,
  arrival_airport, arrival_time, price, status, airplane_id
) VALUES
('CSCI Air', 1001, 'SFO', '2026-02-15 09:00:00', 'LAX', '2026-02-15 10:30:00', 199, 'On Time', 1),
('CSCI Air', 1002, 'LAX', '2026-02-16 14:00:00', 'SEA', '2026-02-16 17:00:00', 249, 'Delayed', 1);

-- Optional customer
INSERT INTO customer (
  email, name, password, building_number, street, city, state, phone_number,
  passport_number, passport_expiration, passport_country, date_of_birth
) VALUES
('naruto@example.com','Naruto','password','1','Leaf St','San Francisco','CA',1234567890,
 'P12345','2030-01-01','USA','2000-01-01');
