# DAX measures

### Total Establishments
*Folder: 1 Establishments · Format: `#,0`*
```dax
Total Establishments = SWITCH(TRUE(), ISCROSSFILTERED(Dim_Region[Region]) && ISCROSSFILTERED(Dim_Activity[Activity]), BLANK(), ISCROSSFILTERED(Dim_Region[Region]), SUM(Fact_Establishments_Region[Establishments]), SUM(Fact_Establishments_Activity[Establishments]))
```

### Establishments Share %
*Folder: 1 Establishments · Format: `0.0%`*
```dax
Establishments Share % = DIVIDE([Total Establishments], CALCULATE([Total Establishments], REMOVEFILTERS(Dim_Activity), REMOVEFILTERS(Dim_Region)))
```

### Total Employees
*Folder: 2 Employment · Format: `#,0`*
```dax
Total Employees = SWITCH(TRUE(), ISCROSSFILTERED(Dim_Region[Region]) && ISCROSSFILTERED(Dim_Activity[Activity]), BLANK(), ISCROSSFILTERED(Dim_Region[Region]), CALCULATE(SUM(Fact_Employment_Region[Employees])), CALCULATE(SUM(Fact_Employment_Activity[Employees])))
```

### Male Employees
*Folder: 2 Employment · Format: `#,0`*
```dax
Male Employees = SWITCH(TRUE(), ISCROSSFILTERED(Dim_Region[Region]) && ISCROSSFILTERED(Dim_Activity[Activity]), BLANK(), ISCROSSFILTERED(Dim_Region[Region]), CALCULATE(SUM(Fact_Employment_Region[Employees]), Fact_Employment_Region[Gender] = "Male"), CALCULATE(SUM(Fact_Employment_Activity[Employees]), Fact_Employment_Activity[Gender] = "Male"))
```

### Female Employees
*Folder: 2 Employment · Format: `#,0`*
```dax
Female Employees = SWITCH(TRUE(), ISCROSSFILTERED(Dim_Region[Region]) && ISCROSSFILTERED(Dim_Activity[Activity]), BLANK(), ISCROSSFILTERED(Dim_Region[Region]), CALCULATE(SUM(Fact_Employment_Region[Employees]), Fact_Employment_Region[Gender] = "Female"), CALCULATE(SUM(Fact_Employment_Activity[Employees]), Fact_Employment_Activity[Gender] = "Female"))
```

### Saudi Employees
*Folder: 2 Employment · Format: `#,0`*
```dax
Saudi Employees = SWITCH(TRUE(), ISCROSSFILTERED(Dim_Region[Region]) && ISCROSSFILTERED(Dim_Activity[Activity]), BLANK(), ISCROSSFILTERED(Dim_Region[Region]), CALCULATE(SUM(Fact_Employment_Region[Employees]), Fact_Employment_Region[Nationality] = "Saudi"), CALCULATE(SUM(Fact_Employment_Activity[Employees]), Fact_Employment_Activity[Nationality] = "Saudi"))
```

### Non-Saudi Employees
*Folder: 2 Employment · Format: `#,0`*
```dax
Non-Saudi Employees = SWITCH(TRUE(), ISCROSSFILTERED(Dim_Region[Region]) && ISCROSSFILTERED(Dim_Activity[Activity]), BLANK(), ISCROSSFILTERED(Dim_Region[Region]), CALCULATE(SUM(Fact_Employment_Region[Employees]), Fact_Employment_Region[Nationality] = "Non-Saudi"), CALCULATE(SUM(Fact_Employment_Activity[Employees]), Fact_Employment_Activity[Nationality] = "Non-Saudi"))
```

### Female Share %
*Folder: 2 Employment · Format: `0.0%`*
```dax
Female Share % = DIVIDE([Female Employees], [Total Employees])
```

### Saudi Share %
*Folder: 2 Employment · Format: `0.0%`*
```dax
Saudi Share % = DIVIDE([Saudi Employees], [Total Employees])
```

### Employees Share %
*Folder: 2 Employment · Format: `0.0%`*
```dax
Employees Share % = DIVIDE([Total Employees], CALCULATE([Total Employees], REMOVEFILTERS(Dim_Activity), REMOVEFILTERS(Dim_Region)))
```

### Employees per Establishment
*Folder: 2 Employment · Format: `0.0`*
```dax
Employees per Establishment = DIVIDE([Total Employees], [Total Establishments])
```

### Licensed Facilities
*Folder: 3 Regional hospitality · Format: `#,0`*
```dax
Licensed Facilities = SUM(Fact_Regional_Hospitality[Facilities])
```

### Available Rooms
*Folder: 3 Regional hospitality · Format: `#,0`*
```dax
Available Rooms = SUM(Fact_Regional_Hospitality[Available_Rooms])
```

### Occupancy Rate
*Folder: 3 Regional hospitality · Format: `0.0%`*
```dax
Occupancy Rate = DIVIDE(SUMX(Fact_Regional_Hospitality, Fact_Regional_Hospitality[Occupancy] * Fact_Regional_Hospitality[Available_Rooms]), SUM(Fact_Regional_Hospitality[Available_Rooms]))
```

### ADR (SAR)
*Folder: 3 Regional hospitality · Format: `#,0`*
```dax
ADR (SAR) = DIVIDE(SUMX(Fact_Regional_Hospitality, Fact_Regional_Hospitality[ADR] * Fact_Regional_Hospitality[Occupancy] * Fact_Regional_Hospitality[Available_Rooms]), SUMX(Fact_Regional_Hospitality, Fact_Regional_Hospitality[Occupancy] * Fact_Regional_Hospitality[Available_Rooms]))
```

### RevPAR (SAR)
*Folder: 3 Regional hospitality · Format: `#,0`*
```dax
RevPAR (SAR) = [Occupancy Rate] * [ADR (SAR)]
```

### Length of Stay (nights)
*Folder: 3 Regional hospitality · Format: `0.00`*
```dax
Length of Stay (nights) = AVERAGE(Fact_Regional_Hospitality[ALOS])
```

### Average Hotel Occupancy Rate
*Folder: 3 Regional hospitality · Format: `0.0%`*
```dax
Average Hotel Occupancy Rate = CALCULATE([Occupancy Rate], Dim_Facility_Type[Facility_Type] = "Hotels")
```

### Average Apartment Occupancy Rate
*Folder: 3 Regional hospitality · Format: `0.0%`*
```dax
Average Apartment Occupancy Rate = CALCULATE([Occupancy Rate], Dim_Facility_Type[Facility_Type] = "Serviced apartments & other")
```

### Average ADR
*Folder: 3 Regional hospitality · Format: `#,0`*
```dax
Average ADR = CALCULATE([ADR (SAR)], Dim_Facility_Type[Facility_Type] = "Hotels")
```

### Average Apartment ADR
*Folder: 3 Regional hospitality · Format: `#,0`*
```dax
Average Apartment ADR = CALCULATE([ADR (SAR)], Dim_Facility_Type[Facility_Type] = "Serviced apartments & other")
```

### Hotel RevPAR (SAR)
*Folder: 3 Regional hospitality · Format: `#,0`*
```dax
Hotel RevPAR (SAR) = CALCULATE([RevPAR (SAR)], Dim_Facility_Type[Facility_Type] = "Hotels")
```

### Average Length of Stay
*Folder: 3 Regional hospitality · Format: `0.00`*
```dax
Average Length of Stay = IF(ISCROSSFILTERED(Dim_Region[Region]), CALCULATE([Length of Stay (nights)], Dim_Facility_Type[Facility_Type] = "Hotels"), CALCULATE(MAX(Fact_Quarterly[ALOS_Hotels]), Fact_Quarterly[Quarter_Key] = 20262))
```

### Hotel Occupancy Q2 2025
*Folder: 3 Regional hospitality · Format: `0.0%`*
```dax
Hotel Occupancy Q2 2025 = CALCULATE(DIVIDE(SUMX(Fact_Regional_Hospitality, Fact_Regional_Hospitality[Occupancy_Q2_2025] * Fact_Regional_Hospitality[Available_Rooms]), SUM(Fact_Regional_Hospitality[Available_Rooms])), Dim_Facility_Type[Facility_Type] = "Hotels")
```

### Hotel Occupancy Change (pts)
*Folder: 3 Regional hospitality · Format: `+0.0;-0.0;0.0`*
```dax
Hotel Occupancy Change (pts) = ([Average Hotel Occupancy Rate] - [Hotel Occupancy Q2 2025]) * 100
```

### Hotel ADR Q2 2025
*Folder: 3 Regional hospitality · Format: `#,0`*
```dax
Hotel ADR Q2 2025 = CALCULATE(DIVIDE(SUMX(Fact_Regional_Hospitality, Fact_Regional_Hospitality[ADR_Q2_2025] * Fact_Regional_Hospitality[Occupancy_Q2_2025] * Fact_Regional_Hospitality[Available_Rooms]), SUMX(Fact_Regional_Hospitality, Fact_Regional_Hospitality[Occupancy_Q2_2025] * Fact_Regional_Hospitality[Available_Rooms])), Dim_Facility_Type[Facility_Type] = "Hotels")
```

### Hotel ADR Change %
*Folder: 3 Regional hospitality · Format: `+0.0%;-0.0%;0.0%`*
```dax
Hotel ADR Change % = DIVIDE([Average ADR] - [Hotel ADR Q2 2025], [Hotel ADR Q2 2025])
```

### City Occupancy Rate
*Folder: 4 City · Format: `0.0%`*
```dax
City Occupancy Rate = IF(ISCROSSFILTERED(Dim_Facility_Type[Facility_Type]), AVERAGE(Fact_City_Hospitality[Occupancy]), CALCULATE(AVERAGE(Fact_City_Hospitality[Occupancy]), Dim_Facility_Type[Facility_Type] = "All facilities"))
```

### City ADR (SAR)
*Folder: 4 City · Format: `#,0`*
```dax
City ADR (SAR) = IF(ISCROSSFILTERED(Dim_Facility_Type[Facility_Type]), AVERAGE(Fact_City_Hospitality[ADR]), CALCULATE(AVERAGE(Fact_City_Hospitality[ADR]), Dim_Facility_Type[Facility_Type] = "All facilities"))
```

### City Length of Stay (nights)
*Folder: 4 City · Format: `0.00`*
```dax
City Length of Stay (nights) = IF(ISCROSSFILTERED(Dim_Facility_Type[Facility_Type]), AVERAGE(Fact_City_Hospitality[ALOS]), CALCULATE(AVERAGE(Fact_City_Hospitality[ALOS]), Dim_Facility_Type[Facility_Type] = "All facilities"))
```

### Q Tourism Establishments
*Folder: 5 Quarterly · Format: `#,0`*
```dax
Q Tourism Establishments = SUM(Fact_Quarterly[Tourism_Establishments])
```

### Q Licensed Facilities
*Folder: 5 Quarterly · Format: `#,0`*
```dax
Q Licensed Facilities = SUM(Fact_Quarterly[Licensed_Facilities])
```

### Q Hotel Occupancy
*Folder: 5 Quarterly · Format: `0.0%`*
```dax
Q Hotel Occupancy = AVERAGE(Fact_Quarterly[Occupancy_Hotels])
```

### Q Apartment Occupancy
*Folder: 5 Quarterly · Format: `0.0%`*
```dax
Q Apartment Occupancy = AVERAGE(Fact_Quarterly[Occupancy_Apartments])
```

### Q Hotel ADR (SAR)
*Folder: 5 Quarterly · Format: `#,0`*
```dax
Q Hotel ADR (SAR) = AVERAGE(Fact_Quarterly[ADR_Hotels])
```

### Q Apartment ADR (SAR)
*Folder: 5 Quarterly · Format: `#,0`*
```dax
Q Apartment ADR (SAR) = AVERAGE(Fact_Quarterly[ADR_Apartments])
```

### Q Hotel Length of Stay
*Folder: 5 Quarterly · Format: `0.00`*
```dax
Q Hotel Length of Stay = AVERAGE(Fact_Quarterly[ALOS_Hotels])
```

### Q Apartment Length of Stay
*Folder: 5 Quarterly · Format: `0.00`*
```dax
Q Apartment Length of Stay = AVERAGE(Fact_Quarterly[ALOS_Apartments])
```

### Q Total Employees
*Folder: 5 Quarterly · Format: `#,0`*
```dax
Q Total Employees = SUM(Fact_Quarterly[Total_Employees])
```

### Q Saudi Employees
*Folder: 5 Quarterly · Format: `#,0`*
```dax
Q Saudi Employees = SUM(Fact_Quarterly[Saudi_Employees])
```

### Q Non-Saudi Employees
*Folder: 5 Quarterly · Format: `#,0`*
```dax
Q Non-Saudi Employees = SUM(Fact_Quarterly[NonSaudi_Employees])
```

### Establishments YoY %
*Folder: 5 Quarterly · Format: `+0.0%;-0.0%;0.0%`*
```dax
Establishments YoY % = VAR k = MAX(Dim_Quarter[Quarter_Key]) VAR cur = CALCULATE(SUM(Fact_Quarterly[Tourism_Establishments]), Dim_Quarter[Quarter_Key] = k) VAR prev = CALCULATE(SUM(Fact_Quarterly[Tourism_Establishments]), ALL(Dim_Quarter), Dim_Quarter[Quarter_Key] = k - 10) RETURN IF(NOT ISBLANK(prev) && NOT ISBLANK(cur), DIVIDE(cur - prev, prev))
```

### Employees YoY %
*Folder: 5 Quarterly · Format: `+0.0%;-0.0%;0.0%`*
```dax
Employees YoY % = VAR k = MAX(Dim_Quarter[Quarter_Key]) VAR cur = CALCULATE(SUM(Fact_Quarterly[Total_Employees]), Dim_Quarter[Quarter_Key] = k) VAR prev = CALCULATE(SUM(Fact_Quarterly[Total_Employees]), ALL(Dim_Quarter), Dim_Quarter[Quarter_Key] = k - 10) RETURN IF(NOT ISBLANK(prev) && NOT ISBLANK(cur), DIVIDE(cur - prev, prev))
```

### Licensed Facilities YoY %
*Folder: 5 Quarterly · Format: `+0.0%;-0.0%;0.0%`*
```dax
Licensed Facilities YoY % = VAR k = MAX(Dim_Quarter[Quarter_Key]) VAR cur = CALCULATE(SUM(Fact_Quarterly[Licensed_Facilities]), Dim_Quarter[Quarter_Key] = k) VAR prev = CALCULATE(SUM(Fact_Quarterly[Licensed_Facilities]), ALL(Dim_Quarter), Dim_Quarter[Quarter_Key] = k - 10) RETURN IF(NOT ISBLANK(prev) && NOT ISBLANK(cur), DIVIDE(cur - prev, prev))
```

### Latest Hotel Occupancy (published)
*Folder: 5 Quarterly · Format: `0.0%`*
```dax
Latest Hotel Occupancy (published) = VAR k = MAX(Dim_Quarter[Quarter_Key]) RETURN CALCULATE(MAX(Fact_Quarterly[Occupancy_Hotels]), Dim_Quarter[Quarter_Key] = k)
```

### Latest Hotel ADR (published)
*Folder: 5 Quarterly · Format: `#,0`*
```dax
Latest Hotel ADR (published) = VAR k = MAX(Dim_Quarter[Quarter_Key]) RETURN CALCULATE(MAX(Fact_Quarterly[ADR_Hotels]), Dim_Quarter[Quarter_Key] = k)
```

### Occupancy Change Color
*Folder: 9 Formatting · Used as field-value conditional formatting for the "Hotel occupancy change vs Q2 2025" bars (green = up, rose = down)*
```dax
Occupancy Change Color = IF([Hotel Occupancy Change (pts)] >= 0, "#0F7B5F", "#B5475B")
```
