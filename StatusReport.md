# 🚗 Traffic Crash Severity Analysis  
## Milestone 3: Status Report  

**Team Members:**  
- Grace Qiao
- Kristin dai


# 1. Project Overview

This project aims to analyze the key factors that influence the severity of traffic crashes using datasets from the City of Chicago. By integrating crash-level and vehicle-level data, we aim to identify patterns and build predictive insights regarding injury or fatal crashes.

---

# 2. Progress Update on Project Plan Tasks


## 2.1 Data Collection & Understanding

**Status:** ✅ Completed  

**Update:**  
- Successfully obtained datasets:
  - Traffic Crashes – Crashes  
  - Traffic Crashes – Vehicles  
- Identified key linking field: `CRASH_RECORD_ID`  
- Reviewed dataset schema and selected relevant variables  

**Artifacts:**  
- Dataset files: `Traffic_Crashes_-_Crashes.csv`  `Traffic_Crashes_-_Vehicles.csv`
- Data dictionary notes: `路径`  

---

## 2.2 Data Cleaning & Preprocessing

**Status:** ✅ Completed  

**Update:**  
- Removed missing or invalid values (e.g., null vehicle types, unknown categories)  
- Standardized column formats (dates, categorical values)  
- Selected relevant variables such as:
  - vehicle_type  
  - occupant_cnt  

**Artifacts:**  
- Cleaning script: `clean_crash_code.ipynb`  `clean_vehicle_code.ipynb`  
- Clean dataset: `crash_cleaned.csv`  `vehicle_cleaned.csv`  

---

## 2.3 Data Integration (Merging Datasets)

**Status:** ✅ Completed  

**Update:**  
- Successfully merged crash-level and vehicle-level datasets using `CRASH_RECORD_ID`  
- Verified merge correctness and removed duplicate entries  

**Artifacts:**  
- Merge script: `/s`  
- Merged dataset: `/da`  

---

## 2.4 Feature Engineering

**Status:** ✅ Completed 

**Update:**  
- Created severity indicator (binary classification: injury/fatal vs non-injury)  
- Extracted time-based features:
  - hour of crash  
  - day of week  
- Started categorizing environmental factors  

**Next Steps:**  
- Finalize feature transformations  
- Encode categorical variables  

**Artifacts:**  
- Feature engineering script: `/scripts/feature_engineering.py`  

---

## 2.5 Exploratory Data Analysis (EDA)

**Status:** 🔄 In Progress  

**Update:**  
- Generated initial visualizations:
  - crash severity distribution  
  - vehicle type vs severity  
  - time-of-day trends  
- Identified preliminary patterns (e.g., higher severity at night)  

**Artifacts:**  
- EDA notebook: `/notebooks/EDA.ipynb`  
- Visualizations: `/outputs/figures/`  

---

## 2.6 Modeling (Planned)

**Status:** ⏳ Not Started  

**Plan:**  
- Train classification models:
  - Logistic Regression  
  - Random Forest  
- Evaluate using:
  - Accuracy  
  - F1-score  
  - ROC-AUC  

---

# 3. Updated Timeline

| Week | Task | Status | Notes |
|------|------|--------|------|
| Week 1–2 | Data collection & understanding | ✅ Done | Completed as planned |
| Week 3 | Data cleaning | ✅ Done | Minor missing value issues |
| Week 4 | Data merging | ✅ Done | Successfully linked datasets |
| Week 5 | Feature engineering | 🔄 In Progress | Will finalize soon |
| Week 6 | EDA | 🔄 In Progress | Initial plots completed |
| Week 7 | Modeling | ⏳ Planned | |
| Week 8 | Final report & GitHub release | ⏳ Planned | |

---

# 4. Changes to Project Plan

Compared to our original proposal, we made the following adjustments:

- Simplified feature set to focus on the most relevant variables (to reduce noise)
- 

**Reason for Changes:**  
These adjustments were made to improve data quality and ensure that our analysis is more reliable and interpretable.

---

# 5. Challenges and Solutions

## Challenge 1: Missing and Inconsistent Data  
**Issue:**  
Many fields contained missing values or “UNKNOWN/NA” entries  

**Solution:**  
- Removed or filtered invalid rows  
- Standardized categorical values  

---

## Challenge 2: Dataset Merging Issues  
**Issue:**  
Mismatch and duplicates when merging datasets  

**Solution:**  
- Verified unique `CRASH_RECORD_ID`  
- Removed duplicate records after merging  

---

## Challenge 3: Feature Selection  
**Issue:**  
Too many variables made analysis complex  

**Solution:**  
- Selected key variables based on relevance  
- Reduced dimensionality for clearer analysis  

---

# 6. Individual Contributions


## Grace Qiao

- Implemented data cleaning pipeline for both datasets
- Processed raw datasets and handled missing values  
- Contributed to EDA analysis  

---

## Kristin Dai

- Created merged dataset  
- Developed feature engineering logic  
- Generated initial visualizations  

---

# 7. Repository Status

- All current progress has been committed to GitHub  
- Repository includes:
  - Raw and processed datasets  
  - Scripts for cleaning, merging, and feature engineering  
  - EDA notebooks  
- Created release: **status-report**

---

# 8. Next Steps

- Complete feature engineering  
- Finalize EDA insights  
- Train and evaluate models  
- Prepare final report and presentation  

---

# 9. Conclusion

So far, the project is progressing as expected. We have successfully completed data collection, cleaning, and integration, and are currently working on feature engineering and exploratory analysis. The next phase will focus on modeling and deriving actionable insights from the data.