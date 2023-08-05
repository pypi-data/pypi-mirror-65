WITH entries AS (SELECT
  c.name AS cat_name,
  p.name AS prj_name,
  e.start_time,
  e.duration
 FROM entry AS e
 LEFT JOIN category AS c ON
   e.category_id = c.id
 LEFT JOIN project AS p ON
   e.project_id = p.id
WHERE e.start_time BETWEEN :start_date AND :end_date
),
days AS (
 SELECT
   e.cat_name,
   e.start_time,
   strftime('%w', e.start_time) AS DOW,
   e.duration
 from entries AS e
)
SELECT
  a.cat_name,
  ROUND(SUM(a.sun) / 60.0, 2) AS SUN,
  ROUND(SUM(a.mon) / 60.0, 2) AS MON,
  ROUND(SUM(a.tue) / 60.0, 2) AS TUE,
  ROUND(SUM(a.wed) / 60.0, 2) AS WED,
  ROUND(SUM(a.thu) / 60.0, 2) AS THU,
  ROUND(SUM(a.FRI) / 60.0, 2) AS FRI,
  ROUND(SUM(a.SAT) / 60.0, 2) AS SAT,
  ROUND((SUM(a.sun) + SUM(a.mon) + SUM(a.tue) + SUM(a.wed) + SUM(a.thu) + SUM(a.fri) + SUM(a.sat)) / 60.0, 2) AS TOTAL
FROM (
SELECT
  d.cat_name,
  CASE WHEN d.dow = '0' THEN d.duration ELSE 0 END AS sun,
  CASE WHEN d.dow = '1' THEN d.duration ELSE 0 END AS mon,
  CASE WHEN d.dow = '2' THEN d.duration ELSE 0 END AS tue,
  CASE WHEN d.dow = '3' THEN d.duration ELSE 0 END AS wed,
  CASE WHEN d.dow = '4' THEN d.duration ELSE 0 END AS thu,
  CASE WHEN d.dow = '5' THEN d.duration ELSE 0 END AS fri,
  CASE WHEN d.dow = '6' THEN d.duration ELSE 0 END AS sat
 FROM days AS d) AS a
 GROUP BY a.cat_name
