/*
Navicat MySQL Data Transfer

Source Server         : 127.0.0.1
Source Server Version : 50717
Source Host           : localhost:3306
Source Database       : osu

Target Server Type    : MYSQL
Target Server Version : 50717
File Encoding         : 65001

Date: 2017-09-01 17:49:58
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) DEFAULT NULL,
  `qq` char(15) DEFAULT NULL,
  `osuid` varchar(30) DEFAULT NULL,
  `groupid` char(15) DEFAULT NULL,
  `osuname` varchar(30) DEFAULT NULL,
  `money` int(11) NOT NULL DEFAULT '0',
  `bagnum` int(11) NOT NULL DEFAULT '5',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_qq` (`qq`,`groupid`),
  KEY `idx_name` (`osuname`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('1', 'inter shuai dao le', '405622418', '8505303', '614892339', '-interesting-', '0', '5');
INSERT INTO `user` VALUES ('2', '提前AFK的kazami', '2930081217', '10632599', '614892339', 'kazami_sonogam', '0', '5');
INSERT INTO `user` VALUES ('3', '你们永远的双刀ChongZi（两年后见啦！）', '920979541', '10020329', '614892339', 'taoyuan_naimai', '0', '5');
INSERT INTO `user` VALUES ('4', 'whirLeeve【咸鱼】', '178039743', '10026750', '614892339', 'whirLeeve', '0', '5');
INSERT INTO `user` VALUES ('5', '【毕业啦】IKenned', '929555357', '4714998', '614892339', 'ikenned', '0', '5');
INSERT INTO `user` VALUES ('6', '【賣调料指導】散落的灰尘', '77808542', '9357088', '614892339', 'shiqikuangsanzz', '0', '5');
INSERT INTO `user` VALUES ('8', '【半蠢鼠玩家】AsrielTW', '1794790664', '8872382', '614892339', 'AsrielTW', '0', '5');
INSERT INTO `user` VALUES ('9', 'my idol heisiban', '1004121460', '9453012', '614892339', '-inter-', '0', '5');
INSERT INTO `user` VALUES ('10', 'umi9sonoda', '921689419', '8426327', '614892339', 'umi9sonoda', '0', '5');
INSERT INTO `user` VALUES ('11', 'dalouBot', '1677323371', '8190582', '614892339', 'louxinye', '0', '5');
INSERT INTO `user` VALUES ('12', '【賣肉指導】My Angel Inui Sana', '630060047', '9043058', '614892339', 'cyclc', '0', '5');
INSERT INTO `user` VALUES ('13', '大家好，我是萌萌的小灰尘～', '2541721178', '3668072', '614892339', 'heisiban', '0', '5');
INSERT INTO `user` VALUES ('14', 'my angle xiaoxu', '1779167916', '7120784', '614892339', 'COOLMILK123', '0', '5');
INSERT INTO `user` VALUES ('15', '鬼知道是谁', '670804973', '9755808', '614892339', 'Sonoaoi', '0', '5');
INSERT INTO `user` VALUES ('16', '被殴打的人', '1044827240', '10059047', '614892339', 'longkong', '0', '5');
INSERT INTO `user` VALUES ('17', '沙丁鱼_frozensardine', '1272278915', '10053352', '614892339', '_frozensardine', '0', '5');
INSERT INTO `user` VALUES ('18', '【HD no pp指导】84461810', '431600414', '9761752', '614892339', '84461810', '0', '5');
INSERT INTO `user` VALUES ('23', '【指导】louxinye', '1061566571', '8190582', '614892339', 'louxinye', '0', '5');
INSERT INTO `user` VALUES ('24', 'emilia的爸爸', '1023406736', '6703655', '614892339', 'pandacattle', '0', '5');
INSERT INTO `user` VALUES ('25', 'Truth you left', '3363569388', '3388375', '614892339', 'Truth', '0', '5');
INSERT INTO `user` VALUES ('27', '【全场acc最菜】Jack_Wang_', '2482000231', '9975427', '614892339', 'Jack_Wang_', '0', '5');
INSERT INTO `user` VALUES ('30', 'AllenBerserker', '1548379163', '9528607', '614892339', 'AllenBerserker', '0', '5');
INSERT INTO `user` VALUES ('31', 'Yaber', '617284805', '351028', '614892339', 'Piero', '0', '5');
