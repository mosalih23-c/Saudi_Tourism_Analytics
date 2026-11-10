"""Builds tidy, analysis-ready tables (data/processed) from the cleaned workbook (data/raw)."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "Saudi_Tourism_Analytics_Cleaned.xlsx"
OUT = ROOT / "data" / "processed"
MAIN = ["Quarterly_Trends", "Regional_KPIs", "City_KPIs", "Employment_Activity",
        "Employment_Region", "Establishments_Activity", "Establishments_Region"]
APT, HOT, ALL = "Serviced apartments & other", "Hotels", "All facilities"
MONTHS = ["April", "May", "June"]


def load_main():
    return {s: pd.read_excel(RAW, sheet_name=s) for s in MAIN}


def clean_city(name):
    import re
    return re.sub(r"\s*\(\d\)$", "", name).strip()


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    m = load_main()
    t = {}

    # ---------- Quarterly (grain: quarter) ----------
    q = m["Quarterly_Trends"].copy()
    q.columns = [c.split("_", 2)[2] if c[0].isdigit() else c for c in q.columns]
    q = q.rename(columns={
        "Number_of_serviced_apartments_and_other_hospitality_facilities": "Apartments_Count",
        "Number_of_hotels": "Hotels_Count", "Total_licensed_hospitality": "Licensed_Facilities",
        "Occupancy_rate_in_serviced_apartments_and_other_hospitality_facilities": "Occupancy_Apartments",
        "Occupancy_rate_in_hotels": "Occupancy_Hotels",
        "Average_daily_rate_in_serviced_apartments_and_other_hospitality_facilities": "ADR_Apartments",
        "Average_daily_rate_in_hotels": "ADR_Hotels",
        "Average_length_of_stay_in_serviced_apartments_and_other_hospitality_facilities": "ALOS_Apartments",
        "Average_length_of_stay_in_hotels": "ALOS_Hotels",
        "Total_number_of_Saudi_employees": "Saudi_Employees",
        "Total_number_of_non_Saudi_employees": "NonSaudi_Employees",
        "Total_employees": "Total_Employees",
        "The_percentage_of_female_employees_out_of_total_employees": "Female_Share",
        "Number_of_tourism_etablishments": "Tourism_Establishments"})
    q["Year"] = q["Quarter"].str[-4:].astype(int)
    q["Quarter_Num"] = q["Quarter"].str[1].astype(int)
    q["Quarter_Label"] = q["Year"].astype(str) + " Q" + q["Quarter_Num"].astype(str)
    q["Quarter_Key"] = q["Year"] * 10 + q["Quarter_Num"]
    t["Dim_Quarter"] = q[["Quarter_Key", "Quarter_Label", "Year", "Quarter_Num", "Quarter_Start_Date"]]
    t["Fact_Quarterly"] = q.drop(columns=["Quarter", "Quarter_Sort", "Quarter_Start_Date", "Year",
                                          "Quarter_Num", "Quarter_Label"])

    # ---------- Regional hospitality (grain: region x facility type [x month]) ----------
    r = m["Regional_KPIs"]
    spec = {APT: dict(n="2_1_Number_of_serviced_apartments_and_other_hospitality_facilities",
                      rooms="2_2_Number_of_available_rooms_in_serviced_apartments_and_other_hospitality_facilities",
                      occ="2_3", adr="2_9", alos="2_15", yo="2_21", ya="2_23", yl="2_25"),
            HOT: dict(n="2_1_Number_of_hotels", rooms="2_2_Number_of_available_rooms_in_hotels",
                      occ="2_4", adr="2_10", alos="2_16", yo="2_22", ya="2_24", yl="2_26")}
    rows, mrows = [], []
    for ft, s in spec.items():
        for _, x in r.iterrows():
            rows.append(dict(Region=x["Region"], Facility_Type=ft, Facilities=x[s["n"]],
                             Available_Rooms=x[s["rooms"]],
                             Occupancy=x[s["occ"] + "_Quarterly_average"],
                             ADR=x[s["adr"] + "_Quarterly_average"],
                             ALOS=x[s["alos"] + "_Quarterly_average"],
                             Occupancy_Q2_2025=x[s["yo"] + "_Q2_of_2025"],
                             ADR_Q2_2025=x[s["ya"] + "_Q2_of_2025"],
                             ALOS_Q2_2025=x[s["yl"] + "_Q2_of_2025"]))
            for mo in MONTHS:
                mrows.append(dict(Region=x["Region"], Facility_Type=ft, Month=mo,
                                  Month_Num=4 + MONTHS.index(mo),
                                  Occupancy=x[f"{s['occ']}_{mo}"], ADR=x[f"{s['adr']}_{mo}"],
                                  ALOS=x[f"{s['alos']}_{mo}"]))
    t["Fact_Regional_Hospitality"] = pd.DataFrame(rows)
    t["Fact_Regional_Monthly"] = pd.DataFrame(mrows)

    # ---------- City hospitality (grain: city x facility type [x month]) ----------
    c = m["City_KPIs"].copy()
    c["City_Raw"], c["City"] = c["City"], c["City"].map(clean_city)
    blocks = {"Occupancy": ("2_5", {ALL: "2_6", APT: "2_7", HOT: "2_8"}),
              "ADR": ("2_11", {ALL: "2_12", APT: "2_13", HOT: "2_14"}),
              "ALOS": ("2_17", {ALL: "2_18", APT: "2_19", HOT: "2_20"})}
    crow, cm = {}, {}
    for metric, (_, tabs) in blocks.items():
        for ft, tab in tabs.items():
            for _, x in c.iterrows():
                crow.setdefault((x["City"], ft), {})[metric] = x[f"{tab}_General_average"]
                for mo in MONTHS:
                    cm.setdefault((x["City"], ft, mo), {})[metric] = x[f"{tab}_{mo}"]
    t["Fact_City_Hospitality"] = pd.DataFrame(
        [dict(City=k[0], Facility_Type=k[1], **v) for k, v in crow.items()])
    t["Fact_City_Monthly"] = pd.DataFrame(
        [dict(City=k[0], Facility_Type=k[1], Month=k[2], Month_Num=4 + MONTHS.index(k[2]), **v)
         for k, v in cm.items()])

    # ---------- Employment (grain: activity|region x nationality x gender) ----------
    def emp_long(df, key, total_prefix):
        out = []
        for _, x in df.iterrows():
            for nat, p in (("Saudi", "Saudi"), ("Non-Saudi", "NonSaudi")):
                for g in ("Males", "Females"):
                    out.append({key: x[key], "Nationality": nat, "Gender": g[:-1],
                                "Employees": int(x[f"{p}_{g}"])})
        return pd.DataFrame(out)
    t["Fact_Employment_Activity"] = emp_long(m["Employment_Activity"], "Activity", "Total")
    t["Fact_Employment_Region"] = emp_long(m["Employment_Region"], "Region", "All")

    # ---------- Establishments ----------
    t["Fact_Establishments_Activity"] = m["Establishments_Activity"][
        ["Activity", "Number_of_tourism_establishments"]].rename(
        columns={"Number_of_tourism_establishments": "Establishments"})
    t["Fact_Establishments_Region"] = m["Establishments_Region"][
        ["Region", "Number_of_tourism_establishments"]].rename(
        columns={"Number_of_tourism_establishments": "Establishments"})

    # ---------- Dimensions ----------
    t["Dim_Region"] = pd.DataFrame({"Region": sorted(r["Region"])})
    t["Dim_City"] = c[["City", "City_Raw"]].assign(
        Is_Other=lambda d: d["City"].eq("Other")).sort_values("City")
    acts = m["Establishments_Activity"]["Activity"]
    short = {"Accommodation for visitors": "Accommodation", "Food and beverage serving activities": "Food & beverage",
             "Railway passenger transport": "Rail transport", "Road passenger transport": "Road transport",
             "Water passenger transport": "Water transport", "Air passenger transport": "Air transport",
             "Transport equipment rental": "Transport rental",
             "Travel agencies and other reservation services activities": "Travel agencies",
             "Cultural activities": "Cultural", "Sports and recreational activities": "Sports & recreation",
             "Other tourism characteristic services in the country": "Other tourism services",
             "Retail trade of tourism characteristic goods in the country": "Tourism retail"}
    t["Dim_Activity"] = pd.DataFrame({"Activity": acts, "Activity_Short": acts.map(short),
                                      "Activity_Order": range(1, len(acts) + 1)})
    t["Dim_Facility_Type"] = pd.DataFrame({"Facility_Type": [HOT, APT, ALL], "Facility_Order": [1, 2, 3]})

    for name, df in t.items():
        df.to_csv(OUT / f"{name}.csv", index=False, encoding="utf-8")
    for s in MAIN:  # the 7 cleaned source tables, as-is
        m[s].to_csv(OUT / f"{s}.csv", index=False, encoding="utf-8")
    return t


if __name__ == "__main__":
    for k, v in build().items():
        print(f"{k:32s} {v.shape}")
