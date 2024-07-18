-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH graded_assignments AS (
    SELECT teacher_id, COUNT(*) AS total_graded_assignments
    FROM assignments
    WHERE grade = 'A'
    GROUP BY teacher_id
)
SELECT MAX(total_graded_assignments) AS max_graded_assignments
FROM graded_assignments;
