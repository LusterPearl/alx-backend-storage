-- List bands with Glam rock as their main style, ranked by longevity
SELECT band_name, 
    IFNULL(SUBSTRING_INDEX(lifespan, '-', 1), 2022) - SUBSTRING_INDEX(lifespan, '-', -1) as lifespan
FROM bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;