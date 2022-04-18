"""
This file is used to test the models created by testing them against the
hold out data for our data analysis
"""
# Imports
import pandas as pd
import numpy as np
import classifiers

# File paths
data_path = "Data/appended_data.csv"
zero_removed_path = "Data/zero_removed_data.csv"
avg_grade_test_path = "Data/testing/avg_grade_test.csv"
zero_removed_test_path = "Data/testing/zero_removed_data_test.csv"
business_grade_test_path = "Data/testing/business_grade_test.csv"

# Read in our data
overall_data = pd.read_csv(data_path, engine="python")
zero_removed_data = pd.read_csv(zero_removed_path, engine="python")

# Create the testing sets
overall_testing = overall_data[6500:]
zero_removed_testing = zero_removed_data[6000:]

np.random.seed(0)


# Function to drop the given column for testing
def drop_column(col, testing_set):
    # If average grade given, drop it
    if col == "Average Grade":
        new_set = testing_set.drop(columns=["Average Grade"])
    # Otherwise, business plan grade
    else:
        new_set = testing_set.drop(columns=["Business Plan Grade"])
    # Return the new set
    return new_set


# Function to run our tests
if __name__ == '__main__':
    # Get our grid searches from classifier
    avg_grade_grid = classifiers.grade_classifier()
    zero_removed_grid = classifiers.non_zero_grade_classifier()
    business_grade_grid = classifiers.business_plan_classifier()

    # Drop some of our columns for our tests
    avg_grade_test = drop_column("Average Grade", overall_testing)
    zero_removed_grade_test = drop_column("Average Grade",
                                          zero_removed_testing)
    business_grade_test = drop_column("Business Plan Grade", overall_testing)

    # Run predictions for our data
    avg_grade_pred = avg_grade_grid.predict(avg_grade_test)
    zero_removed_pred = zero_removed_grid.predict(zero_removed_grade_test)
    business_grade_pred = business_grade_grid.predict(business_grade_test)

    # Output the files to testing folder
    pd.DataFrame({'Average Grade': avg_grade_pred}).to_csv(avg_grade_test_path)
    pd.DataFrame({'Average Grade': zero_removed_pred}).\
        to_csv(zero_removed_test_path)
    pd.DataFrame({'Business Plan Grade': business_grade_pred})\
        .to_csv(business_grade_test_path)
