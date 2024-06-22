SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema movieopt
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `movieopt` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `movieopt` ;

-- -----------------------------------------------------
-- Table `movieopt`.`dimagent`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movieopt`.`dimagent` (
  `AgentID` VARCHAR(5) NOT NULL,
  `AgentName` VARCHAR(50) NULL DEFAULT NULL,
  `AgentAddress` VARCHAR(50) NULL DEFAULT NULL,
  `AgentPhone` VARCHAR(12) NULL DEFAULT NULL,
  PRIMARY KEY (`AgentID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

CREATE INDEX `idx_dimagent_agentid` ON `movieopt`.`dimagent` (`AgentID` ASC) VISIBLE;

CREATE INDEX `idx_dimagent_agentname` ON `movieopt`.`dimagent` (`AgentName` ASC) VISIBLE;

-- -----------------------------------------------------
-- Table `movieopt`.`dimdirector`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movieopt`.`dimdirector` (
  `DirectorID` VARCHAR(5) NOT NULL,
  `DirectorName` VARCHAR(60) NULL DEFAULT NULL,
  `BirthDate` DATE NULL DEFAULT NULL,
  `Gender` VARCHAR(1) NULL DEFAULT NULL,
  `AgentID` VARCHAR(5) NULL DEFAULT NULL,
  PRIMARY KEY (`DirectorID`),
  CONSTRAINT `dimdirector_ibfk_1`
    FOREIGN KEY (`AgentID`)
    REFERENCES `movieopt`.`dimagent` (`AgentID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

CREATE INDEX `AgentID` ON `movieopt`.`dimdirector` (`AgentID` ASC) VISIBLE;

-- -----------------------------------------------------
-- Table `movieopt`.`dimdistributor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movieopt`.`dimdistributor` (
  `DistributorID` VARCHAR(5) NOT NULL,
  `DistName` VARCHAR(50) NULL DEFAULT NULL,
  `DistAddress` VARCHAR(50) NULL DEFAULT NULL,
  `DistPhone` VARCHAR(12) NULL DEFAULT NULL,
  PRIMARY KEY (`DistributorID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Table `movieopt`.`dimtheater`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movieopt`.`dimtheater` (
  `TheaterID` VARCHAR(5) NOT NULL,
  `TheaterName` VARCHAR(50) NULL DEFAULT NULL,
  `Location` VARCHAR(50) NULL DEFAULT NULL,
  `NoScreens` INT NULL DEFAULT NULL,
  `Seats` INT NULL DEFAULT NULL,
  PRIMARY KEY (`TheaterID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

CREATE INDEX `idx_dimtheater_theaterid` ON `movieopt`.`dimtheater` (`TheaterID` ASC) VISIBLE;

CREATE INDEX `idx_dimtheater_location` ON `movieopt`.`dimtheater` (`Location` ASC) VISIBLE;

-- -----------------------------------------------------
-- Table `movieopt`.`factmovie`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movieopt`.`factmovie` (
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
    REFERENCES `movieopt`.`dimdirector` (`DirectorID`),
  CONSTRAINT `factmovie_ibfk_2`
    FOREIGN KEY (`DistributorID`)
    REFERENCES `movieopt`.`dimdistributor` (`DistributorID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

CREATE INDEX `DirectorID` ON `movieopt`.`factmovie` (`DirectorID` ASC) VISIBLE;

CREATE INDEX `DistributorID` ON `movieopt`.`factmovie` (`DistributorID` ASC) VISIBLE;

CREATE INDEX `ReleaseDateKey` ON `movieopt`.`factmovie` (`ReleaseDate` ASC) VISIBLE;

CREATE INDEX `idx_factmovie_movieid` ON `movieopt`.`factmovie` (`MovieID` ASC) VISIBLE;

CREATE INDEX `idx_factmovie_movierating` ON `movieopt`.`factmovie` (`MovieRating` ASC) VISIBLE;

-- -----------------------------------------------------
-- Table `movieopt`.`factmoviecast_combined`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movieopt`.`factmoviecast_combined` (
  `MovieID` VARCHAR(5) NOT NULL,
  `ActorID` VARCHAR(5) NOT NULL,
  `Salary` DOUBLE NULL DEFAULT NULL,
  `ActorName` VARCHAR(255) NULL DEFAULT NULL,
  `BirthDate` DATE NULL DEFAULT NULL,
  `Nationality` VARCHAR(50) NULL DEFAULT NULL,
  `AgentID` VARCHAR(5) NULL DEFAULT NULL,
  `Gender` VARCHAR(1) NULL DEFAULT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Table `movieopt`.`factmoviereview_combined`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movieopt`.`factmoviereview_combined` (
  `MovieID` VARCHAR(5) NOT NULL,
  `ReviewerID` VARCHAR(5) NOT NULL,
  `ReviewRating` DOUBLE NULL DEFAULT NULL,
  `ReviewerName` VARCHAR(50) NULL DEFAULT NULL,
  `ReviewerClass` VARCHAR(50) NULL DEFAULT NULL,
  `BirthDate` DATE NULL DEFAULT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Table `movieopt`.`factshowing`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movieopt`.`factshowing` (
  `MovieID` VARCHAR(5) NOT NULL,
  `TheaterID` VARCHAR(5) NOT NULL,
  `StartDate` DATE NULL DEFAULT NULL,
  `EndDate` DATE NULL DEFAULT NULL,
  `BoxOffice` DOUBLE NULL DEFAULT NULL,
  PRIMARY KEY (`MovieID`, `TheaterID`),
  CONSTRAINT `factshowing_ibfk_1`
    FOREIGN KEY (`MovieID`)
    REFERENCES `movieopt`.`factmovie` (`MovieID`),
  CONSTRAINT `factshowing_ibfk_2`
    FOREIGN KEY (`TheaterID`)
    REFERENCES `movieopt`.`dimtheater` (`TheaterID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

CREATE INDEX `TheaterID` ON `movieopt`.`factshowing` (`TheaterID` ASC) VISIBLE;

CREATE INDEX `idx_factshowing_movieid` ON `movieopt`.`factshowing` (`MovieID` ASC, `TheaterID` ASC) VISIBLE;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
