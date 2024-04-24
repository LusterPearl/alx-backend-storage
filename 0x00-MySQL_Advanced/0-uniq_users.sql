-- Create a table for students with constraints
CREATE TABLE students (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    batch_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_batch_id FOREIGN KEY (batch_id) REFERENCES batches(id)
);

-- Add an index on the batch_id column for faster searches
CREATE INDEX idx_batch_id ON students(batch_id);

-- Create a stored procedure to get the total number of students
DELIMITER //
CREATE PROCEDURE get_student_count()
BEGIN
    SELECT COUNT(*) FROM students;
END //
DELIMITER ;

-- Create a view to get the names of students in batch 3
CREATE VIEW students_batch_3 AS
SELECT name FROM students WHERE batch_id = 3;

-- Create a trigger to log student insertions
CREATE TRIGGER log_student_insert
AFTER INSERT ON students
FOR EACH ROW
BEGIN
    INSERT INTO student_log(action, student_id, timestamp)
    VALUES ('insert', NEW.id, NOW());
END;