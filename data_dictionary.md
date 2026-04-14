# Data Dictionary

This document describes the variables used in the cleaned and merged datasets for the traffic crash analysis project.

---

## Dataset: crash_cleaned.csv

### Identifiers
- **crash_record_id**: Unique identifier for each crash event.
- **crash_date**: Date and time when the crash occurred.

### Time Features (Derived)
- **crash_year**: Year of the crash.
- **crash_month**: Month of the crash (1–12).
- **crash_hour**: Hour of the crash (0–23).
- **crash_weekday**: Day of the week (0 = Monday, 6 = Sunday).
- **is_weekend**: Indicator variable (1 = weekend, 0 = weekday).

### Environmental Conditions
- **weather_condition**: Weather at the time of the crash (e.g., CLEAR, RAIN, SNOW).
- **lighting_condition**: Lighting condition (e.g., DAYLIGHT, DARKNESS).
- **roadway_surface_cond**: Condition of the road surface.
- **traffic_control_device**: Traffic control present (e.g., SIGNAL, STOP SIGN).
- **trafficway_type**: Type of roadway (e.g., ONE-WAY, TWO-WAY).

### Crash Characteristics
- **first_crash_type**: Type of first collision (e.g., REAR END, ANGLE).
- **prim_contributory_cause**: Primary cause of the crash (e.g., SPEEDING, WEATHER).
- **num_units**: Number of units (vehicles) involved in the crash.

### Injury Information
- **most_severe_injury**: Severity classification of the crash.
- **injuries_total**: Total number of injuries reported.
- **injuries_fatal**: Number of fatal injuries.
- **injury_level**: Simplified injury severity category.

### Target Variable
- **severe_crash**: Binary indicator of crash severity.
  - Defined as 1 if the crash involves fatal or severe injury.
  - Defined as 0 otherwise.

---

## Dataset: vehicle_cleaned.csv

### Identifiers
- **crash_unit_id**: Unique identifier for each unit (vehicle).
- **crash_record_id**: Identifier linking the vehicle to a crash.
- **unit_no**: Unit number within a crash.

### Vehicle Information
- **vehicle_id**: Unique identifier for the vehicle.
- **vehicle_year**: Manufacturing year of the vehicle.
- **vehicle_age**: Derived variable = crash_year - vehicle_year.

### Vehicle Classification
- **vehicle_type**: Type of vehicle (e.g., PASSENGER, PICKUP).
- **vehicle_category**: General category (e.g., PASSENGER_VEHICLE).
- **vehicle_use**: Purpose of vehicle use (e.g., PERSONAL).

### Movement Information
- **travel_direction**: Direction of travel (N, S, E, W).
- **maneuver**: Vehicle maneuver at the time of crash (e.g., STRAIGHT AHEAD, TURNING).

### Occupancy
- **occupant_cnt**: Number of occupants in the vehicle.
- **num_passengers**: Number of passengers reported.

### Collision Information
- **first_contact_point**: First point of impact on the vehicle.

---

## Dataset: merged_data.csv

This dataset combines crash-level and vehicle-level information using `crash_record_id`.

Each row represents a vehicle involved in a crash, enriched with crash-level context.

### Key Notes
- Multiple rows may correspond to the same crash (one per vehicle).
- Crash-level variables are duplicated across vehicle records.
- This dataset enables analysis of crash severity using both environmental and vehicle-related features.

---

## Derived Features Summary

- **vehicle_age**: Calculated from vehicle_year and crash_year.
- **is_weekend**: Derived from crash_weekday.
- **severe_crash**: Derived from injury severity fields.

---

## Data Limitations

- Missing values exist in several columns (e.g., vehicle_year, weather_condition).
- Some categorical variables include "UNKNOWN" or "NA" values.
- Vehicle-level data may not fully capture driver behavior.
- Crash severity is based on reported injury data, which may be incomplete.

---
