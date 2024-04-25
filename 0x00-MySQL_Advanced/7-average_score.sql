-- Procedure to compute and store the average score for a student
DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    -- Declare variable to store the average score
    DECLARE avg_score DECIMAL(10,2);

    -- Calculate the average score for the specified user
    SELECT AVG(score) INTO avg_score
    FROM corrections
    WHERE user_id = user_id;

    -- Update the average_score column in the users table
    UPDATE users
    SET average_score = avg_score
    WHERE id = user_id;
END //

DELIMITER ;