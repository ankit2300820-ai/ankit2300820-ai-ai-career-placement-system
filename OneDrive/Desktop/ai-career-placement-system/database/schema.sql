-- MySQL schema (SQLite is handled automatically by src/db.py)
CREATE TABLE IF NOT EXISTS students (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(120) NOT NULL UNIQUE,
  password_hash VARCHAR(200) NOT NULL,
  branch VARCHAR(50) DEFAULT 'CSE',
  study_year INT DEFAULT 4,
  cgpa FLOAT DEFAULT 7.0,
  tenth_pct FLOAT DEFAULT 75,
  twelfth_pct FLOAT DEFAULT 75,
  backlogs INT DEFAULT 0,
  internships INT DEFAULT 0,
  projects INT DEFAULT 1,
  certifications INT DEFAULT 0,
  coding_score FLOAT DEFAULT 50,
  communication FLOAT DEFAULT 6,
  aptitude FLOAT DEFAULT 50,
  hackathons INT DEFAULT 0,
  target_role VARCHAR(80),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS student_skills (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_id INT NOT NULL,
  skill VARCHAR(60) NOT NULL,
  source VARCHAR(20) DEFAULT 'manual',
  UNIQUE (student_id, skill),
  FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS resumes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_id INT NOT NULL,
  filename VARCHAR(200),
  content TEXT,
  uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS predictions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_id INT NOT NULL,
  probability FLOAT,
  readiness FLOAT,
  target_role VARCHAR(80),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS companies (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(80) NOT NULL,
  tier VARCHAR(20),
  min_cgpa FLOAT,
  max_backlogs INT,
  min_10th FLOAT,
  min_12th FLOAT,
  required_skills VARCHAR(300),
  roles VARCHAR(200),
  avg_package_lpa FLOAT
) ENGINE=InnoDB;
