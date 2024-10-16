


DROP TABLE IF EXISTS `customers`;

CREATE TABLE `customers` (
  `customerID` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`customerID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `customers` WRITE;

INSERT INTO `customers` VALUES (4,'khalid','0594460902','khalid@gmail.com'),(5,'oday','059123123','oday123@gmail.com');

UNLOCK TABLES;


