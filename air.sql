CREATE TABLE `airline` (
  `airline_name` varchar(50) NOT NULL,
  PRIMARY KEY(`airline_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `airline_staff`
--

CREATE TABLE `airline_staff` (
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `date_of_birth` date NOT NULL,
  `airline_name` varchar(50) NOT NULL,
  PRIMARY KEY(`username`),
  FOREIGN KEY(`airline_name`) REFERENCES `airline`(`airline_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

CREATE TABLE `permission` (
    `username` varchar(50) NOT NULL,
    `permission_type` varchar(50) NOT NULL,
    PRIMARY KEY(`username`, `permission_type`),
    FOREIGN KEY(`username`) REFERENCES `airline_staff`(`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `airplane`
--

CREATE TABLE `airplane` (
  `airline_name` varchar(50) NOT NULL,
  `airplane_id` int(11) NOT NULL,
  `seats` int(11) NOT NULL,
  PRIMARY KEY(`airline_name`, `airplane_id`),
  FOREIGN KEY(`airline_name`) REFERENCES `airline`(`airline_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `airport`
--

CREATE TABLE `airport` (
  `airport_name` varchar(50) NOT NULL,
  `airport_city` varchar(50) NOT NULL,
  PRIMARY KEY(`airport_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `booking_agent`
--

CREATE TABLE `booking_agent` (
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `booking_agent_id` int(11) NOT NULL,
  PRIMARY KEY(`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `booking_agent_work_for` (
  `email` varchar(50) NOT NULL,
  `airline_name` varchar(50) NOT NULL,
  PRIMARY KEY(`email`,`airline_name`),
  FOREIGN KEY(`email`) REFERENCES `booking_agent`(`email`),
  FOREIGN KEY(`airline_name`) REFERENCES `airline`(`airline_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `email` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `building_number` varchar(30) NOT NULL,
  `street` varchar(30) NOT NULL,
  `city` varchar(30) NOT NULL,
  `state` varchar(30) NOT NULL,
  `phone_number` int(11) NOT NULL,
  `passport_number` varchar(30) NOT NULL,
  `passport_expiration` date NOT NULL,
  `passport_country` varchar(50) NOT NULL,
  `date_of_birth` date NOT NULL,
  PRIMARY KEY(`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `flight`
--

CREATE TABLE `flight` (
  `airline_name` varchar(50) NOT NULL,
  `flight_num` int(11) NOT NULL,
  `departure_airport` varchar(50) NOT NULL,
  `departure_time` datetime NOT NULL,
  `arrival_airport` varchar(50) NOT NULL,
  `arrival_time` datetime NOT NULL,
  `price` decimal(10,0) NOT NULL,
  `status` varchar(50) NOT NULL,
  `airplane_id` int(11) NOT NULL,
  PRIMARY KEY(`airline_name`, `flight_num`),
  FOREIGN KEY(`airline_name`, `airplane_id`) REFERENCES `airplane`(`airline_name`, `airplane_id`),
  FOREIGN KEY(`departure_airport`) REFERENCES `airport`(`airport_name`),
  FOREIGN KEY(`arrival_airport`) REFERENCES `airport`(`airport_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

CREATE TABLE `ticket` (
  `ticket_id` int(11) NOT NULL,
  `airline_name` varchar(50) NOT NULL,
  `flight_num` int(11) NOT NULL,
  PRIMARY KEY(`ticket_id`),
  FOREIGN KEY(`airline_name`, `flight_num`) REFERENCES `flight`(`airline_name`, `flight_num`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- --------------------------------------------------------

--
-- Table structure for table `purchases`
--

CREATE TABLE `purchases` (
  `ticket_id` int(11) NOT NULL,
  `customer_email` varchar(50) NOT NULL,
  `booking_agent_id` int(11),
  `purchase_date` date NOT NULL,
  PRIMARY KEY(`ticket_id`, `customer_email`),
  FOREIGN KEY(`ticket_id`) REFERENCES `ticket`(`ticket_id`),
  FOREIGN KEY(`customer_email`) REFERENCES `customer`(`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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

-- Tickets (one per flight for now)
INSERT INTO ticket (ticket_id, airline_name, flight_num) VALUES
(5001, 'CSCI Air', 1001),
(5002, 'CSCI Air', 1002);

-- Customer
INSERT INTO customer (
  email, name, password, building_number, street, city, state, phone_number,
  passport_number, passport_expiration, passport_country, date_of_birth
) VALUES
('naruto@example.com','Naruto','password','1','Leaf St','San Francisco','CA',1234567890,
 'P12345','2030-01-01','USA','2000-01-01');
