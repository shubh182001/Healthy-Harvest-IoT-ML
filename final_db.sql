/*
SQLyog Community Edition- MySQL GUI v7.01 
MySQL - 5.0.27-community-nt : Database - cropnew
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`cropnew` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `cropnew`;

/*Table structure for table `pred_data` */

DROP TABLE IF EXISTS `pred_data`;

CREATE TABLE `pred_data` (
  `Did` int(255) NOT NULL auto_increment,
  `N_val` varchar(255) default NULL,
  `P_val` varchar(255) default NULL,
  `K_val` varchar(255) default NULL,
  `Temp_val` varchar(255) default NULL,
  `Humid_val` varchar(255) default NULL,
  `Ph_val` varchar(255) default NULL,
  `Moist_val` varchar(255) default NULL,
  `Prediction` varchar(255) default NULL,
  PRIMARY KEY  (`Did`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `pred_data` */

insert  into `pred_data`(`Did`,`N_val`,`P_val`,`K_val`,`Temp_val`,`Humid_val`,`Ph_val`,`Moist_val`,`Prediction`) values (1,'90','33','86','33.00','74.00','4.12','98.700000000000003','mothbeans');

/*Table structure for table `userdetails` */

DROP TABLE IF EXISTS `userdetails`;

CREATE TABLE `userdetails` (
  `id` int(10) NOT NULL auto_increment,
  `name` varchar(40) NOT NULL,
  `email` varchar(40) NOT NULL,
  `password` varchar(40) NOT NULL,
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `userdetails` */

insert  into `userdetails`(`id`,`name`,`email`,`password`) values (1,'a','a@gmail.com','a'),(2,'shubh','shubh18.dhar@gmail.com','fypfyp');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
