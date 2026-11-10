-- Q1. Headline totals (each fact table at its own grain, no joins between facts)
SELECT (SELECT SUM(Establishments) FROM Fact_Establishments_Activity) AS total_establishments,
       (SELECT SUM(Employees) FROM Fact_Employment_Activity)          AS total_employees,
       (SELECT SUM(Employees) FROM Fact_Employment_Activity WHERE Gender = 'Male')   AS male_employees,
       (SELECT SUM(Employees) FROM Fact_Employment_Activity WHERE Gender = 'Female') AS female_employees,
       (SELECT SUM(Employees) FROM Fact_Employment_Region)            AS total_employees_region_check;

-- Q2. National occupancy and ADR by facility type (weighted)
SELECT Facility_Type,
       SUM(Facilities)                                                   AS facilities,
       SUM(Available_Rooms)                                              AS rooms,
       SUM(Occupancy * Available_Rooms) / SUM(Available_Rooms)           AS occupancy_weighted,
       SUM(ADR * Occupancy * Available_Rooms) / SUM(Occupancy * Available_Rooms) AS adr_weighted,
       AVG(Occupancy)                                                    AS occupancy_simple_avg
FROM Fact_Regional_Hospitality
GROUP BY Facility_Type;

-- Q3. Hotel performance by region with year-on-year change and RevPAR proxy
SELECT Region, Available_Rooms,
       ROUND(Occupancy * 100, 1)                         AS occupancy_pct,
       ROUND((Occupancy - Occupancy_Q2_2025) * 100, 1)   AS occupancy_change_pts,
       ROUND(ADR, 0)                                     AS adr_sar,
       ROUND((ADR / ADR_Q2_2025 - 1) * 100, 1)           AS adr_change_pct,
       ROUND(Occupancy * ADR, 0)                         AS revpar_sar,
       ROUND(ALOS, 2)                                    AS length_of_stay
FROM Fact_Regional_Hospitality
WHERE Facility_Type = 'Hotels'
ORDER BY Occupancy DESC;

-- Q4. Establishments and employees by activity (two facts combined through the shared dimension)
SELECT a.Activity_Short,
       e.Establishments,
       ROUND(100.0 * e.Establishments / (SELECT SUM(Establishments) FROM Fact_Establishments_Activity), 1) AS establishments_share_pct,
       w.Employees,
       ROUND(100.0 * w.Saudi / w.Employees, 1)  AS saudi_share_pct,
       ROUND(1.0 * w.Employees / e.Establishments, 1) AS employees_per_establishment
FROM Dim_Activity a
JOIN Fact_Establishments_Activity e ON e.Activity = a.Activity
JOIN (SELECT Activity, SUM(Employees) AS Employees,
             SUM(CASE WHEN Nationality = 'Saudi' THEN Employees ELSE 0 END) AS Saudi
      FROM Fact_Employment_Activity GROUP BY Activity) w ON w.Activity = a.Activity
ORDER BY e.Establishments DESC;

-- Q5. Employment and establishments by region
SELECT r.Region, s.Establishments, w.Employees,
       ROUND(100.0 * w.Saudi / w.Employees, 1)   AS saudi_share_pct,
       ROUND(100.0 * w.Female / w.Employees, 1)  AS female_share_pct
FROM Dim_Region r
JOIN Fact_Establishments_Region s ON s.Region = r.Region
JOIN (SELECT Region, SUM(Employees) AS Employees,
             SUM(CASE WHEN Nationality = 'Saudi' THEN Employees ELSE 0 END) AS Saudi,
             SUM(CASE WHEN Gender = 'Female' THEN Employees ELSE 0 END)     AS Female
      FROM Fact_Employment_Region GROUP BY Region) w ON w.Region = r.Region
ORDER BY w.Employees DESC;

-- Q6. City ranking by occupancy (all facilities)
SELECT City, ROUND(Occupancy * 100, 1) AS occupancy_pct, ROUND(ADR, 0) AS adr_sar, ROUND(ALOS, 2) AS length_of_stay
FROM Fact_City_Hospitality
WHERE Facility_Type = 'All facilities' AND City <> 'Other'
ORDER BY Occupancy DESC;

-- Q7. Quarterly trend with year-on-year growth of establishments
SELECT d.Quarter_Label, f.Tourism_Establishments,
       ROUND(100.0 * (f.Tourism_Establishments * 1.0 / LAG(f.Tourism_Establishments, 4) OVER (ORDER BY f.Quarter_Key) - 1), 1) AS establishments_yoy_pct,
       ROUND(f.Occupancy_Hotels * 100, 1) AS hotel_occupancy_pct, ROUND(f.ADR_Hotels, 0) AS hotel_adr_sar, f.Total_Employees
FROM Fact_Quarterly f JOIN Dim_Quarter d ON d.Quarter_Key = f.Quarter_Key
ORDER BY f.Quarter_Key
