
#!/usr/bin/env python
# coding: utf-8
"""
clean_crash_code.py
-------------------
Step 2 of the data management pipeline.
Reads raw crash data, selects relevant columns, cleans and standardizes values,
engineers time/severity features, and saves the result to crash_cleaned.csv.
A second-level cleaning pass then narrows to analysis-ready columns and drops
rows with all-unknown environmental conditions.
 
Output: crash_cleaned.csv
Rule: keep crashes from 2018-01-01 and later only.
"""
 
import pandas as pd
import numpy as np
 
# ── Load raw crash data ────────────────────────────────────────────────────────
 
crash_file = "Traffic_Crashes_-_Crashes.csv"
 
crash_keep_cols = [
    "CRASH_RECORD_ID",
    "CRASH_DATE",
    "POSTED_SPEED_LIMIT",
    "TRAFFIC_CONTROL_DEVICE",
    "DEVICE_CONDITION",
    "WEATHER_CONDITION",
    "LIGHTING_CONDITION",
    "FIRST_CRASH_TYPE",
    "TRAFFICWAY_TYPE",
    "LANE_CNT",
    "ALIGNMENT",
    "ROADWAY_SURFACE_COND",
    "ROAD_DEFECT",
    "REPORT_TYPE",
    "CRASH_TYPE",
    "INTERSECTION_RELATED_I",
    "NOT_RIGHT_OF_WAY_I",
    "HIT_AND_RUN_I",
    "DAMAGE",
    "PRIM_CONTRIBUTORY_CAUSE",
    "SEC_CONTRIBUTORY_CAUSE",
    "NUM_UNITS",
    "MOST_SEVERE_INJURY",
    "INJURIES_TOTAL",
    "INJURIES_FATAL",
    "INJURIES_INCAPACITATING",
    "INJURIES_NON_INCAPACITATING",
    "INJURIES_REPORTED_NOT_EVIDENT",
    "CRASH_HOUR",
    "CRASH_DAY_OF_WEEK",
    "CRASH_MONTH",
    "LATITUDE",
    "LONGITUDE"
]
 
crash = pd.read_csv(crash_file, usecols=crash_keep_cols, low_memory=False)
print("Original crash shape:", crash.shape)
 
# ── Basic cleaning ─────────────────────────────────────────────────────────────
 
# 列名统一小写
crash.columns = crash.columns.str.lower()
 
# 去掉主键缺失
crash = crash.dropna(subset=["crash_record_id"])
 
# crash-level 数据理论上一条 crash_record_id 一行
crash = crash.drop_duplicates(subset=["crash_record_id"])
 
crash["crash_date"] = pd.to_datetime(crash["crash_date"], errors="coerce")
crash = crash.dropna(subset=["crash_date"])
 
# 只保留 2018 年及以后
crash = crash[crash["crash_date"] >= pd.Timestamp("2018-01-01")].copy()
 
# ── Numeric columns ────────────────────────────────────────────────────────────
 
crash_numeric_cols = [
    "posted_speed_limit",
    "lane_cnt",
    "num_units",
    "injuries_total",
    "injuries_fatal",
    "injuries_incapacitating",
    "injuries_non_incapacitating",
    "injuries_reported_not_evident",
    "crash_hour",
    "crash_day_of_week",
    "crash_month",
    "latitude",
    "longitude"
]
for col in crash_numeric_cols:
    crash[col] = pd.to_numeric(crash[col], errors="coerce")
 
# ── Categorical columns ────────────────────────────────────────────────────────
 
# 类别字段标准化
crash_cat_cols = [
    "traffic_control_device",
    "device_condition",
    "weather_condition",
    "lighting_condition",
    "first_crash_type",
    "trafficway_type",
    "alignment",
    "roadway_surface_cond",
    "road_defect",
    "report_type",
    "crash_type",
    "intersection_related_i",
    "not_right_of_way_i",
    "hit_and_run_i",
    "damage",
    "prim_contributory_cause",
    "sec_contributory_cause",
    "most_severe_injury"
]
 
for col in crash_cat_cols:
    crash[col] = (
        crash[col]
        .astype("string")
        .str.strip()
        .str.upper()
    )
 
# 统一缺失/未知
replace_map = {
    "": pd.NA,
    "UNKNOWN": pd.NA,
    "UNABLE TO DETERMINE": pd.NA,
    "NOT APPLICABLE": pd.NA
}
for col in crash_cat_cols:
    crash[col] = crash[col].replace(replace_map)
 
# ── Y/N binary columns → 1/0 ──────────────────────────────────────────────────
 
# Y/N 字段转 1/0
yn_cols = ["intersection_related_i", "not_right_of_way_i", "hit_and_run_i"]
for col in yn_cols:
    crash[col] = crash[col].map({"Y": 1, "N": 0}).astype("Int64")
 
# ── Time feature engineering ───────────────────────────────────────────────────
 
# 时间特征
crash["crash_year"] = crash["crash_date"].dt.year
crash["crash_month_from_date"] = crash["crash_date"].dt.month
crash["crash_day"] = crash["crash_date"].dt.day
crash["crash_hour_from_date"] = crash["crash_date"].dt.hour
crash["crash_weekday"] = crash["crash_date"].dt.day_name()
crash["is_weekend"] = crash["crash_date"].dt.weekday.isin([5, 6]).astype(int)
 
# 用日期提取补齐原字段缺失
crash["crash_hour"] = crash["crash_hour"].fillna(crash["crash_hour_from_date"])
crash["crash_month"] = crash["crash_month"].fillna(crash["crash_month_from_date"])
 
# ── Injury / severity features ─────────────────────────────────────────────────
 
# 伤害字段缺失补 0，便于构造 severity
injury_fill0_cols = [
    "injuries_total",
    "injuries_fatal",
    "injuries_incapacitating",
    "injuries_non_incapacitating",
    "injuries_reported_not_evident"
]
for col in injury_fill0_cols:
    crash[col] = crash[col].fillna(0)
 
# severe_crash: injury/fatal vs non-injury
crash["severe_crash"] = np.where(
    (crash["injuries_total"] > 0) | (crash["injuries_fatal"] > 0),
    1,
    0
)
 
# 更细的伤害等级
def injury_level(row):
    if row["injuries_fatal"] > 0:
        return "FATAL"
    elif row["injuries_incapacitating"] > 0:
        return "INCAPACITATING"
    elif row["injuries_non_incapacitating"] > 0:
        return "NON_INCAPACITATING"
    elif row["injuries_reported_not_evident"] > 0:
        return "REPORTED_NOT_EVIDENT"
    else:
        return "NO_INJURY"
 
crash["injury_level"] = crash.apply(injury_level, axis=1)
 
# ── Fill remaining NaN with "UNKNOWN" ─────────────────────────────────────────
 
important_env_cols = ["weather_condition", "lighting_condition", "roadway_surface_cond"]
for col in important_env_cols:
    crash[col] = crash[col].fillna("UNKNOWN")
 
other_cat_fill = [
    "traffic_control_device",
    "device_condition",
    "first_crash_type",
    "trafficway_type",
    "alignment",
    "road_defect",
    "prim_contributory_cause",
    "sec_contributory_cause",
    "most_severe_injury",
    "damage",
    "crash_type"
]
for col in other_cat_fill:
    crash[col] = crash[col].fillna("UNKNOWN")
 
# ── Select final columns and save ─────────────────────────────────────────────
 
crash_final_cols = [
    "crash_record_id",
    "crash_date",
    "crash_year",
    "crash_month",
    "crash_day",
    "crash_hour",
    "crash_weekday",
    "is_weekend",
    "posted_speed_limit",
    "traffic_control_device",
    "device_condition",
    "weather_condition",
    "lighting_condition",
    "first_crash_type",
    "trafficway_type",
    "lane_cnt",
    "alignment",
    "roadway_surface_cond",
    "road_defect",
    "crash_type",
    "intersection_related_i",
    "not_right_of_way_i",
    "hit_and_run_i",
    "damage",
    "prim_contributory_cause",
    "sec_contributory_cause",
    "num_units",
    "most_severe_injury",
    "injuries_total",
    "injuries_fatal",
    "injuries_incapacitating",
    "injuries_non_incapacitating",
    "injuries_reported_not_evident",
    "injury_level",
    "severe_crash",
    "latitude",
    "longitude"
]
 
crash_cleaned = crash[crash_final_cols].copy()
 
print("Cleaned crash shape:", crash_cleaned.shape)
print("\nCrash severe_crash distribution:")
print(crash_cleaned["severe_crash"].value_counts(normalize=True, dropna=False))
 
crash_cleaned.to_csv("crash_cleaned.csv", index=False)
print("\nSaved: crash_cleaned.csv")
 
# ── 2nd Level Cleaning ────────────────────────────────────────────────────────
 
crash = pd.read_csv("crash_cleaned.csv", low_memory=False)
 
analysis_cols = [
    "crash_record_id",
    "crash_date",
    "crash_year",
    "crash_month",
    "crash_hour",
    "crash_weekday",
    "is_weekend",
    "weather_condition",
    "lighting_condition",
    "roadway_surface_cond",
    "posted_speed_limit",
    "traffic_control_device",
    "trafficway_type",
    "first_crash_type",
    "prim_contributory_cause",
    "num_units",
    "most_severe_injury",
    "injuries_total",
    "injuries_fatal",
    "injury_level",
    "severe_crash"
]
 
crash_analysis = crash[analysis_cols].copy()
 
# Drop rows where any key environmental condition is UNKNOWN
env_all_missing = (
    crash_analysis["weather_condition"].isin(["UNKNOWN"]) |
    crash_analysis["lighting_condition"].isin(["UNKNOWN"]) |
    crash_analysis["roadway_surface_cond"].isin(["UNKNOWN"])
)
crash_analysis = crash_analysis.loc[~env_all_missing].copy()
 
print("Analysis-ready shape:", crash_analysis.shape)
 
crash_analysis.to_csv("crash_cleaned.csv", index=False)
print("Saved: crash_cleaned.csv")
 
# ── Verification: reload saved CSV ────────────────────────────────────────────
 
crash = pd.read_csv("crash_cleaned.csv", low_memory=False)
crash