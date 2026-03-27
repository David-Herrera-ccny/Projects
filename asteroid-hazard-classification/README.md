# Asteroid Hazard Classification (NASA Dataset)

## Overview
This project develops machine learning models to classify whether an asteroid is potentially hazardous (PHA) based on its orbital and physical characteristics. The goal is to improve the detection of rare but high-risk events.

## Problem
The dataset contains extreme class imbalance (~0.2% hazardous asteroids), making traditional accuracy metrics misleading. The objective is to build models that effectively identify hazardous asteroids while minimizing missed threats.

## Dataset
- Source: NASA JPL Asteroid Dataset (Kaggle)
- ~900,000+ observations
- Features include orbital mechanics and physical characteristics
- Target variable: `pha` (Potentially Hazardous Asteroid)

## Methods
- Data cleaning and feature selection
- Handling class imbalance using:
  - Class weighting
  - Sampling techniques
- Models implemented:
  - Logistic Regression
  - K-Nearest Neighbors (KNN)
  - Support Vector Classifier (SVC)
  - Random Forest
- Model evaluation using:
  - Precision, Recall, Accuracy scores
  - Confusion matrices
  - ROC curves
- Feature importance and ablation studies

## Key Results
- Random Forest achieved the strongest overall performance
- Absolute magnitude (`H`) was a more important predictor than MOID
- Recall was prioritized over precision due to real-world risk implications (missing a hazardous asteroid is more critical than false alarms)

## Tech Stack
- Python
- Pandas, NumPy
- scikit-learn
- Matplotlib / Seaborn

## Repository Structure
- `asteroid-hazard-classification.ipynb` – model development and evaluation
- `README.md` – project overview

## Future Improvements
- Apply SMOTE or other synthetic data techniques to address class imbalance
- Explore additional datasets with richer feature coverage
- Test model performance without key predictors (feature robustness)

## Author
David Herrera
