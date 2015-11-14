-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.6.17 - MySQL Community Server (GPL)
-- Server OS:                    Win64
-- HeidiSQL Version:             8.3.0.4694
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dumping structure for table threebont.articles
CREATE TABLE IF NOT EXISTS `articles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `postId` varchar(100) NOT NULL,
  `title` varchar(100) NOT NULL,
  `account_img` varchar(250) DEFAULT NULL,
  `src` varchar(100) DEFAULT NULL,
  `url` varchar(300) NOT NULL,
  `image` varchar(300) DEFAULT NULL,
  `summary` text,
  `tags` varchar(500) DEFAULT NULL,
  `lang` varchar(50) DEFAULT NULL,
  `content` text,
  `date` datetime NOT NULL,
  `itemIndex` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `postId` (`postId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table threebont.instagram
CREATE TABLE IF NOT EXISTS `instagram` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `caption` varchar(200) DEFAULT NULL,
  `account` varchar(300) DEFAULT NULL,
  `account_img` varchar(300) DEFAULT NULL,
  `tags` varchar(300) DEFAULT NULL,
  `url` varchar(300) DEFAULT NULL,
  `img_vid_src` varchar(300) DEFAULT NULL,
  `likes` varchar(300) DEFAULT NULL,
  `lang` varchar(300) DEFAULT NULL,
  `media_id` varchar(100) DEFAULT NULL,
  `date` datetime NOT NULL,
  `itemIndex` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `media_id` (`media_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table threebont.livescores
CREATE TABLE IF NOT EXISTS `livescores` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `competition` varchar(120) DEFAULT NULL,
  `competitionLogo` varchar(500) DEFAULT NULL,
  `visitorTeam` varchar(120) DEFAULT NULL,
  `visitorTeamLogo` varchar(500) DEFAULT NULL,
  `localTeam` varchar(120) DEFAULT NULL,
  `localTeamLogo` varchar(500) DEFAULT NULL,
  `visitorTeamScore` tinyint(3) unsigned NOT NULL,
  `localTeamScore` tinyint(3) unsigned NOT NULL,
  `matchDateTime` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `visitorTeam_localTeam_matchDateTime` (`visitorTeam`,`localTeam`,`matchDateTime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table threebont.relatedarticles
CREATE TABLE IF NOT EXISTS `relatedarticles` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `articleId` int(11) NOT NULL,
  `clusterId` int(11) NOT NULL,
  `distance` float NOT NULL,
  `createdAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`Id`),
  KEY `FK_relatedarticles_articles` (`articleId`),
  CONSTRAINT `FK_relatedarticles_articles` FOREIGN KEY (`articleId`) REFERENCES `articles` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table threebont.twitter
CREATE TABLE IF NOT EXISTS `twitter` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` text,
  `account` varchar(300) DEFAULT NULL,
  `tags` varchar(300) DEFAULT NULL,
  `url` varchar(300) DEFAULT NULL,
  `media_url` varchar(300) DEFAULT NULL,
  `retweets` varchar(300) DEFAULT NULL,
  `lang` varchar(300) DEFAULT NULL,
  `favs` varchar(300) DEFAULT NULL,
  `tweet_id` varchar(100) DEFAULT NULL,
  `date` datetime NOT NULL,
  `account_img` varchar(300) DEFAULT NULL,
  `itemIndex` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tweet_id` (`tweet_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table threebont.videos
CREATE TABLE IF NOT EXISTS `videos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `account_img` varchar(300) NOT NULL,
  `url` varchar(300) DEFAULT NULL,
  `lang` varchar(50) DEFAULT NULL,
  `preview_image` varchar(300) DEFAULT NULL,
  `embed_code` varchar(300) DEFAULT NULL,
  `embed_url` varchar(300) DEFAULT NULL,
  `date` datetime NOT NULL,
  `channel` varchar(110) DEFAULT NULL,
  `itemIndex` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title_channel` (`title`,`channel`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
