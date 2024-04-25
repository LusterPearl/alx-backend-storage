-- Create a stored procedure ComputeAverageScoreForUser
DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_projects INT;
    DECLARE avg_score FLOAT;

    -- Compute total score and total projects for the user
    SELECT SUM(score), COUNT(DISTINCT project_id)
    INTO total_score, total_projects
    FROM corrections
    WHERE user_id = user_id;

    -- Compute average score
    IF total_projects > 0 THEN
        SET avg_score = total_score / total_projects;
    ELSE
        SET avg_score = 0;
    END IF;

    -- Update the user's average score
    UPDATE users
    SET average_score = avg_score
    WHERE id = user_id;
END //
DELIMITER ;