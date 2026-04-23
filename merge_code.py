#!/usr/bin/env python
# coding: utf-8
"""
merge_code.py
-------------
Step 3 of the data management pipeline.
Merges cleaned vehicle data with cleaned crash data on crash_record_id,
engineers key features, validates the merge, and saves the final dataset.
"""

import pandas as pd

# ── Load cleaned datasets ──────────────────────────────────────────────────────

cleaned_vehicle = pd.read_csv('vehicle_cleaned.csv')
cleaned_crash = pd.read_csv('crash_cleaned.csv')

cleaned_vehicle.head()

cleaned_crash.head()

cleaned_vehicle.info()

cleaned_crash.info()

# ── Merge vehicle and crash data ───────────────────────────────────────────────

merged = cleaned_vehicle.merge(
    cleaned_crash,
    on='crash_record_id',
    how='left'
)
merged.head()

# ── Feature engineering ────────────────────────────────────────────────────────

# Target variable: severe crash (any injury or fatality)
merged['severe_crash'] = (
    (merged['injuries_total'] > 0) | (merged['injuries_fatal'] > 0)
).astype(int)
merged.head()

# Derived features
merged['vehicle_age'] = merged['crash_year'] - merged['vehicle_year']
merged['passenger_group'] = pd.cut(
    merged['num_passengers'],
    bins=[-1, 0, 2, 5, 100],
    labels=['0', '1-2', '3-5', '5+']
)
merged['vehicle_type_group'] = merged['vehicle_type'].replace({
    'PASSENGER': 'car',
    'SUV': 'car',
    'TRUCK': 'truck',
    'MOTORCYCLE': 'motorcycle'
})
merged.head()

# ── Merge validation ───────────────────────────────────────────────────────────

print(len(merged), len(cleaned_vehicle))
print(merged.duplicated().sum())
print(merged.isnull().sum())

print(cleaned_vehicle.isnull().sum())

print(merged[merged['crash_year'].isna()].shape)
print(merged[merged['crash_year'].isna()]['crash_record_id'].nunique())

# Check unmatched vehicle records (crash_record_id not found in crash table)
unmatched = cleaned_vehicle.loc[
    ~cleaned_vehicle['crash_record_id'].isin(cleaned_crash['crash_record_id'])
]

print(len(unmatched))
print(unmatched['crash_record_id'].nunique())

# ── Save final merged dataset ──────────────────────────────────────────────────

merged.to_csv('merged_data.csv', index=False)
