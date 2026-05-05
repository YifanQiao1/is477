#!/usr/bin/env python
# coding: utf-8

"""
merge_code.py
-------------
Merges cleaned vehicle data with cleaned crash data on crash_record_id,
engineers key features, validates the merge, and saves merged_data.csv.
"""

import pandas as pd


# ── Load cleaned datasets ──────────────────────────────────────────────────────

cleaned_vehicle = pd.read_csv("vehicle_cleaned.csv", low_memory=False)
cleaned_crash = pd.read_csv("crash_cleaned.csv", low_memory=False)

print("Cleaned vehicle shape:", cleaned_vehicle.shape)
print("Cleaned crash shape:", cleaned_crash.shape)


# ── Basic validation before merge ──────────────────────────────────────────────

required_vehicle_cols = ["crash_record_id", "crash_unit_id"]
required_crash_cols = ["crash_record_id", "severe_crash", "crash_year"]

for col in required_vehicle_cols:
    if col not in cleaned_vehicle.columns:
        raise ValueError(f"Missing required vehicle column: {col}")

for col in required_crash_cols:
    if col not in cleaned_crash.columns:
        raise ValueError(f"Missing required crash column: {col}")

cleaned_vehicle = cleaned_vehicle.dropna(subset=["crash_record_id"])
cleaned_crash = cleaned_crash.dropna(subset=["crash_record_id"])

cleaned_vehicle["crash_record_id"] = cleaned_vehicle["crash_record_id"].astype(str)
cleaned_crash["crash_record_id"] = cleaned_crash["crash_record_id"].astype(str)


# ── Check unmatched vehicle records before merge ───────────────────────────────

unmatched = cleaned_vehicle.loc[
    ~cleaned_vehicle["crash_record_id"].isin(cleaned_crash["crash_record_id"])
]

print("Unmatched vehicle rows before inner merge:", len(unmatched))
print("Unmatched unique crash_record_id:", unmatched["crash_record_id"].nunique())


# ── Merge vehicle and crash data ───────────────────────────────────────────────
# Use inner merge because the project analysis requires crash-level variables.
# This avoids treating unmatched crash records as non-severe by mistake.

merged = cleaned_vehicle.merge(
    cleaned_crash,
    on="crash_record_id",
    how="inner",
    suffixes=("_vehicle", "_crash"),
)

print("Merged shape:", merged.shape)


# ── Feature engineering ────────────────────────────────────────────────────────

# Use severe_crash from crash_cleaned.csv directly.
# Do not recreate it here from injury fields, because that can introduce errors
# if crash-level fields are missing.
merged["severe_crash"] = merged["severe_crash"].astype(int)

# Vehicle age
if "vehicle_year" in merged.columns and "crash_year" in merged.columns:
    merged["vehicle_age"] = merged["crash_year"] - merged["vehicle_year"]

    merged.loc[
        (merged["vehicle_age"] < 0) | (merged["vehicle_age"] > 80),
        "vehicle_age",
    ] = pd.NA

# Passenger group
if "num_passengers" in merged.columns:
    merged["passenger_group"] = pd.cut(
        merged["num_passengers"],
        bins=[-1, 0, 2, 5, 100],
        labels=["0", "1-2", "3-5", "5+"],
    )

# Vehicle type group
if "vehicle_category" in merged.columns:
    merged["vehicle_type_group"] = merged["vehicle_category"]
elif "vehicle_type" in merged.columns:
    merged["vehicle_type_group"] = merged["vehicle_type"].replace(
        {
            "PASSENGER": "PASSENGER_VEHICLE",
            "SUV": "PASSENGER_VEHICLE",
            "TRUCK": "TRUCK",
            "MOTORCYCLE": "MOTORCYCLE",
        }
    )


# ── Merge validation ───────────────────────────────────────────────────────────

print("\nMerge validation")
print("Rows in cleaned_vehicle:", len(cleaned_vehicle))
print("Rows in cleaned_crash:", len(cleaned_crash))
print("Rows in merged_data:", len(merged))
print("Duplicate full rows:", merged.duplicated().sum())

print("\nSevere crash distribution:")
print(merged["severe_crash"].value_counts(normalize=True, dropna=False))

print("\nMissing values in important merged columns:")
important_cols = [
    "crash_record_id",
    "crash_unit_id",
    "crash_year",
    "crash_month",
    "crash_hour",
    "weather_condition",
    "lighting_condition",
    "first_crash_type",
    "prim_contributory_cause",
    "vehicle_type",
    "vehicle_category",
    "vehicle_age",
    "passenger_group",
    "severe_crash",
]

available_important_cols = [c for c in important_cols if c in merged.columns]
print(merged[available_important_cols].isna().sum())


# ── Save final merged dataset ──────────────────────────────────────────────────

merged.to_csv("merged_data.csv", index=False)

print("\nSaved final merged dataset: merged_data.csv")
print("Final merged columns:")
print(merged.columns.tolist())