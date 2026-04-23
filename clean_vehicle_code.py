#!/usr/bin/env python
# coding: utf-8
"""
clean_vehicle_code.py
---------------------
Step 1 of the data management pipeline.
Reads raw vehicle crash data, selects relevant columns, cleans and standardizes
values, removes low-quality rows, and saves the result to vehicle_cleaned.csv.
"""

import pandas as pd
import numpy as np

# ── Load raw vehicle data ──────────────────────────────────────────────────────

vehicle_file = "Traffic_Crashes_-_Vehicles.csv"   # 改成你的路径

vehicle_keep_cols = [
    "CRASH_UNIT_ID",
    "CRASH_RECORD_ID",
    "CRASH_DATE",
    "UNIT_NO",
    "NUM_PASSENGERS",
    "UNIT_TYPE",
    "VEHICLE_ID",
    "CMRC_VEH_I",
    "VEHICLE_YEAR",
    "VEHICLE_DEFECT",
    "VEHICLE_TYPE",
    "VEHICLE_USE",
    "TRAVEL_DIRECTION",
    "MANEUVER",
    "TOWED_I",
    "FIRE_I",
    "OCCUPANT_CNT",
    "EXCEED_SPEED_LIMIT_I",
    "FIRST_CONTACT_POINT",
    "VEHICLE_CONFIG",
    "CARGO_BODY_TYPE",
    "LOAD_TYPE",
    "HAZMAT_CLASS"
]

vehicle = pd.read_csv(
    vehicle_file,
    usecols=lambda c: c in vehicle_keep_cols,
    low_memory=False
)

print("Original vehicle shape:", vehicle.shape)

# ── Basic cleaning ─────────────────────────────────────────────────────────────

vehicle.columns = vehicle.columns.str.lower()

vehicle = vehicle.dropna(subset=["crash_record_id", "crash_unit_id"])

vehicle["crash_date"] = pd.to_datetime(vehicle["crash_date"], errors="coerce")
vehicle = vehicle.dropna(subset=["crash_date"])

vehicle = vehicle[vehicle["crash_date"] >= pd.Timestamp("2018-01-01")].copy()

vehicle = vehicle.drop_duplicates(subset=["crash_unit_id"])

# ── Numeric columns ────────────────────────────────────────────────────────────

numeric_cols = [
    "unit_no",
    "num_passengers",
    "vehicle_id",
    "vehicle_year",
    "occupant_cnt"
]

for col in numeric_cols:
    vehicle[col] = pd.to_numeric(vehicle[col], errors="coerce")

vehicle.loc[(vehicle["vehicle_year"] < 1900) | (vehicle["vehicle_year"] > 2026), "vehicle_year"] = np.nan

# ── Categorical columns ────────────────────────────────────────────────────────

cat_cols = [
    "unit_type",
    "cmrc_veh_i",
    "vehicle_defect",
    "vehicle_type",
    "vehicle_use",
    "travel_direction",
    "maneuver",
    "towed_i",
    "fire_i",
    "exceed_speed_limit_i",
    "first_contact_point",
    "vehicle_config",
    "cargo_body_type",
    "load_type",
    "hazmat_class"
]

for col in cat_cols:
    vehicle[col] = (
        vehicle[col]
        .astype("string")
        .str.strip()
        .str.upper()
    )

replace_map = {
    "": pd.NA,
    "UNKNOWN": pd.NA,
    "UNABLE TO DETERMINE": pd.NA,
    "NOT APPLICABLE": pd.NA
}

for col in cat_cols:
    vehicle[col] = vehicle[col].replace(replace_map)

# ── Y/N binary columns → 1/0 ──────────────────────────────────────────────────

yn_cols = [
    "cmrc_veh_i",
    "towed_i",
    "fire_i",
    "exceed_speed_limit_i"
]

for col in yn_cols:
    vehicle[col] = vehicle[col].map({"Y": 1, "N": 0}).astype("Int64")

# ── Vehicle type simplification ────────────────────────────────────────────────

def simplify_vehicle_type(x):
    if pd.isna(x):
        return "UNKNOWN"
    x = str(x)

    if "MOTORCYCLE" in x or "MOPED" in x or "MOTOR SCOOTER" in x:
        return "MOTORCYCLE"
    elif "PICKUP" in x or "VAN" in x or "SUV" in x or "PASSENGER" in x or "AUTOMOBILE" in x:
        return "PASSENGER_VEHICLE"
    elif "BUS" in x:
        return "BUS"
    elif "TRUCK" in x or "TRACTOR" in x or "SEMI" in x:
        return "TRUCK"
    elif "BICYCLE" in x or "PEDALCYCLE" in x:
        return "BICYCLE"
    elif "PEDESTRIAN" in x:
        return "PEDESTRIAN"
    else:
        return "OTHER"

vehicle["vehicle_category"] = vehicle["vehicle_type"].apply(simplify_vehicle_type)

# ── Fill remaining NaN with "UNKNOWN" ─────────────────────────────────────────

fill_unknown_cols = [
    "vehicle_type",
    "vehicle_category",
    "vehicle_use",
    "maneuver",
    "vehicle_defect",
    "first_contact_point",
    "vehicle_config",
    "cargo_body_type",
    "load_type",
    "hazmat_class"
]

for col in fill_unknown_cols:
    vehicle[col] = vehicle[col].fillna("UNKNOWN")

# ── Drop rows with no useful signal ───────────────────────────────────────────

weak_info_mask = (
    vehicle["vehicle_type"].eq("UNKNOWN") &
    vehicle["maneuver"].eq("UNKNOWN") &
    vehicle["vehicle_use"].eq("UNKNOWN")
)

vehicle = vehicle.loc[~weak_info_mask].copy()

# ── Select final columns and save ─────────────────────────────────────────────

final_cols = [
    "crash_unit_id",
    "crash_record_id",
    "crash_date",
    "unit_no",
    "num_passengers",
    "unit_type",
    "vehicle_id",
    "cmrc_veh_i",
    "vehicle_year",
    "vehicle_defect",
    "vehicle_type",
    "vehicle_category",
    "vehicle_use",
    "travel_direction",
    "maneuver",
    "towed_i",
    "fire_i",
    "occupant_cnt",
    "exceed_speed_limit_i",
    "first_contact_point",
    "vehicle_config",
    "cargo_body_type",
    "load_type",
    "hazmat_class"
]

vehicle_analysis = vehicle[final_cols].copy()

print("Analysis-ready vehicle shape:", vehicle_analysis.shape)
print(vehicle_analysis.head())

vehicle_analysis.to_csv("vehicle_cleaned.csv", index=False)
print("\nSaved: vehicle_cleaned.csv")

# ── Drop columns with >90% UNKNOWN or NaN ─────────────────────────────────────

# 计算每一列 UNKNOWN 或 NaN 比例
missing_ratio = (
    vehicle_analysis.isna().mean() +
    (vehicle_analysis == "UNKNOWN").mean()
)

missing_ratio = missing_ratio.sort_values(ascending=False)

print(missing_ratio.head(20))

# 删除 UNKNOWN/NaN 比例 > 0.9 的列
cols_to_drop = missing_ratio[missing_ratio > 0.9].index.tolist()

print("Dropping columns:", cols_to_drop)

vehicle_reduced = vehicle_analysis.drop(columns=cols_to_drop)

print("New shape:", vehicle_reduced.shape)

# ── Manual drop of additional low-value columns ────────────────────────────────

manual_drop = [
    "cmrc_veh_i",          # 商业标识，没用
    "towed_i",             # 很 sparse
    "fire_i",              # 极少发生
    "vehicle_config",      # 过细
    "cargo_body_type",
    "load_type",
    "hazmat_class",
    "vehicle_defect"       # 大量 UNKNOWN + 噪音
]

vehicle_reduced = vehicle_reduced.drop(
    columns=[c for c in manual_drop if c in vehicle_reduced.columns]
)

# ── Verification: reload saved CSV ────────────────────────────────────────────

vehicle_file1 = "vehicle_cleaned.csv"
vehicle1 = pd.read_csv(
    vehicle_file1
)
vehicle1
