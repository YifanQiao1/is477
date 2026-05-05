# Data Dictionary

This document describes the variables in the datasets used for the traffic crash analysis project.

---

## crash_cleaned.csv

| Variable | Type | Description | Values / Range |
|----------|------|-------------|----------------|
| crash_record_id | string | Unique identifier for each crash event | — |
| crash_date | datetime | Date and time of the crash | — |
| crash_year | integer | Year of the crash | 2018–2026 |
| crash_month | integer | Month of the crash | 1–12 |
| crash_hour | integer | Hour of the crash | 0–23 |
| crash_weekday | integer | Day of the week | 0 (Monday) – 6 (Sunday) |
| is_weekend | integer | Whether the crash occurred on a weekend | 0 = weekday, 1 = weekend |
| weather_condition | string | Weather at time of crash | CLEAR, RAIN, SNOW, FOG/SMOKE/HAZE, etc. |
| lighting_condition | string | Lighting at time of crash | DAYLIGHT, DARKNESS, DUSK, DAWN, etc. |
| roadway_surface_cond | string | Road surface condition | DRY, WET, SNOW OR SLUSH, ICE, etc. |
| traffic_control_device | string | Traffic control present at crash location | TRAFFIC SIGNAL, STOP SIGN, NO CONTROLS, etc. |
| trafficway_type | string | Type of roadway | ONE-WAY, TWO-WAY, DIVIDED, etc. |
| first_crash_type | string | Type of first collision | REAR END, ANGLE, SIDESWIPE, FIXED OBJECT, etc. |
| prim_contributory_cause | string | Primary contributing cause of the crash | SPEEDING, FAILING TO YIELD, WEATHER, etc. |
| num_units | integer | Number of vehicles involved in the crash | ≥ 1 |
| most_severe_injury | string | Most severe injury reported in the crash | FATAL, INCAPACITATING INJURY, NO INDICATION OF INJURY, etc. |
| injuries_total | float | Total number of injuries reported | ≥ 0 |
| injuries_fatal | float | Number of fatal injuries | ≥ 0 |
| injury_level | string | Simplified injury severity category | — |
| severe_crash | integer | Target variable: whether the crash involved a fatal or severe injury | 0 = no, 1 = yes |

---

## vehicle_cleaned.csv

| Variable | Type | Description | Values / Range |
|----------|------|-------------|----------------|
| crash_unit_id | integer | Unique identifier for each vehicle record | — |
| crash_record_id | string | Links this vehicle record to a crash event | — |
| crash_date | datetime | Date associated with the vehicle record | — |
| unit_no | integer | Unit number within a crash | ≥ 1 |
| vehicle_id | integer | Numeric identifier for the vehicle | — |
| vehicle_year | float | Manufacturing year of the vehicle | 1900–2026; out-of-range values set to missing |
| unit_type | string | Type of unit | DRIVER, PEDESTRIAN, PEDALCYCLIST, etc. |
| vehicle_type | string | Raw vehicle type from source data | PASSENGER, PICKUP TRUCK, SUV, BUS, etc. |
| vehicle_category | string | Simplified vehicle grouping derived from vehicle_type | PASSENGER_VEHICLE, MOTORCYCLE, TRUCK, BUS, BICYCLE, PEDESTRIAN, OTHER, UNKNOWN |
| vehicle_use | string | Purpose of vehicle use | PERSONAL, TAXI/FOR HIRE, etc. |
| travel_direction | string | Direction of travel at time of crash | N, S, E, W, UNKNOWN |
| maneuver | string | Vehicle maneuver at time of crash | STRAIGHT AHEAD, TURNING LEFT, TURNING RIGHT, BACKING, etc. |
| occupant_cnt | float | Number of occupants in the vehicle | ≥ 0 |
| num_passengers | float | Number of passengers (excluding driver) | ≥ 0 |
| first_contact_point | string | First point of impact on the vehicle | FRONT, REAR, LEFT SIDE, RIGHT SIDE, etc. |

---

## merged_data.csv

Each row represents one vehicle involved in a crash. All variables from `crash_cleaned.csv` and `vehicle_cleaned.csv` are present, plus the derived variables below.

Where a column name exists in both source files, suffixes distinguish them: `_vehicle` (from vehicle data) and `_crash` (from crash data). For example, `crash_date_vehicle` and `crash_date_crash`.

### Additional Derived Variables

| Variable | Type | Description | Values / Range |
|----------|------|-------------|----------------|
| vehicle_age | float | Age of the vehicle at time of crash, calculated as crash_year − vehicle_year | 0–80; values outside this range set to missing |
| passenger_group | category | Binned grouping of num_passengers | `"0"`, `"1-2"`, `"3-5"`, `"5+"` |
| vehicle_type_group | string | Simplified vehicle grouping used for modeling, sourced from vehicle_category when available | PASSENGER_VEHICLE, MOTORCYCLE, TRUCK, BUS, BICYCLE, PEDESTRIAN, OTHER, UNKNOWN |
