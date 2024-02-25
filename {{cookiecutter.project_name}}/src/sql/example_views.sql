/* This SQL scripts creates views for the example data, using 
functionalities from timescale to fill gaps */

/* Create a time_bucketed, gap-filled view from the otiginal table:*/
CREATE VIEW clean_example_data AS(
	SELECT 
		time_bucket_gapfill('30SEC', "time") AS time,
		interpolate(y) AS y,
		interpolate(state) AS state
	FROM
		example_data
	WHERE
		"time" BETWEEN '2023-05-28 00:00:00+00' AND '2023-08-30 23:59:00+00'
	GROUP BY 1
	ORDER BY 1
	);