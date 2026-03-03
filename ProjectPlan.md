### Overview
The goal of our project is to understand what factors are most associated with severe traffic crashes in Chicago. We focus on identifying conditions that lead to crashes involving injuries or fatalities. By analyzing both crash-level and vehicle-level data, we aim to discover patterns that may help explain why some crashes are more severe than others.

We will use two datasets from the City of Chicago Data Portal: **Traffic Crashes – Crashes** and **Traffic Crashes – Vehicles**. These datasets can be linked using the common identifier `CRASH_RECORD_ID`. The crash dataset provides information such as date, weather condition, lighting condition, road surface, and injury severity. The vehicle dataset includes details about vehicle type, driver age, driver action, and contributing factors.

Our approach includes cleaning both datasets, selecting relevant variables, and merging them using the shared crash identifier. We will create a severity indicator (for example, injury or fatal crash vs. non-injury crash). Then, we will perform exploratory data analysis to examine relationships between environmental factors, driver characteristics, vehicle types, and crash severity. If time allows, we may apply statistical modeling to identify which factors are most strongly associated with severe outcomes.

Through this project, we hope to provide insights that could inform traffic safety policies and prevention strategies in Chicago.
