-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.7.17-log - MySQL Community Server (GPL)
-- Server OS:                    Win32
-- HeidiSQL Version:             9.4.0.5174
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for go_restaurant
CREATE DATABASE IF NOT EXISTS `go_restaurant` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `go_restaurant`;

-- Dumping structure for procedure go_restaurant.get_recomended
DELIMITER //
CREATE DEFINER=`root`@`%` PROCEDURE `get_recomended`(
	IN `v_user_id` INT





)
    DETERMINISTIC
BEGIN
	DROP TABLE IF EXISTS RANK;

	CREATE TEMPORARY TABLE rank AS
	SELECT similar.user_id, res1.category_id,  COUNT(*) rate
	FROM rating target
	JOIN rating similar ON target.restaurant_id = similar.restaurant_id and target.rating = similar.rating AND target.user_id <> similar.user_id
	JOIN restaurant res1 on target.restaurant_id = res1.id
	JOIN restaurant res2 on similar.restaurant_id = res2.id
	WHERE target.user_id = v_user_id and res1.category_id = res2.category_id
	GROUP BY similar.user_id, res1.category_id;
	
	
	SELECT similar.restaurant_id, SUM(r.rate) AS total_rate
	FROM rank r
	JOIN 	rating similar ON r.user_id = similar.user_id
	LEFT JOIN rating target ON target.user_id = v_user_id  AND target.restaurant_id = similar.restaurant_id
	JOIN restaurant res on similar.restaurant_id = res.id
	WHERE target.restaurant_id IS NULL and res.category_id = r.category_id
	GROUP BY similar.restaurant_id
	ORDER BY total_rate DESC;

END//
DELIMITER ;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
