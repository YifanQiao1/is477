# IS477 Final Project Report
Traffic Crash Severity Analysis and Data Integration Project

## Contributors
- Grace Qiao
- Kristin Dai

## Summary
This project investigates traffic crash patterns and crash severity by integrating two complementary datasets: a crash-level dataset and a vehicle-level dataset. The motivation for this project is to better understand how environmental conditions, roadway context, and vehicle-related attributes are associated with severe crashes. Traffic safety is an important public issue, and integrated crash data can support more informed analysis of risk factors and possible prevention strategies.

Our main research questions are:
1. What factors are most associated with severe crashes?
2. How do weather, lighting, roadway, and vehicle characteristics relate to crash outcomes?
3. What additional insight is gained by integrating crash-level and vehicle-level data rather than analyzing only one dataset?

To answer these questions, we used publicly available traffic crash records and vehicle records. We cleaned each dataset separately, standardized key fields, created derived variables, and merged the two datasets using shared identifiers. We then performed exploratory data analysis to examine crash patterns over time, injury severity, environmental conditions, and vehicle characteristics. Our integrated dataset allowed us to connect crash circumstances with vehicle-specific information such as vehicle type, maneuver, and occupant count.

Our findings suggest that crash severity is not evenly distributed across conditions. Severe crashes are more likely under certain combinations of roadway and environmental factors, and some vehicle-related variables provide additional context beyond crash-level information alone. The project demonstrates the importance of data curation in producing a usable and analyzable dataset from raw public safety records. It also shows how integrating multiple datasets can improve the interpretability of traffic safety analysis.

## Data Profile

### Dataset 1: Traffic Crashes - Crashes
- **File location:** `Traffic_Crashes_-_Crashes.csv`
- **Cleaned version:** `crash_cleaned.csv`

This dataset contains crash-level records, including date, time, weather condition, lighting condition, roadway surface condition, trafficway type, first crash type, contributory cause, injury information, and the number of units involved. Each row represents one crash event.

Relevant variables include:
- `crash_record_id`
- `crash_date`
- `weather_condition`
- `lighting_condition`
- `roadway_surface_cond`
- `traffic_control_device`
- `trafficway_type`
- `first_crash_type`
- `prim_contributory_cause`
- `num_units`
- `most_severe_injury`
- `injuries_total`
- `injuries_fatal`

This dataset is central to the project because it captures crash context and crash outcomes.

### Dataset 2: Traffic Crashes - Vehicles
- **File location:** `Traffic_Crashes_-_Vehicles.csv`
- **Cleaned version:** `vehicle_cleaned.csv`

This dataset contains vehicle-level records associated with crash events. It includes vehicle type, vehicle year, vehicle use, travel direction, maneuver, occupant count, and first contact point. Each row represents one unit involved in a crash.

Relevant variables include:
- `crash_record_id`
- `crash_unit_id`
- `unit_no`
- `vehicle_year`
- `vehicle_type`
- `vehicle_category`
- `vehicle_use`
- `travel_direction`
- `maneuver`
- `occupant_cnt`
- `first_contact_point`

This dataset complements the crash-level dataset by adding unit-level and vehicle-related detail.

### Integrated Dataset
- **File location:** `merged_data.csv`

The integrated dataset combines crash-level and vehicle-level information using shared crash identifiers. This merged dataset supports richer analysis of crash severity by linking contextual crash conditions with vehicle-specific characteristics.

### Ethical and Legal Considerations
The datasets used in this project are publicly available government data. Even though the data are public, they concern traffic incidents and injuries, so they should be handled responsibly. We do not attempt to identify individuals. Our analysis focuses on aggregate patterns rather than personal information. We also retain attribution to the original data source and follow the terms of use associated with the source datasets.

## Data Quality
We assessed data quality in terms of completeness, consistency, validity, and usability for analysis. Several issues were identified in the raw datasets.

First, both datasets contained missing values in important columns. For example, some vehicle records had missing vehicle years, and some crash records included unknown or unavailable values for weather, roadway, or injury-related variables. Missingness affected the interpretability of some variables and required selective handling depending on the role of each column in analysis.

Second, the raw datasets contained inconsistent or difficult-to-use categorical values. Several fields used placeholders such as `UNKNOWN`, `UNKNOWN/NA`, or other ambiguous labels. These values reduced analytical clarity and required standardization or grouping.

Third, the crash and vehicle datasets were at different levels of granularity. The crash dataset was organized at the event level, while the vehicle dataset was organized at the unit level. This created integration challenges because the merged data could contain multiple vehicle rows per crash. We therefore documented the relationship between the two datasets and preserved the merged structure appropriately.

Fourth, some variables required transformation before they could be meaningfully analyzed. Date and time fields needed to be converted into year, month, hour, weekday, and weekend indicators. Vehicle year also needed to be transformed into vehicle age to improve interpretability.

Overall, the datasets were sufficiently rich for analysis, but careful cleaning and documentation were necessary before they could support reliable conclusions.

## Data Cleaning
We cleaned the crash and vehicle datasets separately before integration.

For the crash dataset, we standardized column names, parsed date fields, and derived temporal variables such as `crash_year`, `crash_month`, `crash_hour`, `crash_weekday`, and `is_weekend`. We retained variables most relevant to crash context and injury outcome. We also defined a target variable, `severe_crash`, based on injury severity fields in the crash data. In addition, we filtered the dataset to the selected time range used in the project and removed or grouped values that were too sparse or uninformative for analysis.

For the vehicle dataset, we standardized column names, selected analysis-relevant columns, and derived additional variables such as `vehicle_age`. We also grouped vehicle types into broader categories where appropriate to reduce sparsity and improve interpretability. Records with excessive missingness or unusable values were reviewed and handled according to their analytical relevance.

After cleaning the two datasets, we merged them using shared crash identifiers. The merge process preserved the relationship between crash-level and vehicle-level records so that each vehicle record retained the broader crash context. The final integrated dataset was saved as `merged_data.csv`.

Cleaning scripts:
- `clean_crash_code.ipynb`
- `clean_vehicle_code.ipynb`
- `merge_code.ipynb`

## Findings
Our exploratory analysis revealed several notable patterns.

First, crash severity varies across environmental and roadway conditions. Certain weather and lighting conditions appear more frequently in severe crashes than in non-severe crashes. This suggests that external conditions remain an important component of traffic risk.

Second, crash type and contributory cause show meaningful variation in relation to injury severity. Some categories are overrepresented among severe crashes, indicating that not all crash mechanisms carry the same level of risk.

Third, integrating vehicle-level variables provided added context. Variables such as vehicle type, maneuver, occupant count, and vehicle age helped explain differences that are not visible in the crash-level dataset alone.

Fourth, the merged dataset supports richer future modeling because it combines environmental, temporal, and vehicle-specific features in a single analytical table.

Key visualizations from the project are stored in the `figures/` folder and generated in `EDA.ipynb`.

## Future Work
There are several directions for extending this project.

A natural next step is predictive modeling. The merged dataset could be used to build classification models for severe crash prediction using features from both crash and vehicle data. Comparing interpretable models such as logistic regression with more flexible models such as random forests would help assess the predictive value of integrated features.

A second direction is more advanced feature engineering. Additional temporal grouping, spatial analysis, or vehicle-category aggregation could reveal more detailed relationships. If location variables are available and usable, mapping crash hotspots would be especially valuable.

A third direction is improving the integration workflow. The current project successfully merges two complementary datasets, but future work could include a more formal schema design, workflow automation, and stronger provenance documentation.

Finally, future work should further examine data ethics and representational limitations. Public traffic datasets are useful, but they may reflect reporting inconsistencies and institutional biases. Any policy interpretation should therefore be made cautiously.

## Challenges
One major challenge was working with datasets at different levels of granularity. The crash dataset describes crash events, while the vehicle dataset describes units within crashes. This required careful planning during integration to avoid confusion or incorrect assumptions about row-level meaning.

Another challenge was handling missing and ambiguous values. Many public administrative datasets include placeholder values such as `UNKNOWN` or `UNKNOWN/NA`, and deciding when to retain, group, or exclude these values required balancing transparency with analytical usefulness.

A third challenge was selecting an appropriate set of variables for integration and analysis. Both raw datasets contained many columns, but not all were useful for the project’s research questions. We therefore had to make principled decisions about which variables to keep and how to transform them.

Finally, maintaining reproducibility while working in notebooks required extra documentation. To address this, we clearly separated cleaning, merging, and analysis tasks into different notebooks and documented the execution order in the reproduction section below.

## Reproducing

To reproduce this project:

1. Clone the repository.
2. Make sure the following raw data files are available in the project root:
   - `Traffic_Crashes_-_Crashes.csv`
   - `Traffic_Crashes_-_Vehicles.csv`
3. Run the notebooks in the following order:
   - `clean_crash_code.ipynb`
   - `clean_vehicle_code.ipynb`
   - `merge_code.ipynb`
   - `EDA.ipynb`
4. Confirm that the generated output files include:
   - `crash_cleaned.csv`
   - `vehicle_cleaned.csv`
   - `merged_data.csv`
   - figures exported to the `figures/` folder
5. Review the final results and visualizations in the notebook outputs and in this `README.md`.

## Repository Structure

- `Traffic_Crashes_-_Crashes.csv`: raw crash dataset
- `Traffic_Crashes_-_Vehicles.csv`: raw vehicle dataset
- `crash_cleaned.csv`: cleaned crash dataset
- `vehicle_cleaned.csv`: cleaned vehicle dataset
- `merged_data.csv`: merged dataset
- `clean_crash_code.ipynb`: crash cleaning workflow
- `clean_vehicle_code.ipynb`: vehicle cleaning workflow
- `merge_code.ipynb`: dataset integration workflow
- `EDA.ipynb`: exploratory analysis and visualizations
- `data_dictionary.md`: variable documentation
- `requirements.txt`: software dependencies

## References

- City of Chicago. *Traffic Crashes - Crashes*. Dataset.
- City of Chicago. *Traffic Crashes - Vehicles*. Dataset.
- Python Software Foundation. *Python*. Software.
- pandas development team. *pandas*. Software.
- matplotlib development team. *matplotlib*. Software.
- scikit-learn developers. *scikit-learn*. Software, if used.
