"""
This file is used to test the models created by testing them against the
hold out data for our data analysis
"""
# Imports
import pandas as pd
import numpy as np
import classifiers
import csv

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


# Function to compare two csv files
def compare_csv(control_path, test_path, starting_row, comp_value):
    # Create a control list to test against
    control_list = []
    test_list = []
    # Iterate through and add values to the control list
    with open(control_path, newline='') as control:
        reader = csv.reader(control, delimiter=',')
        # Skip the header
        next(reader, None)

        # We want to skip a number of rows equal to our starting row value
        skip_row = 0
        for row in reader:
            # If less than starting row, skip
            if skip_row < starting_row:
                skip_row += 1
                continue
            # Otherwise, begin adding to the control list - check which value
            # we are comparing
            if comp_value == "Mean Average":
                if row[14] == "True":
                    translate_val = "1"
                else:
                    translate_val = "0"
            else:
                if row[13] == "True":
                    translate_val = "1"
                else:
                    translate_val = "0"
            # Append to the control list
            control_list.append(translate_val)
        # Close the connection
        control.close()

    # Now load in our comparison csv
    with open(test_path, newline='') as test_file:
        reader = csv.reader(test_file, delimiter=',')

        # Skip the header
        next(reader, None)

        # Iterate through the rest of the list
        for row in reader:
            # Append the second value to the list
            test_list.append(row[1])

        # Close connection
        test_file.close()

    # Value to track our successes
    success = 0

    # Iterate through and compare the values
    for comp_value in range(len(test_list)):
        # Compare the two and see if they match
        if test_list[comp_value] == control_list[comp_value]:
            # Iterate the success counter
            success += 1

    # Calculate success rate
    success_rate = success / len(test_list)

    # Return the success rate
    return success_rate


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

    # Compare our CSVs and return the score
    print("Testing Mean Average Grades:")
    avg_grade_results = compare_csv(data_path, avg_grade_test_path,
                                    6500, "Mean Average")
    print("Success Rate: " + str(avg_grade_results))

    print("\n\nTesting Zero Removed Mean Average Grades:")
    zero_removed_results = compare_csv(zero_removed_path,
                                       zero_removed_test_path,
                                       6000, "Mean Average")
    print("Success Rate: " + str(zero_removed_results))

    print("\n\nTesting Business Grades:")
    business_grade_results = compare_csv(data_path, business_grade_test_path,
                                         6500, "Business Grade")
    print("Success Rate: " + str(business_grade_results))

