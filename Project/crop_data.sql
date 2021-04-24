-- Sakila Sample Database Schema
-- Version 1.2

-- Copyright (c) 2006, 2019, Oracle and/or its affiliates.

-- Redistribution and use in source and binary forms, with or without
-- modification, are permitted provided that the following conditions are
-- met:

-- * Redistributions of source code must retain the above copyright notice,
--   this list of conditions and the following disclaimer.
-- * Redistributions in binary form must reproduce the above copyright
--   notice, this list of conditions and the following disclaimer in the
--   documentation and/or other materials provided with the distribution.
-- * Neither the name of Oracle nor the names of its contributors may be used
--   to endorse or promote products derived from this software without
--   specific prior written permission.

-- THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
-- IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
-- THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
-- PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
-- CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
-- EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
-- PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
-- PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
-- LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
-- NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
-- SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

SET NAMES utf8mb4;
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';


DROP SCHEMA IF EXISTS crop_data;
CREATE SCHEMA crop_data;
USE crop_data;

--
-- Table structure for table `farm`
--

CREATE TABLE farm (
  farm_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  acres INT NOT NULL,
  state VARCHAR(2) NOT NULL,
  PRIMARY KEY  (farm_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Table structure for table `fields`
--

CREATE TABLE field (
  field_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  farm_id INT UNSIGNED NOT NULL,
  acres INT UNSIGNED NOT NULL,
  irrigation ENUM("Above-ground", "In-ground", "None"),
  PRIMARY KEY  (field_id),
  FOREIGN KEY (farm_id) REFERENCES farm (farm_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Table structure for table `category`
--

CREATE TABLE greenhouse (
  greenhouse_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  farm_id INT UNSIGNED NOT NULL,
  hydroponics BOOL NOT NULL,
  growbeds INT UNSIGNED NOT NULL,
  sq_feet INT UNSIGNED NOT NULL,
  PRIMARY KEY  (greenhouse_id),
  FOREIGN KEY (farm_id) REFERENCES farm (farm_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



--
-- Table structure for table `fertilizers`
--

CREATE TABLE fertilizer (
  fert_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  nitrogen INT UNSIGNED NOT NULL,
  phosphorus INT UNSIGNED NOT NULL,
  potassium INT UNSIGNED NOT NULL,
  price_per_ton DECIMAL(5,2),
  PRIMARY KEY  (fert_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Table structure for table `seed`
--

CREATE TABLE seed (
  seed_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  crop_name VARCHAR(24) NOT NULL,
  germination_time SMALLINT UNSIGNED NULL,
  price_per_lb DECIMAL(3,2),
  PRIMARY KEY  (seed_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;




--
-- Table structure for table `crop`
--

CREATE TABLE crop (
  crop_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  field_id INT UNSIGNED,
  greenhouse_id INT UNSIGNED,
  fert_id INT UNSIGNED,
  seed_id INT UNSIGNED NOT NULL,
  pounds_prod INT UNSIGNED,
  pounds_fert INT UNSIGNED,
  date_planted DATE,
  date_harvested DATE,
  PRIMARY KEY  (crop_id),
  FOREIGN KEY (field_id) REFERENCES field (field_id) ON DELETE CASCADE,
  FOREIGN KEY (greenhouse_id) REFERENCES greenhouse (greenhouse_id) ON DELETE CASCADE,
  FOREIGN KEY (fert_id) REFERENCES fertilizer (fert_id) ON DELETE CASCADE,
  FOREIGN KEY (seed_id) REFERENCES seed (seed_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;




--
-- Table structure for table `sales`
--

CREATE TABLE sales (
  sale_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  crop_id INT UNSIGNED NOT NULL,
  date_sold DATE NOT NULL,
  price_per_unit DECIMAL(3,2) NOT NULL,
  units_sold INT UNSIGNED,
  PRIMARY KEY  (sale_id),
  FOREIGN KEY (crop_id) REFERENCES crop (crop_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;




