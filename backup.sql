-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.5.24-log - MySQL Community Server (GPL)
-- Server OS:                    Win32
-- HeidiSQL Version:             8.3.0.4694
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dumping database structure for threebond
CREATE DATABASE IF NOT EXISTS `threebond` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `threebond`;


-- Dumping structure for table threebond.articles
CREATE TABLE IF NOT EXISTS `articles` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `url` varchar(300) NOT NULL,
  `image` varchar(300) NOT NULL,
  `summary` varchar(500) NOT NULL,
  `tags` varchar(500) NOT NULL,
  `src` varchar(100) NOT NULL,
  `lang` varchar(50) NOT NULL,
  `content` text NOT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.


-- Dumping structure for table threebond.instagram
CREATE TABLE IF NOT EXISTS `instagram` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `caption` varchar(200) NOT NULL,
  `src` varchar(300) NOT NULL,
  `account` varchar(300) NOT NULL,
  `tags` varchar(300) NOT NULL,
  `url` varchar(300) NOT NULL,
  `img_vid_src` varchar(300) NOT NULL,
  `likes` varchar(300) NOT NULL,
  `lang` varchar(300) NOT NULL,
  `media_id` varchar(300) NOT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.


-- Dumping structure for table threebond.twitter
CREATE TABLE IF NOT EXISTS `twitter` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` text NOT NULL,
  `src` varchar(300) NOT NULL,
  `account` varchar(300) NOT NULL,
  `tags` varchar(300) NOT NULL,
  `url` varchar(300) NOT NULL,
  `media_url` varchar(300) NOT NULL,
  `retweets` varchar(300) NOT NULL,
  `lang` varchar(300) NOT NULL,
  `favs` varchar(300) NOT NULL,
  `tweet_id` varchar(300) NOT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.


-- Dumping structure for table threebond.videos
CREATE TABLE IF NOT EXISTS `videos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `url` varchar(300) NOT NULL,
  `src` varchar(100) NOT NULL,
  `lang` varchar(50) NOT NULL,
  `preview_image` varchar(300) NOT NULL,
  `embed_code` varchar(300) NOT NULL,
  `embed_url` varchar(300) NOT NULL,
  `date` datetime NOT NULL,
  `channel` varchar(110) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
