-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 30-09-2025 a las 03:02:47
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `realestatedb`
--

DELIMITER $$
--
-- Procedimientos
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_delete_agent` (IN `p_agent_id` INT)   BEGIN
    DELETE FROM Agents 
    WHERE AgentID = p_agent_id;
    
    SELECT ROW_COUNT() AS RowsAffected;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_delete_client` (IN `p_client_id` INT)   BEGIN
    DELETE FROM Clients 
    WHERE ClientID = p_client_id;
    
    SELECT ROW_COUNT() AS RowsAffected;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_delete_office` (IN `p_office_id` INT)   BEGIN
    DELETE FROM Offices 
    WHERE OfficeID = p_office_id;
    
    SELECT ROW_COUNT() AS RowsAffected;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_delete_property` (IN `p_property_id` INT)   BEGIN
    DELETE FROM Properties 
    WHERE PropertyID = p_property_id;
    
    SELECT ROW_COUNT() AS RowsAffected;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_delete_sale` (IN `p_sale_id` INT)   BEGIN
    DELETE FROM Sales 
    WHERE SaleID = p_sale_id;
    
    SELECT ROW_COUNT() AS RowsAffected;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_get_agent_by_id` (IN `p_agent_id` INT)   BEGIN
    SELECT AgentID, Name, Phone 
    FROM Agents 
    WHERE AgentID = p_agent_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_get_all_agents` ()   BEGIN
    SELECT AgentID, Name, Phone 
    FROM Agents 
    ORDER BY AgentID;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_get_all_clients` ()   BEGIN
    SELECT ClientID, Name, Email 
    FROM Clients 
    ORDER BY ClientID;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_get_all_offices` ()   BEGIN
    SELECT OfficeID, Location, Phone 
    FROM Offices 
    ORDER BY OfficeID;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_get_all_properties` ()   BEGIN
    SELECT PropertyID, Address, Price 
    FROM Properties 
    ORDER BY PropertyID;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_get_all_sales` ()   BEGIN
    SELECT s.SaleID, s.PropertyID, p.Address AS PropertyAddress, p.Price,
           s.ClientID, c.Name AS ClientName, c.Email AS ClientEmail
    FROM Sales s
    JOIN Properties p ON s.PropertyID = p.PropertyID
    JOIN Clients c ON s.ClientID = c.ClientID
    ORDER BY s.SaleID;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_get_client_by_id` (IN `p_client_id` INT)   BEGIN
    SELECT ClientID, Name, Email 
    FROM Clients 
    WHERE ClientID = p_client_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_get_office_by_id` (IN `p_office_id` INT)   BEGIN
    SELECT OfficeID, Location, Phone 
    FROM Offices 
    WHERE OfficeID = p_office_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_get_property_by_id` (IN `p_property_id` INT)   BEGIN
    SELECT PropertyID, Address, Price 
    FROM Properties 
    WHERE PropertyID = p_property_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_get_sale_by_id` (IN `p_sale_id` INT)   BEGIN
    SELECT s.SaleID, s.PropertyID, p.Address AS PropertyAddress, 
           s.ClientID, c.Name AS ClientName
    FROM Sales s
    JOIN Properties p ON s.PropertyID = p.PropertyID
    JOIN Clients c ON s.ClientID = c.ClientID
    WHERE s.SaleID = p_sale_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_insert_agent` (IN `p_name` VARCHAR(50), IN `p_phone` VARCHAR(15))   BEGIN
    INSERT INTO Agents (Name, Phone) 
    VALUES (p_name, p_phone);
    
    SELECT LAST_INSERT_ID() AS NewAgentID;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_insert_client` (IN `p_name` VARCHAR(50), IN `p_email` VARCHAR(50))   BEGIN
    INSERT INTO Clients (Name, Email) 
    VALUES (p_name, p_email);
    
    SELECT LAST_INSERT_ID() AS NewClientID;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_insert_office` (IN `p_location` VARCHAR(50), IN `p_phone` VARCHAR(15))   BEGIN
    INSERT INTO Offices (Location, Phone) 
    VALUES (p_location, p_phone);
    
    SELECT LAST_INSERT_ID() AS NewOfficeID;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_insert_property` (IN `p_address` VARCHAR(100), IN `p_price` DECIMAL(12,2))   BEGIN
    INSERT INTO Properties (Address, Price) 
    VALUES (p_address, p_price);
    
    SELECT LAST_INSERT_ID() AS NewPropertyID;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_insert_sale` (IN `p_property_id` INT, IN `p_client_id` INT)   BEGIN
    DECLARE property_exists INT DEFAULT 0;
    DECLARE client_exists INT DEFAULT 0;
    
    -- Verificar si la propiedad existe
    SELECT COUNT(*) INTO property_exists 
    FROM Properties 
    WHERE PropertyID = p_property_id;
    
    -- Verificar si el cliente existe
    SELECT COUNT(*) INTO client_exists 
    FROM Clients 
    WHERE ClientID = p_client_id;
    
    IF property_exists = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La propiedad no existe';
    ELSEIF client_exists = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El cliente no existe';
    ELSE
        INSERT INTO Sales (PropertyID, ClientID) 
        VALUES (p_property_id, p_client_id);
        
        SELECT LAST_INSERT_ID() AS NewSaleID;
    END IF;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_update_agent` (IN `p_agent_id` INT, IN `p_name` VARCHAR(50), IN `p_phone` VARCHAR(15))   BEGIN
    UPDATE Agents 
    SET Name = p_name, 
        Phone = p_phone 
    WHERE AgentID = p_agent_id;
    
    SELECT ROW_COUNT() AS RowsAffected;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_update_client` (IN `p_client_id` INT, IN `p_name` VARCHAR(50), IN `p_email` VARCHAR(50))   BEGIN
    UPDATE Clients 
    SET Name = p_name, 
        Email = p_email 
    WHERE ClientID = p_client_id;
    
    SELECT ROW_COUNT() AS RowsAffected;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_update_office` (IN `p_office_id` INT, IN `p_location` VARCHAR(50), IN `p_phone` VARCHAR(15))   BEGIN
    UPDATE Offices 
    SET Location = p_location, 
        Phone = p_phone 
    WHERE OfficeID = p_office_id;
    
    SELECT ROW_COUNT() AS RowsAffected;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_update_property` (IN `p_property_id` INT, IN `p_address` VARCHAR(100), IN `p_price` DECIMAL(12,2))   BEGIN
    UPDATE Properties 
    SET Address = p_address, 
        Price = p_price 
    WHERE PropertyID = p_property_id;
    
    SELECT ROW_COUNT() AS RowsAffected;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_update_sale` (IN `p_sale_id` INT, IN `p_property_id` INT, IN `p_client_id` INT)   BEGIN
    UPDATE Sales 
    SET PropertyID = p_property_id, 
        ClientID = p_client_id 
    WHERE SaleID = p_sale_id;
    
    SELECT ROW_COUNT() AS RowsAffected;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `agents`
--

CREATE TABLE `agents` (
  `AgentID` int(11) NOT NULL,
  `Name` varchar(50) DEFAULT NULL,
  `Phone` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `agents`
--

INSERT INTO `agents` (`AgentID`, `Name`, `Phone`) VALUES
(1, 'Juan Pérez', '555-1234'),
(2, 'María López', '555-5678'),
(3, 'Carlos Gómez', '555-9012');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clients`
--

CREATE TABLE `clients` (
  `ClientID` int(11) NOT NULL,
  `Name` varchar(50) DEFAULT NULL,
  `Email` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `clients`
--

INSERT INTO `clients` (`ClientID`, `Name`, `Email`) VALUES
(1, 'Ana Martínez', 'ana.martinez@email.com'),
(2, 'Luis Rodríguez', 'luis.rodriguez@email.com'),
(3, 'Sofía García', 'sofia.garcia@email.com');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `offices`
--

CREATE TABLE `offices` (
  `OfficeID` int(11) NOT NULL,
  `Location` varchar(50) DEFAULT NULL,
  `Phone` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `offices`
--

INSERT INTO `offices` (`OfficeID`, `Location`, `Phone`) VALUES
(1, 'Downtown Springfield', '555-0001'),
(2, 'Uptown Springfield', '555-0002'),
(3, 'Shelbyville Central', '555-0003');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `properties`
--

CREATE TABLE `properties` (
  `PropertyID` int(11) NOT NULL,
  `Address` varchar(100) DEFAULT NULL,
  `Price` decimal(12,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `properties`
--

INSERT INTO `properties` (`PropertyID`, `Address`, `Price`) VALUES
(1, '123 Maple St, Springfield', 250000.00),
(2, '456 Oak Ave, Springfield', 320000.00),
(3, '789 Pine Rd, Shelbyville', 180000.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sales`
--

CREATE TABLE `sales` (
  `SaleID` int(11) NOT NULL,
  `PropertyID` int(11) DEFAULT NULL,
  `ClientID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `sales`
--

INSERT INTO `sales` (`SaleID`, `PropertyID`, `ClientID`) VALUES
(1, 1, 2),
(2, 2, 3),
(3, 3, 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `agents`
--
ALTER TABLE `agents`
  ADD PRIMARY KEY (`AgentID`);

--
-- Indices de la tabla `clients`
--
ALTER TABLE `clients`
  ADD PRIMARY KEY (`ClientID`);

--
-- Indices de la tabla `offices`
--
ALTER TABLE `offices`
  ADD PRIMARY KEY (`OfficeID`);

--
-- Indices de la tabla `properties`
--
ALTER TABLE `properties`
  ADD PRIMARY KEY (`PropertyID`);

--
-- Indices de la tabla `sales`
--
ALTER TABLE `sales`
  ADD PRIMARY KEY (`SaleID`),
  ADD KEY `PropertyID` (`PropertyID`),
  ADD KEY `ClientID` (`ClientID`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `agents`
--
ALTER TABLE `agents`
  MODIFY `AgentID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `clients`
--
ALTER TABLE `clients`
  MODIFY `ClientID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `offices`
--
ALTER TABLE `offices`
  MODIFY `OfficeID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `properties`
--
ALTER TABLE `properties`
  MODIFY `PropertyID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `sales`
--
ALTER TABLE `sales`
  MODIFY `SaleID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `sales`
--
ALTER TABLE `sales`
  ADD CONSTRAINT `sales_ibfk_1` FOREIGN KEY (`PropertyID`) REFERENCES `properties` (`PropertyID`),
  ADD CONSTRAINT `sales_ibfk_2` FOREIGN KEY (`ClientID`) REFERENCES `clients` (`ClientID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
