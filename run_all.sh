#!/bin/bash

set -e

echo "Starting full project workflow"

echo "Step 1: Cleaning crash dataset..."
python clean_crash_code.py

echo "Step 2: Cleaning vehicle dataset..."
python clean_vehicle_code.py

echo "Step 3: Merging cleaned datasets..."
python merge_code.py

echo "Step 4: Running exploratory data analysis..."
python EDA.py

echo "Step 5: Running modeling analysis..."
python modeling.py

echo "======================================"
echo "Workflow completed successfully."
echo "======================================"