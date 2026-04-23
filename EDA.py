#!/usr/bin/env python
# coding: utf-8
"""
EDA.py
------
Exploratory Data Analysis

The dataset has been preprocessed and merged from crash-level and vehicle-level data.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (8, 5)

df = pd.read_csv("merged_data.csv")

df.head()

# ── Dataset Overview ───────────────────────────────────────────────────────────
# We first examine the basic structure of the dataset, including:
# - Number of rows and columns
# - Missing values
# - Key variables used in analysis

print("Shape:", df.shape)
df.info()

df.isnull().sum().sort_values(ascending=False).head(15)

# ── Crash Severity Distribution ────────────────────────────────────────────────
# We analyze the distribution of crash severity using the `severe_crash` variable.
# - 0 → Non-severe crash
# - 1 → Severe crash
# This helps us understand class imbalance and overall risk level.

sns.countplot(data=df, x="severe_crash")
plt.title("Distribution of Crash Severity")
plt.xlabel("Severe Crash (0 = No, 1 = Yes)")
plt.ylabel("Count")
plt.show()

# proportion
df["severe_crash"].value_counts(normalize=True)

# ── Vehicle Type and Crash Severity ───────────────────────────────────────────

top_types = df["vehicle_type"].value_counts().nlargest(10).index
subset = df[df["vehicle_type"].isin(top_types)]

sns.barplot(data=subset, x="vehicle_type", y="severe_crash")
plt.xticks(rotation=45)
plt.title("Top Vehicle Types vs Severity")
plt.show()

# ── Crash Severity by Hour of Day ─────────────────────────────────────────────
# We examine how crash severity varies across different hours of the day.

hourly = df.groupby("crash_hour")["severe_crash"].mean()

hourly.plot()
plt.title("Severity Rate by Hour of Day")
plt.xlabel("Hour")
plt.ylabel("Probability of Severe Crash")
plt.show()

# ── Lighting Condition and Severity ───────────────────────────────────────────

sns.barplot(data=df, x="lighting_condition", y="severe_crash")
plt.xticks(rotation=45)
plt.title("Lighting Condition vs Severity")
plt.show()

# ── Weather Condition and Severity ────────────────────────────────────────────

sns.barplot(data=df, x="weather_condition", y="severe_crash")
plt.xticks(rotation=45)
plt.title("Weather vs Severity")
plt.show()

# ── Road Surface Condition ────────────────────────────────────────────────────

sns.barplot(data=df, x="roadway_surface_cond", y="severe_crash")
plt.xticks(rotation=45)
plt.title("Road Surface vs Severity")
plt.show()

# ── Primary Contributory Cause ────────────────────────────────────────────────

top_causes = df["prim_contributory_cause"].value_counts().nlargest(10).index
subset = df[df["prim_contributory_cause"].isin(top_causes)]

sns.barplot(data=subset, x="prim_contributory_cause", y="severe_crash")
plt.xticks(rotation=45)
plt.title("Top Causes vs Severity")
plt.show()

# ── Correlation Analysis ──────────────────────────────────────────────────────

numeric_cols = [
    "crash_hour",
    "num_units",
    "injuries_total",
    "occupant_cnt",
    "severe_crash"
]

corr = df[numeric_cols].corr()

sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Correlation Matrix")
plt.show()

# ── Key Findings ──────────────────────────────────────────────────────────────
#
# From the exploratory data analysis, we found several patterns:
#
# 1. Temporal Patterns
#    Crash severity shows a clear time-of-day pattern. Severity is highest during
#    late night and early morning hours (approximately 0:00–4:00), decreases during
#    daytime, and rises again in the evening. This suggests that low visibility and
#    driver fatigue may contribute to more severe crashes.
#
# 2. Vehicle Type Differences
#    Certain vehicle types, such as passenger vehicles and vans/minivans, exhibit
#    higher severity rates compared to others. In contrast, smaller or less common
#    vehicle categories tend to have lower severity rates.
#
# 3. Lighting Conditions
#    Crashes occurring in darkness with lighting show the highest severity levels,
#    even higher than pure darkness. This may reflect high-speed urban environments
#    where lighting exists but risk remains elevated.
#
# 4. Weather Impact
#    Adverse weather conditions such as fog, snow, and strong winds are associated
#    with higher crash severity. Clear weather generally corresponds to lower severity.
#
# 5. Primary Contributory Causes
#    Human-related factors play a dominant role. Behaviors such as following too
#    closely, failing to yield, and improper turning are strongly associated with
#    higher severity crashes.
#
# 6. Correlation Insights
#    The correlation analysis shows a strong positive relationship between total
#    injuries and severe crashes, validating the target variable definition.
#    Other variables have relatively weak direct correlations, suggesting that
#    nonlinear models may be more effective.
