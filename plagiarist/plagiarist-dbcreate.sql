SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

DROP SCHEMA IF EXISTS `plagiaristdb` ;
CREATE SCHEMA IF NOT EXISTS `plagiaristdb` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci ;

-- -----------------------------------------------------
-- Table `plagiaristdb`.`words`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `plagiaristdb`.`words` ;

CREATE  TABLE IF NOT EXISTS `plagiaristdb`.`words` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `word` VARCHAR(45) NULL ,
  `frequency` INT NOT NULL DEFAULT 0 ,
  PRIMARY KEY (`id`) ,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `plagiaristdb`.`following_words`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `plagiaristdb`.`following_words` ;

CREATE  TABLE IF NOT EXISTS `plagiaristdb`.`following_words` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `frequency` INT NOT NULL DEFAULT 0 ,
  `root_word_id` INT NOT NULL ,
  `following_word_id` INT NOT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_following_words_root` (`root_word_id` ASC) ,
  INDEX `fk_following_words_end` (`following_word_id` ASC) ,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) ,
  CONSTRAINT `fk_following_words_root`
    FOREIGN KEY (`root_word_id` )
    REFERENCES `plagiaristdb`.`words` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_following_words_end`
    FOREIGN KEY (`following_word_id` )
    REFERENCES `plagiaristdb`.`words` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `plagiaristdb`.`preceding_words`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `plagiaristdb`.`preceding_words` ;

CREATE  TABLE IF NOT EXISTS `plagiaristdb`.`preceding_words` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `frequency` INT NOT NULL DEFAULT 0 ,
  `root_word_id` INT NOT NULL ,
  `preceding_word_id` INT NOT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_preceding_word_root` (`root_word_id` ASC) ,
  INDEX `fk_preceding_word_end` (`preceding_word_id` ASC) ,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) ,
  CONSTRAINT `fk_preceding_word_root`
    FOREIGN KEY (`root_word_id` )
    REFERENCES `plagiaristdb`.`words` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_preceding_word_end`
    FOREIGN KEY (`preceding_word_id` )
    REFERENCES `plagiaristdb`.`words` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
