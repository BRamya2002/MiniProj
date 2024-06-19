/*
SQLyog Community v13.1.7 (64 bit)
MySQL - 5.5.30 : Database - vtpip09_2022
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`vtpip09_2022` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `vtpip09_2022`;

/*Table structure for table `doctor` */

DROP TABLE IF EXISTS `doctor`;

CREATE TABLE `doctor` (
  `Name` varchar(255) DEFAULT NULL,
  `Email` varchar(255) NOT NULL,
  `Password` varchar(255) DEFAULT NULL,
  `Mobile` varchar(255) DEFAULT NULL,
  `Department` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `dpre` */

DROP TABLE IF EXISTS `dpre`;

CREATE TABLE `dpre` (
  `Id` int(11) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `Medicine` varchar(255) DEFAULT NULL,
  `Bed` varchar(255) DEFAULT NULL,
  `Food` varchar(255) DEFAULT NULL,
  `bstatus` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `predictions` */

DROP TABLE IF EXISTS `predictions`;

CREATE TABLE `predictions` (
  `Age` int(11) DEFAULT NULL,
  `Gender` varchar(255) DEFAULT NULL,
  `NoDays` int(11) DEFAULT NULL,
  `Precautions` longtext,
  `Food` longtext
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `sreport` */

DROP TABLE IF EXISTS `sreport`;

CREATE TABLE `sreport` (
  `Id` int(11) DEFAULT NULL,
  `Name` varchar(255) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `DocId` varchar(255) DEFAULT NULL,
  `FileName` varchar(255) DEFAULT NULL,
  `Key1` varchar(255) DEFAULT NULL,
  `Dreq` varchar(255) DEFAULT NULL,
  `Ureq` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `Name` varchar(255) DEFAULT NULL,
  `Email` varchar(255) NOT NULL,
  `Password` varchar(255) DEFAULT NULL,
  `Mobile` varchar(255) DEFAULT NULL,
  `Location` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `userdet` */

DROP TABLE IF EXISTS `userdet`;

CREATE TABLE `userdet` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `Symptoms` varchar(255) DEFAULT NULL,
  `DocId` varchar(255) DEFAULT NULL,
  `Status` varchar(255) DEFAULT NULL,
  KEY `Id` (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
