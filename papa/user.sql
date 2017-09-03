/*
Navicat MySQL Data Transfer

Source Server         : bii
Source Server Version : 50711
Source Host           : localhost:3306
Source Database       : osu

Target Server Type    : MYSQL
Target Server Version : 50711
File Encoding         : 65001

Date: 2017-09-04 00:40:02
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `user`
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
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8;

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
INSERT INTO `user` VALUES ('9', 'my idol heisiban', '1004121460', '10777307', '614892339', '-int-', '0', '5');
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
INSERT INTO `user` VALUES ('32', '【伪指导？】Sisters10086', '1442455430', '3665920', '614892339', 'Sisters10086', '0', '5');
INSERT INTO `user` VALUES ('34', '进不了进阶群的垃圾duoduo', '908604578', '6479079', '614892339', 'duoduo_123dong', '0', '5');
INSERT INTO `user` VALUES ('35', 'Hermit【请叫我四萝莉】', '1985958893', '7175234', '614892339', '-Hermit-', '0', '5');
INSERT INTO `user` VALUES ('36', 'runa love love', '1587912578', '4602934', '514661057', 'Yamiko', '0', '5');
INSERT INTO `user` VALUES ('37', '练习hr中', '1277818495', '7009664', '514661057', 'my_angel_kotori', '0', '5');
INSERT INTO `user` VALUES ('38', '-FKai-', '756475791', '10083452', '514661057', '-FKai-', '0', '5');
INSERT INTO `user` VALUES ('39', '资深小蜗牛', '371169640', '5844899', '598918097', 'BiusyChinese', '0', '5');
INSERT INTO `user` VALUES ('40', 'χ_ƒιяєƻ33', '2071833095', '4013194', '598918097', 'X_fire233', '0', '5');
INSERT INTO `user` VALUES ('41', 'kpx', '1683370840', '6709675', '598918097', 'kpx-x', '0', '5');
INSERT INTO `user` VALUES ('43', 'Sodacooky', '523379653', '7603551', '598918097', 'Sodacooky', '0', '5');
INSERT INTO `user` VALUES ('45', '暗蓝', '2464447425', '8118374', '598918097', 'Futamaru_Kururi', '0', '5');
INSERT INTO `user` VALUES ('46', 'Boom.xE', '1514184199', '954557', '614892339', 'emertxe', '0', '5');
INSERT INTO `user` VALUES ('47', 'AFK状态 JRC888（菜逼）', '847238204', '9569188', '614892339', 'jrc888', '0', '5');
INSERT INTO `user` VALUES ('48', 'StarTemplar', '1376662442', '8795096', '614892339', 'startemplar', '0', '5');
INSERT INTO `user` VALUES ('50', '-xiaoxu-（叫我小绪）', '507989594', '10398689', '614892339', '-xiaoxu-', '0', '5');
INSERT INTO `user` VALUES ('51', '水滴(Marxtonwater)', '948369800', '1425538', '614892339', 'Marxtonwater', '0', '5');
INSERT INTO `user` VALUES ('52', '【丹阳】Sakura miku（我今天fc音乐工厂没)', '1149483077', '1698898', '514661057', 'Sakura_miku', '0', '5');
INSERT INTO `user` VALUES ('53', '-NekO- | My angel vita', '2429299722', '7183040', '514661057', '-NekO-', '0', '5');
INSERT INTO `user` VALUES ('54', 'C8N16O32 | 我永远支持dalou', '546748348', '7038366', '514661057', 'C8N16O32', '0', '5');
INSERT INTO `user` VALUES ('55', 'Cola kun', '1065896632', '7555859', '514661057', 'Cola_kun', '0', '5');
INSERT INTO `user` VALUES ('56', '【A一年】', '77808542', '9357088', '514661057', 'shiqikuangsanzz', '0', '5');
INSERT INTO `user` VALUES ('57', '觉', '2017642475', '86852', '514661057', 'mafuyu', '0', '5');
INSERT INTO `user` VALUES ('58', 'SinowWhite', '873743955', '4701649', '514661057', 'sinowwhite', '0', '5');
INSERT INTO `user` VALUES ('59', 'my angle xiaoxu(37.5)', '1779167916', '7120784', '514661057', 'COOLMILK123', '0', '5');
INSERT INTO `user` VALUES ('61', 'AdorableCubCat', '1838698586', '2016586', '514661057', 'AdorableCubCat', '0', '5');
INSERT INTO `user` VALUES ('62', 'kahei0726', '3540422430', '3285324', '614892339', 'kahei0726', '0', '5');
INSERT INTO `user` VALUES ('63', 'kss233', '1169181371', '9296663', '614892339', 'kss233', '0', '5');
INSERT INTO `user` VALUES ('64', '【毕业】505369962', '505369962', '9903602', '614892339', '505369962', '0', '5');
INSERT INTO `user` VALUES ('65', '小葉Aok', '1719583076', '8826089', '614892339', 'Aok', '0', '5');
INSERT INTO `user` VALUES ('66', '[ctb]Last Place', '757772012', '253015', '614892339', 'Last_Place', '0', '5');
