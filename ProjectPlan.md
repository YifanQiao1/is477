### Overview
The goal of our project is to understand what factors are most associated with severe traffic crashes in Chicago. We focus on identifying conditions that lead to crashes involving injuries or fatalities. By analyzing both crash-level and vehicle-level data, we aim to discover patterns that may help explain why some crashes are more severe than others.

We will use two datasets from the City of Chicago Data Portal: **Traffic Crashes – Crashes** and **Traffic Crashes – Vehicles**. These datasets can be linked using the common identifier `CRASH_RECORD_ID`. The crash dataset provides information such as date, weather condition, lighting condition, road surface, and injury severity. The vehicle dataset includes details about vehicle type, driver age, driver action, and contributing factors.

Our approach includes cleaning both datasets, selecting relevant variables, and merging them using the shared crash identifier. We will create a severity indicator (for example, injury or fatal crash vs. non-injury crash). Then, we will perform exploratory data analysis to examine relationships between environmental factors, driver characteristics, vehicle types, and crash severity. If time allows, we may apply statistical modeling to identify which factors are most strongly associated with severe outcomes.

Through this project, we hope to provide insights that could inform traffic safety policies and prevention strategies in Chicago.


## Team Roles and Responsibilities  

### Grace Qiao – Crash Dataset & Environmental Analysis  

- Download and document crash-level dataset acquisition  
- Clean and preprocess the Traffic Crashes – Crashes dataset  
- Standardize environmental variables (weather, lighting, road condition)  
- Create crash severity indicator  
- Conduct environmental factor analysis  
- Contribute to documentation and workflow automation  

### Kristin Dai – Vehicle Dataset & Driver-Level Analysis  

- Download and document vehicle-level dataset acquisition  
- Clean and preprocess the Traffic Crashes – Vehicles dataset  
- Standardize driver and vehicle-related variables  
- Engineer vehicle-related features (vehicle category, driver age groups)  
- Conduct driver and vehicle factor analysis  
- Contribute to documentation and workflow automation  

### Shared Responsibilities  

- Design data storage structure  
- Merge datasets using `CRASH_RECORD_ID`  
- Validate integration results  
- Perform modeling and interpretation  
- Implement automated workflow (Snakemake or run-all script)  
- Write final report and ensure reproducibility  

### Research Question

What factors are most associated with severe crashes in Chicago?

### Additional sub-RQs  

RQ1: Are environmental conditions (weather, lighting, road surface) significantly associated with crash severity?  
RQ2: Do certain vehicle types (e.g., motorcycles, trucks) increase the likelihood of severe outcomes?  


### Datasets

We will use two datasets from the City of Chicago Data Portal:

1. **Traffic Crashes – Crashes**

This dataset contains crash-level information for traffic accidents reported in Chicago. Each row represents one crash. Important variables include crash date and time, location, weather condition, lighting condition, road surface condition, number of injuries, number of fatalities, and primary contributing cause. The dataset also includes a unique identifier called `CRASH_RECORD_ID`, which allows us to link it to the vehicle-level dataset.

2. **Traffic Crashes – Vehicles**

This dataset contains vehicle-level information for each crash. Each row represents one vehicle involved in a crash. It includes variables such as vehicle type, driver age, driver gender, driver action, damage level, and contributing factors. This dataset also contains the `CRASH_RECORD_ID`, which allows us to connect each vehicle to its corresponding crash.

#### Integration Plan
We will join the two datasets using `CRASH_RECORD_ID`. Because the relationship is one-to-many:

- We will first clean both datasets separately.  
- Then merge them using an inner join.  

We will carefully validate:

- Duplicate crash records  
- Consistency of severity labels  
- Row counts before and after merging  

---

## Timeline（6 Steps）

### Week 1 – Project Setup & Data Acquisition
- **Tasks:**  
  - Finalize research question  
  - Download Traffic Crashes – Crashes and Traffic Crashes – Vehicles datasets  
  - Review data dictionaries and variable definitions  
  - Initialize GitHub repository and set up folder structure  
- **Estimated Completion:** Week 1, Day 2  
- **Responsible:** Grace & Kristin (shared)

---

### Week 2 – Data Profiling & Cleaning
- **Tasks:**  
  - Examine missing values and duplicates in both datasets  
  - Standardize column names and data types  
  - Handle missing or invalid values  
  - Document cleaning steps for reproducibility  
- **Estimated Completion:** Week 2, Day 3  
- **Responsible:**  
  - Grace – Crash-level dataset cleaning  
  - Kristin – Vehicle-level dataset cleaning  
  - All – Document cleaning process

---

### Week 3 – Data Integration & Feature Engineering
- **Tasks:**  
  - Merge datasets using `CRASH_RECORD_ID`  
  - Create crash severity indicator (injury/fatal vs. non-injury)  
  - Group driver ages, categorize vehicle types, and create aggregated features if needed  
  - Validate merged dataset (check counts, duplicates, consistency)  
- **Estimated Completion:** Week 3, Day 2  
- **Responsible:** All team members

---

### Week 4 – Exploratory Data Analysis
- **Tasks:**  
  - Generate summary statistics and frequency tables  
  - Visualize relationships between environmental factors, driver/vehicle characteristics, and crash severity  
  - Identify patterns and preliminary insights for modeling  
- **Estimated Completion:** Week 4, Day 2  
- **Responsible:**  
  - Grace – Environmental factors  
  - Kristin – Driver & vehicle factors  
  - All – Cross-factor analysis

---

### Week 5 – Modeling & Interpretation
- **Tasks:**  
  - Run classification models (e.g., logistic regression) to predict crash severity  
  - Identify most significant predictors  
  - Interpret model results and evaluate performance  
  - Document assumptions and limitations  
- **Estimated Completion:** Week 5, Day 3  
- **Responsible:** All team members

---

### Week 6 – Final Report & Workflow Documentation
- **Tasks:**  
  - Write final report summarizing datasets, methods, findings, and reproducibility steps  
  - Include all visualizations and tables  
  - Verify workflow automation (run-all script or Snakemake)  
  - Final repository review and commit  
- **Estimated Completion:** Week 6, Day 3  
- **Responsible:** All team members


## Constraints  
### Large Dataset Size  

Both datasets contain millions of records. Potential challenges include:

- CSV files may exceed GitHub’s 100MB file size limit.  
- Merging large datasets may increase processing time.  
- Memory limitations during integration.  

Mitigation strategies:

- Store large raw files externally if necessary.  
- Optimize data types or columns to reduce memory usage.  
- Consider chunk-based reading for large files.  

---

### Data Completeness  

- Missing weather or driver information.  
- Inconsistent categorical coding across years.  

---


### Ethical and Legal Considerations  

- Data includes injury and fatality information.  
- Must comply with data portal terms of use.  
- Avoid re-identification risks even if data is anonymized.  

---

## Gaps and Areas Needing Further Input  

### Data Storage Strategy  

If raw files exceed GitHub limits:

- Decide whether to host raw data externally.  （其实我们已经确定了通过LFS上传？）
- Decide whether to commit only cleaned subsets.  

---

### Aggregation Strategy  

When merging:

- Determine whether analysis should occur at crash-level or vehicle-level.  
- Decide how to summarize multiple vehicles per crash.  

---

### Modeling Scope  

- Select appropriate statistical models.  
- Address potential class imbalance if severe crashes are rare.  

---

### Computational Efficiency  

Large merges may require:

- Data type optimization  
- Efficient join strategy (要不要保留这么多bullet point)
---


## Anticipation of Future Course Topics  

This project will incorporate:

- Data lifecycle modeling  
- Data integration using relational joins  
- Data quality assessment  
- Metadata documentation  
- Workflow automation  
- Reproducibility best practices  

The project plan may evolve as we receive feedback and encounter technical constraints.