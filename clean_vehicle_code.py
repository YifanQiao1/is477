#!/usr/bin/env python
# coding: utf-8

"""
clean_vehicle_code.py
---------------------
Reads raw vehicle crash data, selects relevant columns, cleans and standardizes
values, removes low-quality rows and low-information columns, and saves the
final result to vehicle_cleaned.csv.
"""

import pandas as pd
import numpy as np


# ── Load raw vehicle data ──────────────────────────────────────────────────────

vehicle_file = "Traffic_Crashes_-_Vehicles.csv"

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
    "HAZMAT_CLASS",
]

vehicle = pd.read_csv(
    vehicle_file,
    usecols=lambda c: c in vehicle_keep_cols,
    low_memory=False,
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
    "occupant_cnt",
]

for col in numeric_cols:
    if col in vehicle.columns:
        vehicle[col] = pd.to_numeric(vehicle[col], errors="coerce")

vehicle.loc[
    (vehicle["vehicle_year"] < 1900) | (vehicle["vehicle_year"] > 2026),
    "vehicle_year",
] = np.nan


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
    "hazmat_class",
]

for col in cat_cols:
    if col in vehicle.columns:
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
    "NOT APPLICABLE": pd.NA,
}

for col in cat_cols:
    if col in vehicle.columns:
        vehicle[col] = vehicle[col].replace(replace_map)


# ── Y/N binary columns → 1/0 ──────────────────────────────────────────────────

yn_cols = [
    "cmrc_veh_i",
    "towed_i",
    "fire_i",
    "exceed_speed_limit_i",
]

for col in yn_cols:
    if col in vehicle.columns:
        vehicle[col] = vehicle[col].map({"Y": 1, "N": 0}).astype("Int64")


# ── Vehicle type simplification ────────────────────────────────────────────────

def simplify_vehicle_type(x):
    if pd.isna(x):
        return "UNKNOWN"

    x = str(x).upper()

    if "MOTORCYCLE" in x or "MOPED" in x or "MOTOR SCOOTER" in x:
        return "MOTORCYCLE"
    elif (
        "PICKUP" in x
        or "VAN" in x
        or "SUV" in x
        or "PASSENGER" in x
        or "AUTOMOBILE" in x
    ):
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


# ── Fill selected categorical missing values ───────────────────────────────────

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
    "hazmat_class",
    "travel_direction",
    "unit_type",
]

for col in fill_unknown_cols:
    if col in vehicle.columns:
        vehicle[col] = vehicle[col].fillna("UNKNOWN")


# ── Drop rows with no useful signal ───────────────────────────────────────────

weak_info_mask = (
    vehicle["vehicle_type"].eq("UNKNOWN")
    & vehicle["maneuver"].eq("UNKNOWN")
    & vehicle["vehicle_use"].eq("UNKNOWN")
)

vehicle = vehicle.loc[~weak_info_mask].copy()


# ── Select analysis columns ────────────────────────────────────────────────────

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
    "hazmat_class",
]

vehicle_analysis = vehicle[[c for c in final_cols if c in vehicle.columns]].copy()

print("Analysis-ready vehicle shape before column reduction:", vehicle_analysis.shape)


# ── Drop high-missing / low-information columns ────────────────────────────────

missing_ratio = (
    vehicle_analysis.isna().mean()
    + (vehicle_analysis == "UNKNOWN").mean(numeric_only=False)
)

missing_ratio = missing_ratio.sort_values(ascending=False)

print("\nTop missing/UNKNOWN ratios:")
print(missing_ratio.head(20))

auto_drop_cols = missing_ratio[missing_ratio > 0.9].index.tolist()

manual_drop = [
    "cmrc_veh_i",
    "towed_i",
    "fire_i",
    "vehicle_config",
    "cargo_body_type",
    "load_type",
    "hazmat_class",
    "vehicle_defect",
    "exceed_speed_limit_i",
]

cols_to_drop = sorted(set(auto_drop_cols + manual_drop))

vehicle_reduced = vehicle_analysis.drop(
    columns=[c for c in cols_to_drop if c in vehicle_analysis.columns]
)

print("\nDropping columns:", [c for c in cols_to_drop if c in vehicle_analysis.columns])
print("Final cleaned vehicle shape:", vehicle_reduced.shape)
print(vehicle_reduced.head())


# ── Save final cleaned vehicle dataset ─────────────────────────────────────────

vehicle_reduced.to_csv("vehicle_cleaned.csv", index=False)

print("\nSaved final cleaned vehicle file: vehicle_cleaned.csv")
print("Final columns:")
print(vehicle_reduced.columns.tolist())