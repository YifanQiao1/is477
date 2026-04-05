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
- Merged vehicle-level and crash-level datasets using `crash_record_id` with a left join
- Verified row count remained consistent with vehicle dataset (382,862 rows)
- Checked for duplicates (none found)
- Identified unmatched records: ~40,809 rows (20,656 unique crash IDs) in vehicle dataset had no corresponding crash-level data
- Observed missing values in crash-related columns due to incomplete overlap between datasets

---

## 2.4 Feature Engineering

**Status:** ✅ Completed 

**Update:**  
- Created crash severity indicator (`severe_crash`) based on injury/fatal conditions
- Generated vehicle-related features:
  - `vehicle_age` (crash year − vehicle year)
  - `passenger_group` (grouped number of passengers)
  - `vehicle_type_group` (simplified vehicle categories)
- Extracted and used existing time-based features:
  - crash hour
  - crash weekday
- Reviewed missing values and confirmed they are either from original vehicle data or caused by unmatched merge


**Next Steps:**  
- Handle missing values (especially vehicle_year and num_passengers)
- Finalize feature transformations
- Encode categorical variables for modeling


**Artifacts:**  
- Merged dataset: `merged_data.csv`
- Merging script: `merge_code.ipynb`

---

## 2.5 Exploratory Data Analysis (EDA)

**Status:** ✅ Completed  

**Update:**  
- Generated some visualizations to explore crash severity patterns:
  - Crash severity distribution  
  - Vehicle type vs severity  
  - Time-of-day trends  
  - Lighting condition vs severity  
  - Weather condition vs severity  
  - Primary contributory cause vs severity  
  - Correlation matrix for key numerical variables  

- Identified:
  - Crash severity is higher during late night and early morning hours  
  - Certain vehicle types (e.g., passenger vehicles, vans) show higher severity rates  
  - Poor lighting and adverse weather conditions are associated with increased severity  
  - Human factors (e.g., following too closely, failing to yield) are strongly linked to severe crashes  
  - Strong correlation between total injuries and severe crash label confirms validity of target variable  

**Insights:**  
Crash severity is influenced by a combination of environmental conditions, vehicle characteristics, and driver behavior. Also, the relatively weak linear correlations for some variables indicate that we might need some complex models to capture nonlinear relationships.

**Artifacts:**  
- EDA notebook: `EDA.ipynb`  
- Visualizations embedded in notebook  

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
| Week 1–2 | Data collection & understanding | ✅ Done | Data collected |
| Week 3 | Data cleaning | ✅ Done | Cleaned missing values |
| Week 4 | Data merging | ✅ Done | Merged two datasets |
| Week 5 | Feature engineering | ✅ Done | Added features into the dataset |
| Week 6 | EDA | ✅ Done | Identified key patterns |
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
- Conducted exploratory data analysis, generating visualizations on crash severity distribution, temporal trends, vehicle types, environmental conditions, and contributory causes  

---

## Kristin Dai

- Created merged dataset  
- Developed feature engineering logic  
- Identified key patterns in EDA to support feature selection and modeling decisions  

---

# 7. Repository Status

- All current progress has been committed to GitHub  
- Repository includes:
  - Raw and processed datasets  
  - Scripts for cleaning, merging, and feature engineering  


---

# 8. Next Steps

- Train baseline models (Logistic Regression, Random Forest)  
- Evaluate model performance using accuracy, F1-score, and ROC-AUC  
- Perform feature importance analysis  
- Prepare final report and presentation  

---

# 9. Conclusion

So far, the project is progressing as expected. We have successfully completed data collection, cleaning, integration, feature engineering, and exploratory data analysis. The EDA results revealed meaningful patterns related to crash severity, which will directly inform the modeling phase. The next stage will focus on building predictive models and identifying the most important factors contributing to severe crashes.