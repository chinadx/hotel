/*
Navicat MySQL Data Transfer

Source Server         : local-root
Source Server Version : 50525
Source Host           : localhost:3306
Source Database       : spider

Target Server Type    : MYSQL
Target Server Version : 50525
File Encoding         : 65001

Date: 2016-10-28 18:12:37
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for building_anjuke
-- ----------------------------
DROP TABLE IF EXISTS `building_anjuke`;
CREATE TABLE `building_anjuke` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '唯一编码',
  `building_no` varchar(20) NOT NULL COMMENT '安居客编号',
  `name` varchar(60) NOT NULL COMMENT '名称',
  `city` varchar(20) NOT NULL COMMENT '城市',
  `address` varchar(60) NOT NULL COMMENT '地址',
  `type` varchar(60) DEFAULT NULL COMMENT '类型',
  `fee` varchar(60) DEFAULT NULL COMMENT '物业费',
  `floor` varchar(60) DEFAULT NULL COMMENT '楼层',
  `construct_date` varchar(60) DEFAULT NULL COMMENT '竣工年月',
  `detail` varchar(100) DEFAULT NULL COMMENT '详情链接',
  `pic` varchar(100) DEFAULT NULL COMMENT '图片',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_building_anjuke_bn` (`building_no`)
) ENGINE=InnoDB AUTO_INCREMENT=30631 DEFAULT CHARSET=utf8 COMMENT='安居客写字楼信息';

-- ----------------------------
-- Table structure for calcu
-- ----------------------------
DROP TABLE IF EXISTS `calcu`;
CREATE TABLE `calcu` (
  `hotel` varchar(60) DEFAULT NULL,
  `room` varchar(60) DEFAULT NULL,
  `max_p` int(11) DEFAULT NULL,
  `min_p` int(11) DEFAULT NULL,
  `avg_p` int(11) DEFAULT NULL,
  `minus` int(11) DEFAULT NULL,
  `rate` double(12,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for cbd_elong
-- ----------------------------
DROP TABLE IF EXISTS `cbd_elong`;
CREATE TABLE `cbd_elong` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `city` varchar(20) NOT NULL,
  `name` varchar(60) NOT NULL,
  `longitude` decimal(10,6) NOT NULL,
  `latitude` decimal(10,6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1024 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for elong_link
-- ----------------------------
DROP TABLE IF EXISTS `elong_link`;
CREATE TABLE `elong_link` (
  `link` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for hotel_elong
-- ----------------------------
DROP TABLE IF EXISTS `hotel_elong`;
CREATE TABLE `hotel_elong` (
  `id` varchar(11) NOT NULL COMMENT '酒店编号',
  `name` varchar(80) DEFAULT NULL COMMENT '酒店名',
  `title` varchar(256) DEFAULT NULL COMMENT '标题',
  `phone` varchar(60) DEFAULT NULL COMMENT '电话',
  `city` varchar(20) DEFAULT NULL COMMENT '城市',
  `city_code` varchar(20) DEFAULT NULL COMMENT '城市代码',
  `city_pinyin` varchar(20) DEFAULT NULL COMMENT '城市拼音',
  `district` varchar(20) DEFAULT NULL COMMENT '区县',
  `address` varchar(128) DEFAULT NULL COMMENT '地址',
  `longitude` decimal(10,6) DEFAULT NULL COMMENT '经度',
  `latitude` decimal(10,6) DEFAULT NULL COMMENT '纬度',
  `cbd` varchar(80) DEFAULT NULL COMMENT '商圈名',
  `star` varchar(20) DEFAULT NULL COMMENT '星级',
  `description` varchar(2048) DEFAULT NULL COMMENT '描述',
  `detail_url` varchar(256) DEFAULT NULL COMMENT '详情链接',
  `pic_url` varchar(256) DEFAULT NULL COMMENT '头图链接',
  `price` int(11) DEFAULT '0' COMMENT '最低价',
  `point` int(11) DEFAULT '0' COMMENT '好评率',
  `score` decimal(2,1) DEFAULT NULL COMMENT '评分',
  `rooms` int(11) DEFAULT '0' COMMENT '房间数量',
  `pics` int(11) DEFAULT '0' COMMENT '图片数量',
  `facilities` int(11) DEFAULT '0' COMMENT '设施数量',
  `try_times` int(11) DEFAULT '0' COMMENT '重试次数',
  `syn_flag` varchar(1) DEFAULT 'Y' COMMENT '是否同步',
  `create_time` datetime DEFAULT NULL,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_hotel_elong_tt` (`create_time`) USING BTREE,
  KEY `idx_hotel_elong_r` (`rooms`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for hotel_elong_pics
-- ----------------------------
DROP TABLE IF EXISTS `hotel_elong_pics`;
CREATE TABLE `hotel_elong_pics` (
  `hotel_id` varchar(11) NOT NULL COMMENT '酒店编号',
  `src` varchar(100) NOT NULL COMMENT '图片链接',
  `orders` int(11) NOT NULL COMMENT '序号'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for lianjia_zufang_room
-- ----------------------------
DROP TABLE IF EXISTS `lianjia_zufang_room`;
CREATE TABLE `lianjia_zufang_room` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '唯一标识',
  `room_id` varchar(12) NOT NULL COMMENT '房型编号',
  `room_small_href` varchar(256) DEFAULT NULL COMMENT '房型缩略图',
  `room_detail_url` varchar(256) DEFAULT NULL COMMENT '房型详情地址',
  `room_detail_title` varchar(256) DEFAULT NULL COMMENT '详情页面的标题名称',
  `city` varchar(20) DEFAULT NULL COMMENT '归属城市',
  `district` varchar(20) DEFAULT NULL COMMENT '归属地区',
  `cbd` varchar(60) DEFAULT NULL COMMENT '归属商圈',
  `col_where` varchar(256) DEFAULT NULL COMMENT '位置',
  `coordinate_x` decimal(10,6) DEFAULT NULL COMMENT '坐标经度',
  `coordinate_y` decimal(10,6) DEFAULT NULL COMMENT '坐标维度',
  `zone` varchar(10) DEFAULT NULL COMMENT '室厅',
  `meters` varchar(10) DEFAULT NULL COMMENT '平米',
  `price` varchar(10) DEFAULT NULL COMMENT '价格(元/月)',
  `col_look` varchar(10) DEFAULT NULL COMMENT '几人看过房',
  `tags` varchar(256) DEFAULT NULL COMMENT '标签',
  `room_detail_sub_title` varchar(256) DEFAULT NULL COMMENT '副标题名称',
  `price_tag` varchar(256) DEFAULT NULL COMMENT '价格标签',
  `zf_room` varchar(256) DEFAULT NULL COMMENT '租房信息',
  `base_content` varchar(256) DEFAULT NULL COMMENT '基本属性',
  `feature_tag` varchar(256) DEFAULT NULL COMMENT '房源特色标签',
  `feature_content` varchar(512) DEFAULT NULL COMMENT '房源特色内容',
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=60616 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for lianjia_zufang_room_img
-- ----------------------------
DROP TABLE IF EXISTS `lianjia_zufang_room_img`;
CREATE TABLE `lianjia_zufang_room_img` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '唯一标识',
  `room_id` varchar(12) NOT NULL COMMENT '房型编号',
  `img_src` varchar(256) DEFAULT NULL COMMENT '房型缩略图',
  `img_desc` varchar(256) DEFAULT NULL COMMENT '房型详情地址',
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=437589 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for proxy_ip
-- ----------------------------
DROP TABLE IF EXISTS `proxy_ip`;
CREATE TABLE `proxy_ip` (
  `ip` varchar(50) NOT NULL COMMENT 'IP',
  `port` varchar(10) NOT NULL COMMENT 'PORT',
  `city` varchar(50) DEFAULT NULL COMMENT '归属城市',
  `protocl` varchar(10) DEFAULT NULL COMMENT '协议HTTP/HTTPS',
  `speed` decimal(10,3) DEFAULT NULL COMMENT '速度',
  `resp` decimal(10,3) DEFAULT NULL COMMENT '连接速度',
  `durance` decimal(10,2) DEFAULT NULL COMMENT '生存时间',
  `get_time` datetime DEFAULT NULL COMMENT '探测时间',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `try_times` int(11) DEFAULT '0' COMMENT '重试次数',
  `success_num` int(11) DEFAULT '0',
  PRIMARY KEY (`ip`,`port`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for room_elong
-- ----------------------------
DROP TABLE IF EXISTS `room_elong`;
CREATE TABLE `room_elong` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '房型编号',
  `hotel_id` varchar(11) NOT NULL COMMENT '酒店编号',
  `name` varchar(30) NOT NULL COMMENT '房型名称',
  `size` varchar(20) DEFAULT NULL COMMENT '面积',
  `bed` varchar(20) DEFAULT NULL COMMENT '床型',
  `price` int(11) DEFAULT NULL COMMENT '价格',
  `pic` varchar(100) DEFAULT NULL COMMENT '房型图片',
  `full` varchar(6) DEFAULT '0' COMMENT '1满房；0有房',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `pk_room_elong` (`hotel_id`,`name`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=230780 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for room_elong_price
-- ----------------------------
DROP TABLE IF EXISTS `room_elong_price`;
CREATE TABLE `room_elong_price` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `room_id` int(11) NOT NULL COMMENT '房型编号',
  `hotel_id` varchar(11) NOT NULL COMMENT '酒店编号',
  `name` varchar(30) NOT NULL COMMENT '房型名称',
  `price` int(11) NOT NULL COMMENT '价格',
  `price_day` date NOT NULL COMMENT '价格日期',
  `full` varchar(6) DEFAULT '0' COMMENT '0有房；1满房',
  PRIMARY KEY (`id`),
  UNIQUE KEY `pk_room_elong_price` (`hotel_id`,`name`,`price_day`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=230789 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for star_elong
-- ----------------------------
DROP TABLE IF EXISTS `star_elong`;
CREATE TABLE `star_elong` (
  `star` varchar(20) NOT NULL COMMENT '星级',
  `name` varchar(20) NOT NULL COMMENT '星级名称',
  PRIMARY KEY (`star`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='艺龙星级';

-- ----------------------------
-- Table structure for xiaozhu_link
-- ----------------------------
DROP TABLE IF EXISTS `xiaozhu_link`;
CREATE TABLE `xiaozhu_link` (
  `link` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for xiaozhu_zufang_room
-- ----------------------------
DROP TABLE IF EXISTS `xiaozhu_zufang_room`;
CREATE TABLE `xiaozhu_zufang_room` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '唯一标识',
  `room_id` varchar(12) NOT NULL COMMENT '房型编号',
  `city` varchar(20) DEFAULT NULL COMMENT '归属城市',
  `district` varchar(20) DEFAULT NULL COMMENT '归属地区',
  `cbd` varchar(60) DEFAULT NULL COMMENT '归属商圈',
  `detail_title` varchar(256) DEFAULT NULL COMMENT '详情页面的标题名称',
  `detail_url` varchar(256) DEFAULT NULL COMMENT '房型详情地址',
  `detail_img_href` varchar(256) DEFAULT NULL COMMENT '房型缩略图',
  `coordinate_x` varchar(10) DEFAULT NULL COMMENT '维度',
  `coordinate_y` varchar(10) DEFAULT NULL COMMENT '经度',
  `price` varchar(10) DEFAULT NULL COMMENT '价格(元/每晚)',
  `em_comment` varchar(256) DEFAULT NULL COMMENT '点评条数',
  `em_address` varchar(256) DEFAULT NULL COMMENT '出租地址',
  `right_num` varchar(256) DEFAULT NULL COMMENT '评分',
  `rental_type` varchar(256) DEFAULT NULL COMMENT '出租类型',
  `capacity` varchar(256) DEFAULT NULL COMMENT '宜住人数',
  `bed_num` varchar(256) DEFAULT NULL COMMENT '床数',
  `room_meters` varchar(256) DEFAULT NULL COMMENT '面积',
  `room_huxing` varchar(256) DEFAULT NULL COMMENT '户型',
  `bed_size_str` varchar(256) DEFAULT NULL COMMENT '床描述',
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_xiaozhu_zufang_room_pk` (`room_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=16660 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for xiaozhu_zufang_room_attr
-- ----------------------------
DROP TABLE IF EXISTS `xiaozhu_zufang_room_attr`;
CREATE TABLE `xiaozhu_zufang_room_attr` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '唯一标识',
  `room_id` varchar(12) NOT NULL COMMENT '房型编号',
  `attr_type` varchar(256) DEFAULT NULL COMMENT '属性类型',
  `attr_content` varchar(2048) DEFAULT NULL COMMENT '属性内容描述',
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=89861 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for xiaozhu_zufang_room_img
-- ----------------------------
DROP TABLE IF EXISTS `xiaozhu_zufang_room_img`;
CREATE TABLE `xiaozhu_zufang_room_img` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '唯一标识',
  `room_id` varchar(12) NOT NULL COMMENT '房型编号',
  `small_img_src` varchar(256) DEFAULT NULL COMMENT '房型缩略图',
  `big_img_src` varchar(256) DEFAULT NULL COMMENT '房型缩略图',
  `img_desc` varchar(256) DEFAULT NULL COMMENT '房型详情地址',
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=310205 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for zhaopin
-- ----------------------------
DROP TABLE IF EXISTS `zhaopin`;
CREATE TABLE `zhaopin` (
  `id` varchar(20) NOT NULL,
  `name` varchar(200) NOT NULL,
  `city` varchar(20) DEFAULT NULL,
  `xingzhi` varchar(20) DEFAULT NULL,
  `guimo` varchar(20) DEFAULT NULL,
  `site` varchar(200) DEFAULT NULL,
  `hangye` varchar(200) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `latitude` varchar(20) DEFAULT NULL,
  `longitude` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for zhaopin_1
-- ----------------------------
DROP TABLE IF EXISTS `zhaopin_1`;
CREATE TABLE `zhaopin_1` (
  `id` varchar(20) NOT NULL,
  `name` varchar(200) NOT NULL,
  `city` varchar(20) DEFAULT NULL,
  `xingzhi` varchar(20) DEFAULT NULL,
  `guimo` varchar(20) DEFAULT NULL,
  `site` varchar(500) DEFAULT NULL,
  `web` varchar(500) DEFAULT NULL,
  `hangye` varchar(200) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `map` varchar(200) DEFAULT NULL,
  `latitude` varchar(20) DEFAULT NULL,
  `longitude` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
