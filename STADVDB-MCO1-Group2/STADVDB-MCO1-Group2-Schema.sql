-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema movieoptv3
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema movieoptv3
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `movieoptv3` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `movieoptv3` ;

-- -----------------------------------------------------
-- Table `movieoptv3`.`dimagent`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movieoptv3`.`dimagent` (
  `AgentID` VARCHAR(5) NOT NULL,
  `AgentName` VARCHAR(50) NULL DEFAULT NULL,
  `AgentAddress` VARCHAR(50) NULL DEFAULT NULL,
  `AgentPhone` VARCHAR(12) NULL DEFAULT NULL,
  PRIMARY KEY (`AgentID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

CREATE INDEX `idx_dimagent_agentid` ON `movieoptv3`.`dimagent` (`AgentID` ASC) VISIBLE;

CREATE INDEX `idx_dimagent_agentname` ON `movieoptv3`.`dimagent` (`AgentName` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `movieoptv3`.`dimactor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movieoptv3`.`dimactor` (
  `ActorID` VARCHAR(5) NOT NULL,
  `ActorName` VARCHAR(255) NULL DEFAULT NULL,
  `BirthDate` DATE NULL DEFAULT NULL,
  `Nationality` VARCHAR(50) NULL DEFAULT NULL,
  `AgentID` VARCHAR(5) NULL DEFAULT NULL,
  `Gender` VARCHAR(1) NULL DEFAULT NULL,
  PRIMARY KEY (`ActorID`),
  CONSTRAINT `dimactor_ibfk_1`
    FOREIGN KEY (`AgentID`)
    REFERENCES `movieoptv3`.`dimagent` (`AgentID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

CREATE INDEX `AgentID` ON `movieoptv3`.`dimactor` (`AgentID` ASC) VISIBLE;

CREATE INDEX `idx_dimactor_actorid` ON `movieoptv3`.`dimactor` (`ActorID` ASC) VISIBLE;

CREATE INDEX `idx_dimactor_agentid` ON `movieoptv3`.`dimactor` (`AgentID` ASC) VISIBLE;

CREATE INDEX `idx_dimactor_nationality` ON `movieoptv3`.`dimactor` (`Nationality` ASC) VISIBLE;

CREATE INDEX `idx_dimactor_gender` ON `movieoptv3`.`dimactor` (`Gender` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `movieoptv3`.`dimdirector`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movieoptv3`.`dimdirector` (
  `DirectorID` VARCHAR(5) NOT NULL,
  `DirectorName` VARCHAR(60) NULL DEFAULT NULL,
  `BirthDate` DATE NULL DEFAULT NULL,
  `Gender` VARCHAR(1) NULL DEFAULT NULL,
  `AgentID` VARCHAR(5) NULL DEFAULT NULL,
  PRIMARY KEY (`DirectorID`),
  CONSTRAINT `dimdirector_ibfk_1`
    FOREIGN KEY (`AgentID`)
    REFERENCES `movieoptv3`.`dimagent` (`AgentID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

CREATE INDEX `AgentID` ON `movieoptv3`.`dimdirector` (`AgentID` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `movieoptv3`.`dimdistributor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movieoptv3`.`dimdistributor` (
  `DistributorID` VARCHAR(5) NOT NULL,
  `DistName` VARCHAR(50) NULL DEFAULT NULL,
  `DistAddress` VARCHAR(50) NULL DEFAULT NULL,
  `DistPhone` VARCHAR(12) NULL DEFAULT NULL,
  PRIMARY KEY (`DistributorID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `movieoptv3`.`dimreviewer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movieoptv3`.`dimreviewer` (
  `ReviewerID` VARCHAR(5) NOT NULL,
  `ReviewerName` VARCHAR(50) NULL DEFAULT NULL,
  `ReviewerClass` VARCHAR(50) NULL DEFAULT NULL,
  `BirthDate` DATE NULL DEFAULT NULL,
  PRIMARY KEY (`ReviewerID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

CREATE INDEX `idx_dimreviewer_reviewerid` ON `movieoptv3`.`dimreviewer` (`ReviewerID` ASC) VISIBLE;

CREATE INDEX `idx_dimreviewer_reviewerclass` ON `movieoptv3`.`dimreviewer` (`ReviewerClass` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `movieoptv3`.`dimtheater`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movieoptv3`.`dimtheater` (
  `TheaterID` VARCHAR(5) NOT NULL,
  `TheaterName` VARCHAR(50) NULL DEFAULT NULL,
  `Location` VARCHAR(50) NULL DEFAULT NULL,
  `NoScreens` INT NULL DEFAULT NULL,
  `Seats` INT NULL DEFAULT NULL,
  PRIMARY KEY (`TheaterID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

CREATE INDEX `idx_dimtheater_theaterid` ON `movieoptv3`.`dimtheater` (`TheaterID` ASC) VISIBLE;

CREATE INDEX `idx_dimtheater_location` ON `movieoptv3`.`dimtheater` (`Location` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `movieoptv3`.`factmovie`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movieoptv3`.`factmovie` (
  `MovieID` VARCHAR(5) NOT NULL,
  `Title` VARCHAR(50) NULL DEFAULT NULL,
  `DirectorID` VARCHAR(5) NULL DEFAULT NULL,
  `DistributorID` VARCHAR(50) NULL DEFAULT NULL,
  `ReleaseDate` DATE NULL DEFAULT NULL,
  `ProductionBudget` DECIMAL(19,4) NULL DEFAULT NULL,
  `MovieRating` VARCHAR(5) NULL DEFAULT NULL,
  `Producer` VARCHAR(45) NULL DEFAULT NULL,
  `Genre` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`MovieID`),
  CONSTRAINT `factmovie_ibfk_1`
    FOREIGN KEY (`DirectorID`)
    REFERENCES `movieoptv3`.`dimdirector` (`DirectorID`),
  CONSTRAINT `factmovie_ibfk_2`
    FOREIGN KEY (`DistributorID`)
    REFERENCES `movieoptv3`.`dimdistributor` (`DistributorID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

CREATE INDEX `DirectorID` ON `movieoptv3`.`factmovie` (`DirectorID` ASC) VISIBLE;

CREATE INDEX `DistributorID` ON `movieoptv3`.`factmovie` (`DistributorID` ASC) VISIBLE;

CREATE INDEX `ReleaseDateKey` ON `movieoptv3`.`factmovie` (`ReleaseDate` ASC) VISIBLE;

CREATE INDEX `idx_factmovie_movieid` ON `movieoptv3`.`factmovie` (`MovieID` ASC) VISIBLE;

CREATE INDEX `idx_factmovie_movierating` ON `movieoptv3`.`factmovie` (`MovieRating` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `movieoptv3`.`factmoviecast`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movieoptv3`.`factmoviecast` (
  `MovieID` VARCHAR(5) NOT NULL,
  `ActorID` VARCHAR(5) NOT NULL,
  `Salary` DOUBLE NULL DEFAULT NULL,
  PRIMARY KEY (`MovieID`, `ActorID`),
  CONSTRAINT `factmoviecast_ibfk_1`
    FOREIGN KEY (`MovieID`)
    REFERENCES `movieoptv3`.`factmovie` (`MovieID`),
  CONSTRAINT `factmoviecast_ibfk_2`
    FOREIGN KEY (`ActorID`)
    REFERENCES `movieoptv3`.`dimactor` (`ActorID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

CREATE INDEX `ActorID` ON `movieoptv3`.`factmoviecast` (`ActorID` ASC) VISIBLE;

CREATE INDEX `idx_factmoviecast_actorid` ON `movieoptv3`.`factmoviecast` (`ActorID` ASC) VISIBLE;

CREATE INDEX `idx_factmoviecast_movieid` ON `movieoptv3`.`factmoviecast` (`MovieID` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `movieoptv3`.`factmoviereview`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movieoptv3`.`factmoviereview` (
  `MovieID` VARCHAR(5) NOT NULL,
  `ReviewerID` VARCHAR(5) NOT NULL,
  `ReviewRating` DOUBLE NULL DEFAULT NULL,
  PRIMARY KEY (`MovieID`, `ReviewerID`),
  CONSTRAINT `factmoviereview_ibfk_1`
    FOREIGN KEY (`MovieID`)
    REFERENCES `movieoptv3`.`factmovie` (`MovieID`),
  CONSTRAINT `factmoviereview_ibfk_2`
    FOREIGN KEY (`ReviewerID`)
    REFERENCES `movieoptv3`.`dimreviewer` (`ReviewerID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

CREATE INDEX `ReviewerID` ON `movieoptv3`.`factmoviereview` (`ReviewerID` ASC) VISIBLE;

CREATE INDEX `idx_factmoviereview_movieid` ON `movieoptv3`.`factmoviereview` (`MovieID` ASC) VISIBLE;

CREATE INDEX `idx_factmoviereview_reviewerid` ON `movieoptv3`.`factmoviereview` (`ReviewerID` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `movieoptv3`.`factshowing`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movieoptv3`.`factshowing` (
  `MovieID` VARCHAR(5) NOT NULL,
  `TheaterID` VARCHAR(5) NOT NULL,
  `StartDate` DATE NULL DEFAULT NULL,
  `EndDate` DATE NULL DEFAULT NULL,
  `BoxOffice` DOUBLE NULL DEFAULT NULL,
  PRIMARY KEY (`MovieID`, `TheaterID`),
  CONSTRAINT `factshowing_ibfk_1`
    FOREIGN KEY (`MovieID`)
    REFERENCES `movieoptv3`.`factmovie` (`MovieID`),
  CONSTRAINT `factshowing_ibfk_2`
    FOREIGN KEY (`TheaterID`)
    REFERENCES `movieoptv3`.`dimtheater` (`TheaterID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

CREATE INDEX `TheaterID` ON `movieoptv3`.`factshowing` (`TheaterID` ASC) VISIBLE;

CREATE INDEX `idx_factshowing_movieid` ON `movieoptv3`.`factshowing` (`MovieID` ASC, `TheaterID` ASC) VISIBLE;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
