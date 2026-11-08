-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Nov 08, 2026 at 11:28 PM
-- Server version: 8.4.3
-- PHP Version: 8.3.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pizzeria_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `detalle_pedido`
--

CREATE TABLE `detalle_pedido` (
  `id_detalle` int NOT NULL,
  `id_pedido` int NOT NULL,
  `tamano` varchar(20) NOT NULL,
  `cantidad` int NOT NULL,
  `precio_tamano` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `detalle_pedido`
--

INSERT INTO `detalle_pedido` (`id_detalle`, `id_pedido`, `tamano`, `cantidad`, `precio_tamano`, `subtotal`) VALUES
(1, 1, 'Mediana', 2, 80.00, 200.00),
(2, 2, 'Mediana', 2, 80.00, 200.00),
(3, 2, 'Grande', 1, 120.00, 130.00),
(4, 3, 'Mediana', 2, 80.00, 200.00),
(5, 4, 'Chica', 1, 40.00, 60.00),
(6, 4, 'Mediana', 1, 80.00, 100.00),
(7, 5, 'Mediana', 3, 80.00, 300.00);

-- --------------------------------------------------------

--
-- Table structure for table `ingredientes_detalle`
--

CREATE TABLE `ingredientes_detalle` (
  `id_ingrediente` int NOT NULL,
  `id_detalle` int NOT NULL,
  `ingrediente` varchar(50) NOT NULL,
  `precio` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `ingredientes_detalle`
--

INSERT INTO `ingredientes_detalle` (`id_ingrediente`, `id_detalle`, `ingrediente`, `precio`) VALUES
(1, 1, 'Jamón', 10.00),
(2, 1, 'Piña', 10.00),
(3, 2, 'Jamón', 10.00),
(4, 2, 'Piña', 10.00),
(5, 3, 'Champiñones', 10.00),
(6, 4, 'Jamón', 10.00),
(7, 4, 'Piña', 10.00),
(8, 5, 'Jamón', 10.00),
(9, 5, 'Champiñones', 10.00),
(10, 6, 'Jamón', 10.00),
(11, 6, 'Piña', 10.00),
(12, 7, 'Jamón', 10.00),
(13, 7, 'Champiñones', 10.00);

-- --------------------------------------------------------

--
-- Table structure for table `pedidos`
--

CREATE TABLE `pedidos` (
  `id_pedido` int NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `direccion` varchar(200) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `fecha_pedido` date NOT NULL,
  `total` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `pedidos`
--

INSERT INTO `pedidos` (`id_pedido`, `nombre`, `direccion`, `telefono`, `fecha_pedido`, `total`) VALUES
(1, 'Maria Juarez', '5 de mayo', '477-787-23', '2026-11-07', 200.00),
(2, 'Carlos Ramirez', 'Centro', '4771234567', '2026-11-07', 330.00),
(3, 'Prueba Validacion', 'Centro', '4771234567', '2026-11-08', 200.00),
(4, 'Lucia Fuentes', '10 de mayo', '477-789-2534', '2026-11-08', 160.00),
(5, 'Athenea Lopez', 'Leon moderno', '477-456-1237', '2026-11-08', 300.00);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `detalle_pedido`
--
ALTER TABLE `detalle_pedido`
  ADD PRIMARY KEY (`id_detalle`),
  ADD KEY `id_pedido` (`id_pedido`);

--
-- Indexes for table `ingredientes_detalle`
--
ALTER TABLE `ingredientes_detalle`
  ADD PRIMARY KEY (`id_ingrediente`),
  ADD KEY `id_detalle` (`id_detalle`);

--
-- Indexes for table `pedidos`
--
ALTER TABLE `pedidos`
  ADD PRIMARY KEY (`id_pedido`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `detalle_pedido`
--
ALTER TABLE `detalle_pedido`
  MODIFY `id_detalle` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `ingredientes_detalle`
--
ALTER TABLE `ingredientes_detalle`
  MODIFY `id_ingrediente` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `pedidos`
--
ALTER TABLE `pedidos`
  MODIFY `id_pedido` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `detalle_pedido`
--
ALTER TABLE `detalle_pedido`
  ADD CONSTRAINT `detalle_pedido_ibfk_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedidos` (`id_pedido`);

--
-- Constraints for table `ingredientes_detalle`
--
ALTER TABLE `ingredientes_detalle`
  ADD CONSTRAINT `ingredientes_detalle_ibfk_1` FOREIGN KEY (`id_detalle`) REFERENCES `detalle_pedido` (`id_detalle`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
