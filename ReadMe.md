# Price Prediction Web App

## Introduction
This project implements the machine-learning model developed in my previous work. The model predicts real estate prices in Belgium.  
A working version of the web interface is available here:  
https://caveeagle-ml-shiny.share.connect.posit.cloud

## User Interface Overview
The user selects a region on an interactive map, and the *Postal code* field is filled in automatically based on the selected area.  
Next, the user provides the property parameters.  
After clicking **Evaluate property**, the interface returns an estimated price calculated by the model.  
All missing values are handled automatically using a dedicated imputation algorithm.

## Technical Description
Price estimation is performed using an **XGBoost** model created in my earlier project (GitHub repository `ML-studying`, directory `scripts-xgboost`).  
The web application is written in Python using the **Shiny** framework.

## Files and Directories
- **requirements.txt** — list of required Python libraries  
- **app.py** — the main web application file  
- **model_price.py** — script that performs price prediction and implements imputation for missing variables  
- **data/** — directory containing all data required by the model  
- **service_…** — directories with auxiliary files used for preparation and debugging; they are not required for running the model but may be needed when modifying it

