### Overview
The goal of our project is to understand what factors are most associated with severe traffic crashes in Chicago. We focus on identifying conditions that lead to crashes involving injuries or fatalities. By analyzing both crash-level and vehicle-level data, we aim to discover patterns that may help explain why some crashes are more severe than others.

We will use two datasets from the City of Chicago Data Portal: **Traffic Crashes – Crashes** and **Traffic Crashes – Vehicles**. These datasets can be linked using the common identifier `CRASH_RECORD_ID`. The crash dataset provides information such as date, weather condition, lighting condition, road surface, and injury severity. The vehicle dataset includes details about vehicle type, driver age, driver action, and contributing factors.

Our approach includes cleaning both datasets, selecting relevant variables, and merging them using the shared crash identifier. We will create a severity indicator (for example, injury or fatal crash vs. non-injury crash). Then, we will perform exploratory data analysis to examine relationships between environmental factors, driver characteristics, vehicle types, and crash severity. If time allows, we may apply statistical modeling to identify which factors are most strongly associated with severe outcomes.

Through this project, we hope to provide insights that could inform traffic safety policies and prevention strategies in Chicago.

### Team

### Research Question

What factors are most associated with severe crashes in Chicago?

### Datasets

We will use two datasets from the City of Chicago Data Portal:

1. **Traffic Crashes – Crashes**

This dataset contains crash-level information for traffic accidents reported in Chicago. Each row represents one crash. Important variables include crash date and time, location, weather condition, lighting condition, road surface condition, number of injuries, number of fatalities, and primary contributing cause. The dataset also includes a unique identifier called `CRASH_RECORD_ID`, which allows us to link it to the vehicle-level dataset.

2. **Traffic Crashes – Vehicles**

This dataset contains vehicle-level information for each crash. Each row represents one vehicle involved in a crash. It includes variables such as vehicle type, driver age, driver gender, driver action, damage level, and contributing factors. This dataset also contains the `CRASH_RECORD_ID`, which allows us to connect each vehicle to its corresponding crash.

#### Integration Plan
We will join the two datasets using `CRASH_RECORD_ID`. Since one crash may involve multiple vehicles, this is a one-to-many relationship. After merging, we will create a crash severity indicator (for example, injury or fatal crash) and analyze how vehicle characteristics and environmental factors are associated with crash severity.