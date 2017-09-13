/*
Navicat MySQL Data Transfer

Source Server         : bii
Source Server Version : 50711
Source Host           : localhost:3306
Source Database       : osu

Target Server Type    : MYSQL
Target Server Version : 50711
File Encoding         : 65001

Date: 2017-09-13 08:35:04
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
) ENGINE=InnoDB AUTO_INCREMENT=178 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------
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
INSERT INTO `user` VALUES ('15', '鬼知道是谁，反正afk了', '670804973', '9755808', '614892339', 'Sonoaoi', '0', '5');
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
INSERT INTO `user` VALUES ('34', 'afk', '908604578', '6479079', '614892339', 'duoduo_123dong', '0', '5');
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
INSERT INTO `user` VALUES ('57', '觉', '2017642475', '9049939', '514661057', 'mafuyu_shiina', '0', '5');
INSERT INTO `user` VALUES ('58', 'mina love love', '873743955', '4783679', '514661057', 'jadelux', '0', '5');
INSERT INTO `user` VALUES ('59', 'my angle xiaoxu(37.5)', '1779167916', '7120784', '514661057', 'COOLMILK123', '0', '5');
INSERT INTO `user` VALUES ('61', 'AdorableCubCat', '1838698586', '2016586', '514661057', 'AdorableCubCat', '0', '5');
INSERT INTO `user` VALUES ('62', 'kahei0726', '3540422430', '3285324', '614892339', 'kahei0726', '0', '5');
INSERT INTO `user` VALUES ('63', 'kss233', '1169181371', '9296663', '614892339', 'kss233', '0', '5');
INSERT INTO `user` VALUES ('64', '【毕业】505369962', '505369962', '9903602', '614892339', '505369962', '0', '5');
INSERT INTO `user` VALUES ('65', '小葉Aok', '1719583076', '8826089', '614892339', 'Aok', '0', '5');
INSERT INTO `user` VALUES ('66', '[ctb]Last Place', '757772012', '253015', '614892339', 'Last_Place', '0', '5');
INSERT INTO `user` VALUES ('67', '蓝', '623055567', '8530700', '598918097', 'KyuubiRan', '0', '5');
INSERT INTO `user` VALUES ('68', '【quit w】taolex', '1239219529', '4489519', '614892339', 'taolex', '0', '5');
INSERT INTO `user` VALUES ('69', '【毕业】貓兔/Soraka', '2056380983', '6812680', '614892339', 'Soraka', '0', '5');
INSERT INTO `user` VALUES ('70', 'Endorfin.', '2655927663', '9386243', '514661057', '300yx', '0', '5');
INSERT INTO `user` VALUES ('71', 'umi9sonoda', '921689419', '8426327', '514661057', 'umi9sonoda', '0', '5');
INSERT INTO `user` VALUES ('72', 'ye__ow', '568532708', '2992539', '514661057', 'ye__ow', '0', '5');
INSERT INTO `user` VALUES ('73', 'AMelax', '1136084891', '8768183', '514661057', 'AMelax', '0', '5');
INSERT INTO `user` VALUES ('74', 'あもり', '670527749', '3132772', '598918097', 'amori', '0', '5');
INSERT INTO `user` VALUES ('75', 'AngeLIllya，求mu', '675737637', '1777162', '598918097', 'firebat92', '0', '5');
INSERT INTO `user` VALUES ('76', 'Totoriott', '943837838', '5967131', '598918097', 'totoriott', '0', '5');
INSERT INTO `user` VALUES ('77', '柳墨云河', '1693020481', '9445093', '598918097', 'yuanxi123', '0', '5');
INSERT INTO `user` VALUES ('78', 'hgxcxdg', '280485660', '5935141', '598918097', 'hgxcxdg', '0', '5');
INSERT INTO `user` VALUES ('79', 'abc', '805404829', '3635214', '598918097', 'vrainbow', '0', '5');
INSERT INTO `user` VALUES ('80', '【1800pp虚高1000pp】NucleophileAP', '604490178', '9237208', '614892339', 'NucleophileAP', '0', '5');
INSERT INTO `user` VALUES ('81', 'dullwolf', '1091569752', '2660718', '614892339', 'dullwolf', '0', '5');
INSERT INTO `user` VALUES ('82', 'lausdeo', '877618011', '6096283', '614892339', 'lausdeo', '0', '5');
INSERT INTO `user` VALUES ('84', '7Ark', '1265775896', '8978950', '614892339', '7Ark', '0', '5');
INSERT INTO `user` VALUES ('90', 'pwpouoqwq', '2073296145', '9799883', '614892339', 'pwpouoqwq', '0', '5');
INSERT INTO `user` VALUES ('91', 'a一年', '480988405', '8995648', '614892339', 'txy114114', '0', '5');
INSERT INTO `user` VALUES ('92', 'Isokaze', '981113321', '8567372', '614892339', 'Souji', '0', '5');
INSERT INTO `user` VALUES ('94', 'Alan', '1849304789', '10398767', '614892339', 'Alan_Chark', '0', '5');
INSERT INTO `user` VALUES ('95', 'Se Tsu Na', '1559449817', '6073139', '614892339', 'Se_Tsu_Na', '0', '5');
INSERT INTO `user` VALUES ('96', 'Great meat', '624467921', '3259615', '614892339', 'Great_meat', '0', '5');
INSERT INTO `user` VALUES ('97', 'dxrzxb期待mu', '2863286514', '6956592', '598918097', 'dxrzxb', '0', '5');
INSERT INTO `user` VALUES ('98', 'Thonking', '1730459893', '9781926', '598918097', 'Thonking', '0', '5');
INSERT INTO `user` VALUES ('99', '-Ninko', '2529839497', '7534323', '598918097', '-Ninko', '0', '5');
INSERT INTO `user` VALUES ('100', 'bug酱', '812035954', '3749808', '598918097', 'czhhws', '0', '5');
INSERT INTO `user` VALUES ('101', '君莫言', '2510797443', '8368247', '598918097', 'junmoyan', '0', '5');
INSERT INTO `user` VALUES ('102', '请叫我小p', '1131576371', '7375340', '598918097', 'Stein', '0', '5');
INSERT INTO `user` VALUES ('103', 'Candyland123 RXSO玩家', '1442104687', '9343961', '614892339', 'Candyland123', '0', '5');
INSERT INTO `user` VALUES ('104', '各位天台见', '1753364172', '1053938', '598918097', 'NAIVE', '0', '5');
INSERT INTO `user` VALUES ('105', 'カリーฅฅ', '374627945', '8012734', '598918097', 'curriescaz', '0', '5');
INSERT INTO `user` VALUES ('106', '铃', '857281217', '926614', '598918097', 'rinkon', '0', '5');
INSERT INTO `user` VALUES ('107', '罪孽深重のph', '823427288', '3394580', '598918097', 'phtry', '0', '5');
INSERT INTO `user` VALUES ('108', 'Dblife', '530802875', '8767628', '598918097', 'dblife', '0', '5');
INSERT INTO `user` VALUES ('109', '揺れるミイラ', '2241521134', '1243669', '598918097', 'yf_bmp', '0', '5');
INSERT INTO `user` VALUES ('110', 'http://osu.ppy.sh/u/6635629', '617539644', '6635629', '598918097', 'DurnTars', '0', '5');
INSERT INTO `user` VALUES ('111', 'ericgogo68', '1499881708', '1457224', '373591087', 'ericgogo68', '0', '5');
INSERT INTO `user` VALUES ('112', '魔都喝水传说', '1435754878', '4271875', '373591087', 'Storia', '0', '5');
INSERT INTO `user` VALUES ('115', '枔', '2873996258', '124493', '598918097', 'cookiezi', '0', '5');
INSERT INTO `user` VALUES ('116', '花~', '996832348', '1324906', '373591087', '[king]', '0', '5');
INSERT INTO `user` VALUES ('117', 'ikayas还在减肥', '2033672081', '124493', '598918097', 'cookiezi', '0', '5');
INSERT INTO `user` VALUES ('118', '有坂真白 Yipianyu', '653807170', '7210268', '598918097', 'Yipianyu', '0', '5');
INSERT INTO `user` VALUES ('119', '「     」', '2068150063', '7349259', '373591087', 'blankerss', '0', '5');
INSERT INTO `user` VALUES ('121', '语文99的二号', '1025806291', '3924736', '373591087', 'iamapen', '0', '5');
INSERT INTO `user` VALUES ('122', '什么都会一点的1……', '2740485236', '9568863', '598918097', 'Airon%209th', '0', '5');
INSERT INTO `user` VALUES ('123', 'ss-7', '3340483065', '6149313', '514661057', 'pata-mon', '0', '5');
INSERT INTO `user` VALUES ('124', 'Small_miao', '1773805744', '8771484', '514661057', 'Small_Miao', '0', '5');
INSERT INTO `user` VALUES ('125', '冬儿456', '490713945', '2472232', '514661057', 'donger456', '0', '5');
INSERT INTO `user` VALUES ('126', 'inter', '405622418', '8505303', '614892339', '-interesting-', '0', '5');
INSERT INTO `user` VALUES ('129', 'X Ray_', '2570246497', '8651959', '514661057', 'X%20Ray_', '0', '5');
INSERT INTO `user` VALUES ('130', 'Steal sister(萌新之王)', '553076664', '10516632', '614892339', 'Steal_sister', '0', '5');
INSERT INTO `user` VALUES ('131', 'usagiKokoa', '996005984', '6560592', '514661057', 'usagikokoa', '0', '5');
INSERT INTO `user` VALUES ('133', 'fxdqe(全群最弱)', '1037852407', '4113425', '614892339', 'fxdqe', '0', '5');
INSERT INTO `user` VALUES ('134', 'eanjc', '718379165', '9226555', '614892339', 'eanjc', '0', '5');
INSERT INTO `user` VALUES ('135', 'osu happy', '1766172533', '9580470', '614892339', 'osu_happy', '0', '5');
INSERT INTO `user` VALUES ('138', 'My Angel Yotsuko', '1004121460', '9453012', '514661057', '-inter-', '0', '5');
INSERT INTO `user` VALUES ('139', 'RichardMing', '982477544', '7680600', '614892339', 'RichardMing', '0', '5');
INSERT INTO `user` VALUES ('140', '需要太鼓玩家 Ca', '2875452763', '4850066', '614892339', 'can', '0', '5');
INSERT INTO `user` VALUES ('141', 'NXniihaubrony', '2579661526', '8404284', '614892339', 'NXniihaubrony', '0', '5');
INSERT INTO `user` VALUES ('142', '往往', '906234737', '9636933', '614892339', 'wz_unknown', '0', '5');
INSERT INTO `user` VALUES ('143', 'my angle 绿光[relax/auto指导]', '873743955', '4701649', '614892339', 'sinowwhite', '0', '5');
INSERT INTO `user` VALUES ('144', '191937704', '191937704', '5039669', '614892339', '191937704', '0', '5');
INSERT INTO `user` VALUES ('145', '@A@/异常\\_/游梦者\\', '2727670665', '7936691', '614892339', '7936691', '0', '5');
INSERT INTO `user` VALUES ('146', 'miaopasi2333', '3080710952', '9121525', '614892339', 'miaopasi2333', '0', '5');
INSERT INTO `user` VALUES ('147', '【被指导】bleatingsheep', '962549599', '6659067', '614892339', 'bleatingsheep', '0', '5');
INSERT INTO `user` VALUES ('149', 'Xue Lang', '1587912583', '10354097', '614892339', 'Xue_Lang', '0', '5');
INSERT INTO `user` VALUES ('151', '土罐子', '2922457316', '8259821', '614892339', 'tuguanz', '0', '5');
INSERT INTO `user` VALUES ('152', 'nsm285866172', '285866172', '6942546', '614892339', 'nsm285866172', '0', '5');
INSERT INTO `user` VALUES ('153', 'CappuccinoChino', '759872175', '8919574', '614892339', 'CappuccinoChino', '0', '5');
INSERT INTO `user` VALUES ('154', 'Auver', '774357315', '8535398', '614892339', 'Auver', '0', '5');
INSERT INTO `user` VALUES ('155', 'wqh1996', '408749098', '4716336', '614892339', 'wqh1996', '0', '5');
INSERT INTO `user` VALUES ('157', 'dicskb122', '547519621', '9314367', '514661057', 'dicskb122', '0', '5');
INSERT INTO `user` VALUES ('158', 'happy NekoMinto', '903094802', '8951100', '514661057', '-NekoMinto-', '0', '5');
INSERT INTO `user` VALUES ('159', 'Brave New World', '570639703', '9236518', '514661057', 'brave_new_world', '0', '5');
INSERT INTO `user` VALUES ('160', 'Makise Kurisu', '790532173', '4712906', '514661057', 'laozishi12dora', '0', '5');
INSERT INTO `user` VALUES ('161', '求连打图', '1316740753', '8368974', '514661057', 'Hibikom', '0', '5');
INSERT INTO `user` VALUES ('162', '24fps', '12708531', '9991807', '614892339', '24fps', '0', '5');
INSERT INTO `user` VALUES ('163', 'KAHUB', '125647408', '9164371', '514661057', 'KAHUB', '0', '5');
INSERT INTO `user` VALUES ('164', '没有pp，下一个！！！', '359603915', '1014104', '514661057', 'maruOUQ', '0', '5');
INSERT INTO `user` VALUES ('165', 'Cassssss', '1090880452', '7224102', '614892339', 'Cassssss', '0', '5');
INSERT INTO `user` VALUES ('166', 'elchxyrlia', '2655927663', '1722835', '614892339', 'elchxyrlia', '0', '5');
INSERT INTO `user` VALUES ('167', 'meiyouqian', '1400507607', '10201145', '614892339', 'meiyouqian', '0', '5');
INSERT INTO `user` VALUES ('168', 'pachuri_norejji', '1156477720', '7974004', '614892339', 'pachuri_norejji', '0', '5');
INSERT INTO `user` VALUES ('169', 'cq980125', '965469790', '8772590', '614892339', 'cq980125', '0', '5');
INSERT INTO `user` VALUES ('171', '612242018(RSI AFK）', '2323797615', '8828725', '614892339', '612242018', '0', '5');
INSERT INTO `user` VALUES ('172', 'Inf1nity7788', '2723108206', '10697254', '614892339', 'Inf1nity7788', '0', '5');
INSERT INTO `user` VALUES ('175', '对不起我最菜', '183392679', '7088526', '614892339', 'ikanyai', '0', '5');
INSERT INTO `user` VALUES ('176', '原始人HuaLeGeJiBa', '2730304711', '9404646', '614892339', 'hualegejiba', '0', '5');
INSERT INTO `user` VALUES ('177', 'Eagle in Dark(馒头)', '1019106314', '5384725', '614892339', 'Eagle', '0', '5');
