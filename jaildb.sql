DROP DATABASE IF EXISTS JAILDB;
CREATE SCHEMA JAILDB;
USE JAILDB;

-- Table Structure of `JAIL`

DROP TABLE IF EXISTS JAIL;
CREATE TABLE JAIL (
	JId int(15) NOT NULL,
	JName varchar(15) NOT NULL,
	JAdd varchar(100) NOT NULL,
	JCapacity int(8) NOT NULL,
	PRIMARY KEY (JId),
	UNIQUE (JName),
	UNIQUE (JAdd)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table `JAIL`

LOCK TABLES JAIL WRITE;

INSERT INTO JAIL VALUES (1,'Tihar Jail','Delhi',1500),(2,'KalaPani','Andaman and Nicobar',250);

UNLOCK TABLES;


-- Table Structure of `POLICEOFFICER`

DROP TABLE IF EXISTS POLICEOFFICER;
CREATE TABLE POLICEOFFICER (
	POId int(15) NOT NULL,
	POFName varchar(15) NOT NULL,
	POLName varchar(15) DEFAULT NULL,
	POJailId int(15) NOT NULL,
	POAdd varchar(100) DEFAULT NULL,
	PODOB date DEFAULT NULL,
	POSalary int(8) NOT NULL,
	PODateofPosting date NOT NULL,
	JobType varchar(15) NOT NULL, 
	PRIMARY KEY (POId),
	FOREIGN KEY (POJailId) REFERENCES JAIL(JId) ON DELETE CASCADE
-- CHECK (JobType = 'Jailer' OR JobType = 'Guard')
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table `POLICEOFFICER`

LOCK TABLES POLICEOFFICER WRITE;

INSERT INTO POLICEOFFICER VALUES 
(1,'Tanish','Lad',1,'Yawatmal,Maharashtra','1992-12-07',10000,'2015-11-05','Jailer'),
(2,'Manish','Lad',2,'Mumbai,Maharashtra','1954-08-15',25000,'1985-09-04','Jailer'),
(3,'Kushagra','Aggarwal',1,'Kolkata','1914-02-14',5000,'1948-02-14','Gaurd'),
(4,'Shantanu','Aggarwal',2,'Satna,Madhya Pradesh','1947-08-15',7000,'1975-05-18','Guard'),
(5,'Manas','Kabre',1,'Bengaluru','1987-10-31',5000,'2005-08-14','Guard'),
(6,'Nikunj','Nawal',2,'Indore,MP','2000-03-14',30000,'2019-11-05','Guard');

UNLOCK TABLES;

-- Table Structure of `DEPARTMENT`


DROP TABLE IF EXISTS DEPARTMENT;
CREATE TABLE DEPARTMENT (
	DJailId int(15) NOT NULL,
	DName varchar(30) NOT NULL,
	DHeadId int(15) NOT NULL,
	DWage int(8) NOT NULL,
	DWorkHours int(4) NOT NULL,
	PRIMARY KEY (DJailId,DName),
	FOREIGN KEY (DHeadId) REFERENCES POLICEOFFICER (POId) ON DELETE CASCADE,
	FOREIGN KEY (DJailId) REFERENCES JAIL (JId) ON DELETE CASCADE,
	UNIQUE (DHeadId)
	-- UNIQUE (`DName`)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- Dumping data for table `DEPARTMENT`

LOCK TABLES DEPARTMENT WRITE;

INSERT INTO DEPARTMENT VALUES (1, 'Toilet Cleaning', 3, 200, 20),(2,'Toilet Cleaning',4,200,20),(1, 'Kitchen', 5, 100, 14),(2, 'Kitchen', 6, 100, 14);

UNLOCK TABLES;

