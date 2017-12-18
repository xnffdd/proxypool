/*
Navicat MySQL Data Transfer

Source Server         : mysql_local
Source Server Version : 50636
Source Host           : 127.0.0.1:3306
Source Database       : test

Target Server Type    : MYSQL
Target Server Version : 50636
File Encoding         : 65001

Date: 2017-12-14 16:18:30
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for proxy
-- ----------------------------
DROP TABLE IF EXISTS `proxy`;
CREATE TABLE `proxy` (
  `protocol` varchar(255) DEFAULT NULL,
  `host` varchar(255) DEFAULT NULL,
  `port` varchar(255) DEFAULT NULL,
  `anonymity` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `export_address` varchar(255) DEFAULT NULL,
  `response_time` float DEFAULT NULL,
  `from` varchar(255) DEFAULT NULL,
  `check_time` datetime DEFAULT NULL,
  `grab_time` datetime DEFAULT NULL,
  UNIQUE KEY `uni` (`protocol`,`host`,`port`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
