"""
-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 25-09-2019 a las 16:43:47
-- Versión del servidor: 10.1.35-MariaDB
-- Versión de PHP: 7.2.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `crud`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categoria`
--

CREATE TABLE `categoria` (
  `idCategoria` int(3) NOT NULL,
  `nombreCategoria` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `departamento`
--

CREATE TABLE `departamento` (
  `idDepartamento` int(3) NOT NULL,
  `nombreDepartamento` varchar(30) DEFAULT NULL,
  `idSucursal` int(3) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleado`
--

CREATE TABLE `empleado` (
  `idEmpleado` int(3) NOT NULL,
  `nombreEmpleado` varchar(50) DEFAULT NULL,
  `apellidoEmpleado` varchar(50) DEFAULT NULL,
  `idSucursal` int(3) DEFAULT NULL,
  `idDepartamento` int(3) DEFAULT NULL,
  `job_id` int(3) DEFAULT NULL,
  `correo` varchar(150) DEFAULT NULL,
  `pass` varchar(300) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto`
--

CREATE TABLE `producto` (
  `idProducto` int(3) NOT NULL,
  `nombreProducto` varchar(50) DEFAULT NULL,
  `precio` decimal(6,2) DEFAULT NULL,
  `idSucursal` int(3) DEFAULT NULL,
  `idCategoria` int(3) DEFAULT NULL,
  `idProveedor` int(3) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedor`
--

CREATE TABLE `proveedor` (
  `idProveedor` int(3) NOT NULL,
  `nombreProveedor` varchar(50) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `puestos`
--

CREATE TABLE `puestos` (
  `job_id` int(3) NOT NULL,
  `puesto` varchar(35) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sucursal`
--

CREATE TABLE `sucursal` (
  `idSucursal` int(3) NOT NULL,
  `nombreSucursal` varchar(30) DEFAULT NULL,
  `direccion` varchar(40) DEFAULT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `codigoPostal` int(5) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `categoria`
--
ALTER TABLE `categoria`
  ADD PRIMARY KEY (`idCategoria`);

--
-- Indices de la tabla `departamento`
--
ALTER TABLE `departamento`
  ADD PRIMARY KEY (`idDepartamento`),
  ADD KEY `fk_depto_suc` (`idSucursal`);

--
-- Indices de la tabla `empleado`
--
ALTER TABLE `empleado`
  ADD PRIMARY KEY (`idEmpleado`),
  ADD KEY `fk_emp_suc` (`idSucursal`),
  ADD KEY `fk_emp_depto` (`idDepartamento`),
  ADD KEY `fk_emp_puesto` (`job_id`);

--
-- Indices de la tabla `producto`
--
ALTER TABLE `producto`
  ADD PRIMARY KEY (`idProducto`),
  ADD KEY `fk_prod_suc` (`idSucursal`),
  ADD KEY `fk_prod_cat` (`idCategoria`),
  ADD KEY `fk_prod_prov` (`idProveedor`);

--
-- Indices de la tabla `proveedor`
--
ALTER TABLE `proveedor`
  ADD PRIMARY KEY (`idProveedor`);

--
-- Indices de la tabla `puestos`
--
ALTER TABLE `puestos`
  ADD PRIMARY KEY (`job_id`);

--
-- Indices de la tabla `sucursal`
--
ALTER TABLE `sucursal`
  ADD PRIMARY KEY (`idSucursal`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `categoria`
--
ALTER TABLE `categoria`
  MODIFY `idCategoria` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `departamento`
--
ALTER TABLE `departamento`
  MODIFY `idDepartamento` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `empleado`
--
ALTER TABLE `empleado`
  MODIFY `idEmpleado` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `producto`
--
ALTER TABLE `producto`
  MODIFY `idProducto` int(3) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `proveedor`
--
ALTER TABLE `proveedor`
  MODIFY `idProveedor` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `sucursal`
--
ALTER TABLE `sucursal`
  MODIFY `idSucursal` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `departamento`
--
ALTER TABLE `departamento`
  ADD CONSTRAINT `fk_depto_suc` FOREIGN KEY (`idSucursal`) REFERENCES `sucursal` (`idSucursal`);

--
-- Filtros para la tabla `empleado`
--
ALTER TABLE `empleado`
  ADD CONSTRAINT `fk_emp_depto` FOREIGN KEY (`idDepartamento`) REFERENCES `departamento` (`idDepartamento`),
  ADD CONSTRAINT `fk_emp_suc` FOREIGN KEY (`idSucursal`) REFERENCES `sucursal` (`idSucursal`);

--
-- Filtros para la tabla `producto`
--
ALTER TABLE `producto`
  ADD CONSTRAINT `fk_prod_cat` FOREIGN KEY (`idCategoria`) REFERENCES `categoria` (`idCategoria`),
  ADD CONSTRAINT `fk_prod_prov` FOREIGN KEY (`idProveedor`) REFERENCES `proveedor` (`idProveedor`),
  ADD CONSTRAINT `fk_prod_suc` FOREIGN KEY (`idSucursal`) REFERENCES `sucursal` (`idSucursal`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;



CREATE OR REPLACE VIEW p_view AS
SELECT p.idProducto as id, p.nombreProducto as Producto, p.precio as Precio, s.nombreSucursal as Sucursal, c.nombreCategoria as Categoria, pr.nombreProveedor as Proveedor 
FROM producto p, sucursal s, categoria c, proveedor pr 
WHERE p.idSucursal = s.idSucursal AND p.idCategoria = c.idCategoria AND p.idProveedor = pr.idProveedor ORDER BY p.idProducto;

CREATE OR REPLACE VIEW c_view AS
SELECT idCategoria as id, nombreCategoria as Categoria 
FROM categoria
ORDER BY idCategoria;

CREATE OR REPLACE VIEW s_view as
SELECT idSucursal as id, nombreSucursal as Sucursal, direccion, estado, codigoPostal as cp 
FROM sucursal;


"""
