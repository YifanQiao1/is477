# Traffic Crash Severity Analysis and Data Integration Project

## Contributors

Grace Qiao  
Kristin Dai  

## Summary

This project investigates traffic crash severity by integrating two complementary public datasets from the City of Chicago: the Traffic Crashes - Crashes dataset and the Traffic Crashes - Vehicles dataset. The project was designed as a data curation and reproducible analysis workflow. Rather than analyzing crash records alone, we aimed to combine crash-level information with vehicle-level information to better understand what conditions and vehicle characteristics are associated with severe crashes.

The main motivation for this project is that traffic crashes are an important public safety issue, but raw administrative datasets are often difficult to use directly. They contain missing values, inconsistent categorical fields, multiple levels of granularity, and many columns that are not equally useful for analysis. A crash-level dataset can describe the overall event, such as weather, lighting, road surface condition, crash type, contributory cause, and injury outcome. However, it does not fully explain the role of individual vehicles involved in the crash. A vehicle-level dataset adds information such as vehicle type, vehicle year, vehicle use, maneuver, travel direction, occupant count, and first contact point. By integrating these two sources, we can produce a more complete research object for studying crash severity.

Our research questions are: What environmental, roadway, temporal, and vehicle-related factors are associated with severe crashes? How does combining crash-level and vehicle-level data improve the analysis compared with using only one dataset? Can a reproducible workflow be created to clean, integrate, analyze, and model traffic crash severity from raw public datasets?

To answer these questions, we developed a full workflow that starts with raw data files and produces cleaned datasets, an integrated dataset, exploratory visualizations, and predictive modeling outputs. The crash data were cleaned using `clean_crash_code.py`, the vehicle data were cleaned using `clean_vehicle_code.py`, the two cleaned datasets were integrated using `merge_code.py`, exploratory analysis was performed using `EDA.py`, and predictive modeling was performed using `modeling.py`. The entire process can be re-run using the shell script `run_all.sh`.

The final integrated dataset, `merged_data.csv`, contains 1,581,057 rows after inner joining the cleaned crash and vehicle datasets on `crash_record_id`. Each row represents one vehicle involved in a crash, enriched with crash-level context. The final severe crash distribution in the merged data is approximately 84.7% non-severe crashes and 15.3% severe crashes.

The modeling step trained Logistic Regression and Random Forest classifiers to predict the binary target variable `severe_crash`. Logistic Regression achieved an accuracy of approximately 0.734 and ROC-AUC of approximately 0.789. Random Forest achieved an accuracy of approximately 0.721 and ROC-AUC of approximately 0.802. Because severe crashes are less frequent than non-severe crashes, ROC-AUC, average precision, and severe-class recall were considered more informative than accuracy alone. The project demonstrates that careful data curation, integration, and documentation are necessary for producing a reproducible and meaningful analysis from raw public safety data.

## Data Profile

This project uses two datasets from Data.gov and the City of Chicago open data system. The two datasets are complementary because one describes crashes at the event level and the other describes vehicles or units involved in those crashes. The shared linkage field is `crash_record_id`, which allows vehicle-level rows to be connected to crash-level context.

The first dataset is Traffic Crashes - Crashes. The raw file in this repository is named `Traffic_Crashes_-_Crashes.csv`, and the cleaned output is named `crash_cleaned.csv`. The source link is: https://catalog.data.gov/dataset/traffic-crashes-crashes. This dataset contains one row per crash event. Its structure is event-level, meaning each record describes the overall crash rather than a specific vehicle. Important variables include `crash_record_id`, `crash_date`, `weather_condition`, `lighting_condition`, `roadway_surface_cond`, `posted_speed_limit`, `traffic_control_device`, `trafficway_type`, `first_crash_type`, `prim_contributory_cause`, `num_units`, `most_severe_injury`, `injuries_total`, and `injuries_fatal`. These variables describe when the crash happened, what road and weather conditions were present, what type of crash occurred, what likely contributed to the crash, and whether injuries or fatalities occurred.

The crash dataset is central to the project because it provides the outcome variable used for analysis and modeling. In the cleaned crash data, we created `severe_crash`, a binary variable indicating whether a crash involved injury or fatality according to the cleaned injury fields. We also derived temporal features such as `crash_year`, `crash_month`, `crash_hour`, `crash_weekday`, and `is_weekend`. These derived fields make it easier to analyze crash patterns across time.

The second dataset is Traffic Crashes - Vehicles. The raw file in this repository is named `Traffic_Crashes_-_Vehicles.csv`, and the cleaned output is named `vehicle_cleaned.csv`. The source link is: https://catalog.data.gov/dataset/traffic-crashes-vehicles. This dataset contains one row per vehicle or unit involved in a crash. Its structure is vehicle-level rather than crash-level, so multiple rows may correspond to the same crash. Important variables include `crash_unit_id`, `crash_record_id`, `unit_no`, `num_passengers`, `unit_type`, `vehicle_id`, `vehicle_year`, `vehicle_type`, `vehicle_category`, `vehicle_use`, `travel_direction`, `maneuver`, `occupant_cnt`, and `first_contact_point`.

The vehicle dataset complements the crash dataset by adding information about the units involved in each crash. For example, the crash dataset may show that a crash occurred during a particular lighting condition or due to a particular contributory cause, but the vehicle dataset can show whether the involved unit was a passenger vehicle, truck, bus, motorcycle, bicycle, or other vehicle category. It also provides information about vehicle age, movement, and occupancy, which are relevant for understanding crash outcomes.

The integrated dataset is `merged_data.csv`. It was created by joining `vehicle_cleaned.csv` with `crash_cleaned.csv` on `crash_record_id`. The final integration uses an inner join so that every retained vehicle row has valid crash-level information. This avoids treating unmatched vehicle records as non-severe crashes and ensures that all rows used in analysis and modeling contain the target variable and core crash context. In the final merged file, each row represents one vehicle involved in a crash, with crash-level fields repeated across all vehicles in the same crash.

There are ethical and legal considerations associated with using these datasets. Although the data are publicly available government records, they describe real traffic incidents that may involve injuries or fatalities. For that reason, this project does not attempt to identify individuals, drivers, passengers, or specific victims. The analysis is conducted at an aggregate level and is intended for data curation, public safety analysis, and reproducible research practice. The raw datasets remain subject to the terms of use of the original data provider. The code and documentation created for this project are part of the project repository, while the original datasets are cited in the references section.

## Data Quality

The raw datasets required substantial quality assessment before they could be used for analysis. We evaluated data quality in terms of completeness, consistency, validity, granularity, linkage quality, and analytical usefulness.

One major issue was missingness. The vehicle dataset contained several fields with extremely high missing or unknown values. For example, fields such as `hazmat_class`, `exceed_speed_limit_i`, `fire_i`, `load_type`, `cargo_body_type`, `vehicle_config`, and `cmrc_veh_i` had missing or unknown rates above 90%. These fields were not useful for general crash severity modeling because nearly all records lacked meaningful information. Keeping them would increase noise, create unnecessary sparse features, and make the modeling pipeline less interpretable. Therefore, these columns were removed during vehicle cleaning.

Another important missingness issue involved `num_passengers` and `vehicle_year`. The final merged data still contains missing values in `num_passengers`, which affects the derived variable `passenger_group`, and missing vehicle years, which affects `vehicle_age`. We did not remove all rows with missing passenger or vehicle age values because doing so would remove a large number of otherwise useful records. Instead, these missing values were documented, and the modeling pipeline uses imputation for numeric features. This approach preserves more data while still allowing reproducible modeling.

A second quality issue was inconsistent categorical representation. The raw data included values such as `UNKNOWN`, `UNABLE TO DETERMINE`, blank strings, and `NOT APPLICABLE`. These values can represent different types of missingness or uncertainty. During cleaning, categorical values were standardized by trimming whitespace, converting text to uppercase, and replacing common ambiguous values with missing values where appropriate. For selected categorical fields needed for analysis, missing values were filled with `UNKNOWN` so that the category would be explicit rather than hidden.

A third issue was the different granularity of the two datasets. The crash dataset is crash-level, while the vehicle dataset is vehicle-level. This means that one crash can correspond to multiple vehicle records. If this relationship is not handled carefully, analysis may accidentally count vehicle rows as if they were independent crash events. We addressed this by clearly documenting that `merged_data.csv` is vehicle-level after integration. In modeling, we also used `GroupShuffleSplit` with `crash_record_id` so that records from the same crash do not appear in both the training and test sets. This reduces leakage across the train-test split.

A fourth quality issue was linkage completeness. Before the final correction, a left join kept vehicle records that did not match the cleaned crash dataset, which created missing crash-level information. This was not appropriate for modeling because unmatched rows could be incorrectly treated as non-severe. The final version uses an inner join, which retained only rows with valid matches in both datasets. The final merge produced 1,581,057 rows with zero missing values for key crash-level variables such as `crash_year`, `crash_month`, `crash_hour`, `weather_condition`, `lighting_condition`, `first_crash_type`, `prim_contributory_cause`, and `severe_crash`.

Finally, there was a risk of data leakage in the modeling stage. Since `severe_crash` is derived from injury-related fields, the model should not use `most_severe_injury`, `injuries_total`, `injuries_fatal`, or `injury_level` as predictors. These fields directly encode the target outcome. The modeling script explicitly drops these leakage columns before training. This improves the validity of the evaluation and ensures that the model is not simply learning from variables that directly define the target.

Overall, the datasets were rich and appropriate for the research questions, but they required systematic cleaning, careful integration, and transparent documentation before they could be used reliably.

## Data Cleaning

The data cleaning process was implemented using Python scripts and designed to be reproducible through `run_all.sh`. The crash dataset and vehicle dataset were cleaned separately before integration.

The crash cleaning process is implemented in `clean_crash_code.py`. The raw crash file `Traffic_Crashes_-_Crashes.csv` originally contained 1,033,146 rows and 33 columns. The script standardized column names, parsed crash dates, filtered the records to crashes from 2018 onward, and selected analysis-relevant fields. Date and time information was transformed into derived variables including `crash_year`, `crash_month`, `crash_hour`, `crash_weekday`, and `is_weekend`. These transformations address the problem that raw datetime fields are difficult to use directly in summary analysis or modeling.

The crash script also created the target variable `severe_crash`. This variable is defined from injury-related crash fields and represents whether the crash involved injury or fatality. The cleaned crash output used for analysis contains 793,246 rows and 21 columns. The severe crash distribution in the cleaned crash data is approximately 84.9% non-severe and 15.1% severe. This imbalance is important for interpreting modeling results because a high accuracy alone could be misleading if a model mostly predicts the majority class.

The vehicle cleaning process is implemented in `clean_vehicle_code.py`. The raw vehicle file `Traffic_Crashes_-_Vehicles.csv` originally contained 2,107,146 rows and 23 selected columns. The script standardized column names, parsed the vehicle crash date, filtered to records from 2018 onward, removed duplicate vehicle unit records, converted numeric columns such as `vehicle_year`, `occupant_cnt`, and `num_passengers`, and standardized categorical fields.

Vehicle year values outside a reasonable range were treated as invalid and converted to missing values. This addressed validity issues where impossible or unrealistic vehicle years could distort the derived `vehicle_age` variable. Categorical values were converted to uppercase and stripped of extra whitespace. Common ambiguous values such as `UNKNOWN`, `UNABLE TO DETERMINE`, and `NOT APPLICABLE` were handled consistently. The script also created `vehicle_category`, a simplified grouping of vehicle types such as passenger vehicle, truck, bus, motorcycle, bicycle, pedestrian, other, or unknown. This grouping reduces sparsity compared with using the raw vehicle type categories.

The vehicle script then assessed the proportion of missing or unknown values in each column. Columns with extremely high missingness or low analytical value were dropped. These included `cargo_body_type`, `cmrc_veh_i`, `exceed_speed_limit_i`, `fire_i`, `hazmat_class`, `load_type`, `towed_i`, `vehicle_config`, and `vehicle_defect`. The final cleaned vehicle file, `vehicle_cleaned.csv`, contains 1,783,023 rows and 15 columns.

Data integration is implemented in `merge_code.py`. The script reads `vehicle_cleaned.csv` and `crash_cleaned.csv`, validates that required columns are present, checks unmatched vehicle rows, and then performs an inner join on `crash_record_id`. An inner join was chosen because the analysis requires crash-level context and a valid `severe_crash` target for each retained row. The script also engineers additional fields including `vehicle_age`, `passenger_group`, and `vehicle_type_group`. The final merged dataset is saved as `merged_data.csv`.

The modeling script, `modeling.py`, includes additional cleaning decisions specific to machine learning. It removes identifiers and high-cardinality columns such as `crash_record_id`, `crash_unit_id`, `vehicle_id`, `crash_date_vehicle`, and `crash_date_crash`. It also removes injury-related leakage columns before training. Numeric features are imputed using median values and scaled, while categorical features are imputed using the most frequent value and one-hot encoded. This produces a consistent and reproducible modeling pipeline.

## Findings

The analysis produced both exploratory findings and modeling results. All plots and model output files are stored in the `figures/` folder.

The exploratory analysis shows that crash severity is not evenly distributed across conditions. Severe crashes account for a minority of cases, approximately 15% of the final merged records. This means the project involves an imbalanced classification problem. A naïve model could achieve relatively high accuracy by predicting most crashes as non-severe, so severity analysis must consider precision, recall, ROC-AUC, and average precision in addition to accuracy.

Environmental and roadway conditions are important for understanding crash severity. Variables such as lighting condition, weather condition, roadway surface condition, trafficway type, and first crash type provide meaningful context for differences in severity. Certain crash types and contributory causes are more strongly associated with severe outcomes than others. These patterns support the value of using crash-level variables rather than only vehicle-level information.

Vehicle-level information adds another layer of interpretation. The integrated dataset allows analysis of vehicle type, vehicle category, maneuver, occupant count, and vehicle age in relation to crash severity. This is important because two crashes with similar weather or road conditions may involve different vehicle types or maneuvers. By integrating vehicle-level and crash-level data, the final dataset supports richer analysis than either dataset alone.

The predictive modeling step trained two baseline classifiers: Logistic Regression and Random Forest. The models were evaluated on a test set created using grouped splitting by `crash_record_id`, so that vehicles from the same crash would not be split across training and testing. This is important because the merged dataset is vehicle-level and multiple rows may share the same crash context.

The Logistic Regression model achieved an accuracy of approximately 0.734, ROC-AUC of approximately 0.789, and average precision of approximately 0.444. Its confusion matrix showed 197,286 true negatives, 70,209 false positives, 13,686 false negatives, and 34,665 true positives. The model had relatively high recall for severe crashes, which means it identified many severe cases, but it also produced many false positives.

The Random Forest model achieved an accuracy of approximately 0.721, ROC-AUC of approximately 0.802, and average precision of approximately 0.453. Its confusion matrix showed 192,590 true negatives, 74,905 false positives, 13,139 false negatives, and 35,212 true positives. Compared with Logistic Regression, Random Forest had slightly higher ROC-AUC and average precision, suggesting that it captured some nonlinear relationships in the data. However, it also had lower overall accuracy because it predicted more crashes as severe.

These results suggest that the integrated dataset contains useful predictive signal, but severe crash prediction remains challenging due to class imbalance and the complexity of traffic safety outcomes. The modeling results should not be interpreted as a final decision-making tool. Instead, they demonstrate that the curated and integrated dataset can support reproducible analysis and baseline predictive modeling.

## Future Work

Future work could improve this project in several directions. The first direction is better feature engineering. The current workflow uses environmental, temporal, roadway, crash type, and vehicle-level features, but additional features could improve interpretation and prediction. For example, if location fields were included and cleaned, the project could analyze spatial patterns, crash hotspots, or neighborhood-level risk. Roadway design, traffic volume, and intersection characteristics could also provide useful context.

A second direction is improving the modeling process. This project uses Logistic Regression and Random Forest as baseline models. Future work could compare additional models such as gradient boosting, XGBoost, LightGBM, or calibrated classifiers. Hyperparameter tuning could also be added using cross-validation. Since severe crashes are relatively rare, future modeling should also test methods designed for imbalanced data, such as threshold tuning, class weighting, resampling, or cost-sensitive evaluation.

A third direction is improving interpretability. Random Forest feature importance provides a basic way to understand which variables are influential, but it is limited. Future work could use permutation importance or SHAP values to better explain how specific features contribute to predicted severity. This would be especially useful if the project were used for policy or public safety discussions.

A fourth direction is improving the workflow and provenance documentation. The current project includes a reproducible shell workflow through `run_all.sh`, but future versions could use a more formal workflow manager such as Snakemake. This would make dependencies between steps more explicit and allow partial reruns when only one input changes. The project could also include checksums for raw files to verify data integrity.

A fifth direction is expanding the documentation and metadata. This repository includes `data_dictionary.md` and `requirements.txt`, but future work could add more complete machine-readable metadata using a standard such as DataCite, DCAT, or Schema.org. This would improve FAIR compliance by making the project easier to find, understand, and reuse.

Finally, future work should continue to consider ethical limitations. Traffic crash data are public, but they reflect real incidents and may contain reporting inconsistencies. Patterns in the data may reflect enforcement practices, reporting practices, infrastructure inequality, or missing context rather than purely behavioral causes. Any policy conclusions should therefore be made carefully and supported by additional domain knowledge.

## Challenges

One major challenge was integrating datasets with different levels of granularity. The crash dataset contains one row per crash event, while the vehicle dataset contains one row per vehicle or unit involved in a crash. This means that the integrated dataset naturally has multiple rows for some crashes. Without careful documentation, this structure could lead to incorrect interpretation. For example, counting rows in the merged dataset does not equal counting unique crashes. We addressed this by clearly defining `merged_data.csv` as vehicle-level and using `crash_record_id` as the integration key.

Another challenge was missing and sparse data. Several columns in the vehicle dataset contained more than 90% missing or unknown values. Keeping these columns would make the dataset larger but not more useful. We therefore assessed missingness and removed high-missingness fields. At the same time, not all missing values could be removed because doing so would discard too many records. For example, `num_passengers` and `vehicle_year` still contain missing values in the final merged data. These fields were retained because they provide useful information when available, and the modeling pipeline handles missing numeric values through imputation.

A third challenge was avoiding data leakage during modeling. Since `severe_crash` is derived from injury-related fields, including `most_severe_injury`, `injuries_total`, `injuries_fatal`, or `injury_level` as predictors would make the model evaluation invalid. The final modeling script explicitly removes these leakage fields before training. We also used group-based splitting by `crash_record_id` to avoid placing vehicles from the same crash in both the training and test sets.

A fourth challenge was making the project reproducible. Earlier versions of the project used Jupyter notebooks, which are useful for exploration but can make automated reproduction harder. To address this, the final project includes Python scripts for each step and a shell script, `run_all.sh`, that executes the complete workflow from cleaning through modeling. This makes it easier for another user or TA to reproduce the project from the repository.

A final challenge was balancing detail and clarity in the final repository. The project includes raw data, cleaned data, merged data, scripts, visualizations, modeling results, dependencies, and documentation. Organizing these artifacts clearly was necessary so that the repository could be understood and evaluated. The final README, data dictionary, and workflow instructions are intended to make each step transparent.

## Reproducing

This project can be reproduced from the repository using the provided Python scripts and shell workflow.

First, clone the repository and make sure the raw data files are available in the project root directory:

- `Traffic_Crashes_-_Crashes.csv`
- `Traffic_Crashes_-_Vehicles.csv`

Install the required software dependencies:


’pip install -r requirements.txt‘

Run the complete workflow:

‘bash run_all.sh‘

The workflow runs the following scripts in order:

- `clean_crash_code.py` cleans the raw crash dataset and creates `crash_cleaned.csv`.
- `clean_vehicle_code.py` cleans the raw vehicle dataset and creates `vehicle_cleaned.csv`.
- `merge_code.py` integrates the cleaned crash and vehicle datasets and creates `merged_data.csv`.
- `EDA.py` performs exploratory data analysis and exports visualizations to the `figures/` folder.
- `modeling.py` trains Logistic Regression and Random Forest models, saves model visualizations, and creates `figures/model_metrics.csv`.

A successful run ends with the message:

Workflow completed successfully.

Expected output files include:

- `crash_cleaned.csv`
- `vehicle_cleaned.csv`
- `merged_data.csv`
- `figures/model_metrics.csv`
- `figures/random_forest_top_features.csv`
- Model confusion matrices, ROC curves, precision-recall curves, threshold curves, and feature importance plots in the `figures/` folder.

The repository also includes `data_dictionary.md`, which documents important variables and derived features, and `requirements.txt`, which lists the Python dependencies needed to run the workflow.

---

## Repository Structure

The repository contains the raw data files, cleaned outputs, scripts, documentation, and result artifacts needed to reproduce the project.

**Data Files**

- `Traffic_Crashes_-_Crashes.csv` — raw crash-level dataset.
- `Traffic_Crashes_-_Vehicles.csv` — raw vehicle-level dataset.
- `crash_cleaned.csv` — cleaned crash dataset produced by `clean_crash_code.py`.
- `vehicle_cleaned.csv` — cleaned vehicle dataset produced by `clean_vehicle_code.py`.
- `merged_data.csv` — integrated analysis dataset produced by `merge_code.py`.

**Scripts**

- `clean_crash_code.py` — cleans and prepares the crash-level data.
- `clean_vehicle_code.py` — cleans and prepares the vehicle-level data.
- `merge_code.py` — integrates the two cleaned datasets.
- `EDA.py` — performs exploratory data analysis and produces visualizations.
- `modeling.py` — trains and evaluates the classification models.
- `run_all.sh` — runs the complete workflow from cleaning through modeling.

**Other Files**

- `figures/` — contains visualization outputs, model evaluation plots, feature importance results, and model metrics.
- `data_dictionary.md` — provides variable definitions and descriptions of derived fields.
- `requirements.txt` — lists software dependencies.
- `README.md` — serves as the final project report.

---

## Contributions

**Grace Qiao** contributed to data cleaning, data processing, exploratory data analysis, workflow automation, and final documentation. This included preparing the cleaned crash and vehicle files, creating the data visualizations, and creating the reproducible shell workflow, and contributing to the final report structure.

**Kristin Dai** contributed to project planning, research question development, data profiling, data quality discussion, documentation review, and interpretation of findings. This included helping evaluate the relevance of the datasets, identifying data quality issues, updating the merge logic to use valid matched records, developing the modeling script, and contributing to the final report.

---

## Compliance, Licensing, and FAIR Documentation

The raw datasets used in this project are public government datasets accessed through Data.gov and the City of Chicago open data system. The project cites the original data sources in the references section. The analysis does not attempt to identify individuals and is presented only in aggregate form.

The repository includes `requirements.txt` to document software dependencies and `data_dictionary.md` to document variables and derived fields. These files support reproducibility and reuse. If a separate license file is included in the repository, it applies to the code and documentation created for this project, not to the original raw datasets, which remain governed by the original provider terms.

---

## References

- City of Chicago. *Traffic Crashes - Crashes*. Data.gov. https://catalog.data.gov/dataset/traffic-crashes-crashes
- City of Chicago. *Traffic Crashes - Vehicles*. Data.gov. https://catalog.data.gov/dataset/traffic-crashes-vehicles