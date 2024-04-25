-- Rank country origins of bands by number of fans
SELECT origin, COUNT(*) as nb_fans
FROM bands
GROUP BY origin
ORDER BY nb_fans DESC;
