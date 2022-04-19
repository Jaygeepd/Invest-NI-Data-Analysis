# In this file we will be building a classifier using the features in the
# Invest NI database

"""
There are a few different classifications we want to make using the invest NI
database, which are defined below
Problem Definitions:
1. In the data, I have created two additional columns to try and measure
success for an investment. The first is the "Average Mean Grade", which
measures the return of an investment on a scale between 0 and 1, with 0
being no gain (Total Assistance = Total Investment)
    The goal of the first classification model is to try and use the following
features to determine if a business falls above or below this average value:
    - SME, determines if a business is a "Small to Medium Enterprise"
    - Ownership, broken into Local owners from Northern Ireland or External
    - Jobs Created, this tracks if the business was expected to create new jobs
    - Sector, the business sector that the business operates in
    - Condition, which are the conditions that the assistance has been provided
    for

2. The second classification will repeat the above experiment, but instead we
will try and use the Average Grade accounting for rows which have a gain of
zero.

3. Our third classification will instead use the features laid out in the first
model but will instead try and predict if the investment is above or below
the "Business Plan Grade". This number comes from an article posted by
Invest NI which claims that between 2016-2021 every £1 of assistance provided
£6 in total investment, which is also the period of time that our dataset
covers.
    The goal is similar to the first two models but we are applying to a
different metric of success.
"""

# Imports
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import GridSearchCV
from xgboost.sklearn import XGBClassifier

# Get the Invest Data
data_path = "Data/appended_data.csv"
zero_removed_path = "Data/zero_removed_data.csv"

# Read in the training data
overall_data = pd.read_csv(data_path, engine="python")
zero_removed_data = pd.read_csv(zero_removed_path, engine="python")

# Split out the overall data - Testing is used in the model_tests.py file
training_data = overall_data[:6500]

# Split out zero removed data - Testing is used in the model_tests.py file
zero_train_data = zero_removed_data[:6000]

# Set our random seed
np.random.seed(0)


# Function to classify the average grade data
def grade_classifier():
    # Create our testing and training data from the overall data
    grade_trainer = training_data.drop(columns=["Average Grade"])
    grade_tester = training_data[["Average Grade"]]

    # Categorical features of our data
    categorical_features = ["SME", "Ownership", "Jobs Created",
                            "Sector", "Condition"]

    # Create our categorical transformer
    categorical_pipeline = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value="missing")),
        ('onehot', OneHotEncoder(handle_unknown="ignore"))
    ])

    # Apply our pipeline to the given features
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", categorical_pipeline, categorical_features)
        ]
    )

    # Perform logistic regression using XGB Boosting
    regr = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor", XGBClassifier(objective="binary:logistic", seed=1))
    ])

    # Create the parameters for our search grid
    param_grid = {
        'regressor__n_estimators': [100, 300],
        'regressor__max_depth': [10, 20]
    }

    # Perform a grid search to find the best combination of features
    grid_search = GridSearchCV(
        regr, param_grid, cv=5, verbose=3, n_jobs=2, scoring="accuracy"
    )

    # Fit to our training data
    grid_search.fit(grade_trainer, grade_tester)

    # Print the best score for this grid search
    return grid_search


# Function to classify the grade data not including the zero removed values
def non_zero_grade_classifier():
    # Testing data for the zero removed data
    grade_trainer = zero_train_data.drop(columns=["Average Grade"])
    grade_tester = zero_train_data[["Average Grade"]]

    # Categorical features of our data
    categorical_features = ["SME", "Ownership", "Jobs Created",
                            "Sector", "Condition"]

    # Create our categorical transformer
    categorical_pipeline = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value="missing")),
        ('onehot', OneHotEncoder(handle_unknown="ignore"))
    ])

    # Apply our pipeline to the given features
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", categorical_pipeline, categorical_features)
        ]
    )

    # Perform logistic regression using XGB Boosting
    regr = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor", XGBClassifier(objective="binary:logistic", seed=1))
    ])

    # Create the parameters for our search grid
    param_grid = {
        'regressor__n_estimators': [50, 100],
        'regressor__max_depth': [10, 20]
    }

    # Perform a grid search to find the best combination of features
    grid_search = GridSearchCV(
        regr, param_grid, cv=5, verbose=3, n_jobs=2, scoring="accuracy"
    )

    # Fit to our training data
    grid_search.fit(grade_trainer, grade_tester)

    # Print the best score for this grid search
    return grid_search


# Function to classify the business grade of the investment
def business_plan_classifier():
    # Create our testing and training data from the overall data
    grade_trainer = training_data.drop(columns=["Business Plan Grade"])
    grade_tester = training_data[["Business Plan Grade"]]

    # Categorical features of our data
    categorical_features = ["SME", "Ownership", "Jobs Created",
                            "Sector", "Condition"]

    # Create our categorical transformer
    categorical_pipeline = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value="missing")),
        ('onehot', OneHotEncoder(handle_unknown="ignore"))
    ])

    # Apply our pipeline to the given features
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", categorical_pipeline, categorical_features)
        ]
    )

    # Perform logistic regression using XGB Boosting
    regr = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor", XGBClassifier(objective="binary:logistic", seed=1))
    ])

    # Create the parameters for our search grid
    param_grid = {
        'regressor__n_estimators': [50, 100],
        'regressor__max_depth': [10, 20]
    }

    # Perform a grid search to find the best combination of features
    grid_search = GridSearchCV(
        regr, param_grid, cv=5, n_jobs=2, scoring="accuracy"
    )

    # Fit to our training data
    grid_search.fit(grade_trainer, grade_tester)

    # Print the best score for this grid search
    return grid_search


# If main function, print out values for best scores
if __name__ == '__main__':

    # Call the average grade classifier
    avg_grade_grid = grade_classifier()

    # Call the zero removed grade classifier
    non_zero_grid = non_zero_grade_classifier()

    # Call the business plan grade classifier
    business_grade_grid = business_plan_classifier()

    # Output the scores for each and print the best features
    print("\n\nAverage Grade Grid Search\nBest Score: {}"
          .format(avg_grade_grid.best_score_))

    print("\n\nNon-Zero Grade Grid Search\nBest Score: {}"
          .format(non_zero_grid.best_score_))

    print("\n\nBusiness Grade Grid Search\nBest Score: {}"
          .format(business_grade_grid.best_score_))
