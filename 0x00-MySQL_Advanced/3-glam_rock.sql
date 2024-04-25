-- List bands with Glam rock as main style, ranked by longevity
SELECT band_name,
       CASE
           WHEN split > formed THEN split - formed
           ELSE 2022 - formed
       END as lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;