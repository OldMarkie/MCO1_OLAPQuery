-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema movieolap
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema movieolap
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `movieolap` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `movieolap` ;

-- -----------------------------------------------------
-- Table `movieolap`.`dimagent`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movieolap`.`dimagent` (
  `AgentID` VARCHAR(5) NOT NULL,
  `AgentName` VARCHAR(50) NULL DEFAULT NULL,
  `AgentAddress` VARCHAR(50) NULL DEFAULT NULL,
  `AgentPhone` VARCHAR(12) NULL DEFAULT NULL,
  PRIMARY KEY (`AgentID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `movieolap`.`dimactor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movieolap`.`dimactor` (
  `ActorID` VARCHAR(5) NOT NULL,
  `ActorName` VARCHAR(255) NULL DEFAULT NULL,
  `BirthDate` DATE NULL DEFAULT NULL,
  `Nationality` VARCHAR(50) NULL DEFAULT NULL,
  `AgentID` VARCHAR(5) NULL DEFAULT NULL,
  `Gender` VARCHAR(1) NULL DEFAULT NULL,
  PRIMARY KEY (`ActorID`),
  INDEX `AgentID` (`AgentID` ASC) VISIBLE,
  CONSTRAINT `dimactor_ibfk_1`
    FOREIGN KEY (`AgentID`)
    REFERENCES `movieolap`.`dimagent` (`AgentID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `movieolap`.`dimdirector`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movieolap`.`dimdirector` (
  `DirectorID` VARCHAR(5) NOT NULL,
  `DirectorName` VARCHAR(60) NULL DEFAULT NULL,
  `BirthDate` DATE NULL DEFAULT NULL,
  `Gender` VARCHAR(1) NULL DEFAULT NULL,
  `AgentID` VARCHAR(5) NULL DEFAULT NULL,
  PRIMARY KEY (`DirectorID`),
  INDEX `AgentID` (`AgentID` ASC) VISIBLE,
  CONSTRAINT `dimdirector_ibfk_1`
    FOREIGN KEY (`AgentID`)
    REFERENCES `movieolap`.`dimagent` (`AgentID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `movieolap`.`dimdistributor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movieolap`.`dimdistributor` (
  `DistributorID` VARCHAR(5) NOT NULL,
  `DistName` VARCHAR(50) NULL DEFAULT NULL,
  `DistAddress` VARCHAR(50) NULL DEFAULT NULL,
  `DistPhone` VARCHAR(12) NULL DEFAULT NULL,
  PRIMARY KEY (`DistributorID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `movieolap`.`dimreviewer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movieolap`.`dimreviewer` (
  `ReviewerID` VARCHAR(5) NOT NULL,
  `ReviewerName` VARCHAR(50) NULL DEFAULT NULL,
  `ReviewerClass` VARCHAR(50) NULL DEFAULT NULL,
  `BirthDate` DATE NULL DEFAULT NULL,
  PRIMARY KEY (`ReviewerID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `movieolap`.`dimtheater`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movieolap`.`dimtheater` (
  `TheaterID` VARCHAR(5) NOT NULL,
  `TheaterName` VARCHAR(50) NULL DEFAULT NULL,
  `Location` VARCHAR(50) NULL DEFAULT NULL,
  `NoScreens` INT NULL DEFAULT NULL,
  `Seats` INT NULL DEFAULT NULL,
  PRIMARY KEY (`TheaterID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `movieolap`.`factmovie`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movieolap`.`factmovie` (
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
  INDEX `DirectorID` (`DirectorID` ASC) VISIBLE,
  INDEX `DistributorID` (`DistributorID` ASC) VISIBLE,
  INDEX `ReleaseDateKey` (`ReleaseDate` ASC) VISIBLE,
  CONSTRAINT `factmovie_ibfk_1`
    FOREIGN KEY (`DirectorID`)
    REFERENCES `movieolap`.`dimdirector` (`DirectorID`),
  CONSTRAINT `factmovie_ibfk_2`
    FOREIGN KEY (`DistributorID`)
    REFERENCES `movieolap`.`dimdistributor` (`DistributorID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `movieolap`.`factmoviecast`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movieolap`.`factmoviecast` (
  `MovieID` VARCHAR(5) NOT NULL,
  `ActorID` VARCHAR(5) NOT NULL,
  `Salary` DOUBLE NULL DEFAULT NULL,
  PRIMARY KEY (`MovieID`, `ActorID`),
  INDEX `ActorID` (`ActorID` ASC) VISIBLE,
  CONSTRAINT `factmoviecast_ibfk_1`
    FOREIGN KEY (`MovieID`)
    REFERENCES `movieolap`.`factmovie` (`MovieID`),
  CONSTRAINT `factmoviecast_ibfk_2`
    FOREIGN KEY (`ActorID`)
    REFERENCES `movieolap`.`dimactor` (`ActorID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `movieolap`.`factmoviereview`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movieolap`.`factmoviereview` (
  `MovieID` VARCHAR(5) NOT NULL,
  `ReviewerID` VARCHAR(5) NOT NULL,
  `ReviewRating` DOUBLE NULL DEFAULT NULL,
  PRIMARY KEY (`MovieID`, `ReviewerID`),
  INDEX `ReviewerID` (`ReviewerID` ASC) VISIBLE,
  CONSTRAINT `factmoviereview_ibfk_1`
    FOREIGN KEY (`MovieID`)
    REFERENCES `movieolap`.`factmovie` (`MovieID`),
  CONSTRAINT `factmoviereview_ibfk_2`
    FOREIGN KEY (`ReviewerID`)
    REFERENCES `movieolap`.`dimreviewer` (`ReviewerID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `movieolap`.`factshowing`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movieolap`.`factshowing` (
  `MovieID` VARCHAR(5) NOT NULL,
  `TheaterID` VARCHAR(5) NOT NULL,
  `StartDate` DATE NULL DEFAULT NULL,
  `EndDate` DATE NULL DEFAULT NULL,
  `BoxOffice` DOUBLE NULL DEFAULT NULL,
  PRIMARY KEY (`MovieID`, `TheaterID`),
  INDEX `TheaterID` (`TheaterID` ASC) VISIBLE,
  CONSTRAINT `factshowing_ibfk_1`
    FOREIGN KEY (`MovieID`)
    REFERENCES `movieolap`.`factmovie` (`MovieID`),
  CONSTRAINT `factshowing_ibfk_2`
    FOREIGN KEY (`TheaterID`)
    REFERENCES `movieolap`.`dimtheater` (`TheaterID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
