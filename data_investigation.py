# This file aims to investigate some elements of the data
# The methods can be called to get the results, or if ran as main will
# output the results in a terminal
import csv
import data_manipulation as dm

# File paths
invest_path = "Data/invest_ni.csv"  # Invest NI data path
append_path = "Data/appended_data.csv"  # Invest NI data with added columns
zero_removed_path = "Data/zero_removed_data.csv"    # Remove 0 gain entries

# Data lists to hold our information
invest_list = []
gain_list = []
append_list = []


# Function to get the values from a csv and put into a list
def data_retrieve(data_list, data_source):
    # Open our connection to the given source
    with open(data_source, newline='') as csvfile:
        # Create a data reader object
        data_reader = csv.DictReader(csvfile)
        # For each row, append to our data list
        for row in data_reader:
            data_list.append(row)


# Function to calculate the average investment gain
def average_gain(data_list):

    # Check if this has an investment gain column, otherwise print err + return
    if "Investment Gain" not in data_list[0]:
        print("No Investment Gain column found - exiting function")
        return 0

    # Value to hold the total
    total_grade = 0

    # Iterate through the list
    for entry in data_list:
        # Calculate the grade for this entry using 1 - (Total Assistance/Total
        # Investment) so that the values are normalised
        # If either are 0, then just grade score to 0
        if entry["Total Assistance"] == "0" or entry["Total Investment"] == "0":
            # Set grade score to 0
            grade_score = 0
        # Otherwise calculate the grade score
        else:
            grade_score = 1 - (float(entry["Total Assistance"]) /
                               float(entry["Total Investment"]))

        # Add the investment gain value to the total gain
        total_grade += grade_score
        # If the gain is 0, add to the zero gain list
        if float(entry["Investment Gain"]) == 0:
            entry["Investment Grade"] = 0
        else:
            gain_list.append(entry)
            entry["Investment Grade"] = grade_score

    # Get average and average without 0 values
    average_grade = total_grade / len(data_list)
    zero_removed_average_grade = total_grade / len(gain_list)
    return [average_grade, zero_removed_average_grade]


# Function to add the marker for job creation feature
def job_creation_marker(data_list):
    # Iterate through the data list
    for entry in data_list:
        job_value = "False"
        # If the value for jobs to be created is 0, then set this as 0
        if not entry["Estimated Jobs"] == "0":
            # Mark this as having a job value
            job_value = "True"
        # Update this entry
        entry["Jobs Created"] = job_value


# Function to add the marker for the below average investment return
def average_mean_watermark(data_list, average):
    # Iterate through the list and see which investment gains fall below
    for entry in data_list:
        pass_value = "False"
        # Check if the value falls below the average mean
        if float(entry["Investment Grade"]) > average:
            # Set pass value as 1
            pass_value = "True"
        # Update this entry
        entry["Average Grade"] = pass_value


# Function to add the marker for the below business estimations
# (Taken from 5 year strategy bullet points - £1 in, £6 return)
def business_estimation_watermark(data_list):
    # Iterate through the list and see which investments are below
    for entry in data_list:
        business_value = "False"
        # Check this entry's investment
        if float(entry["Total Assistance"]) * 6 < \
                float(entry["Total Investment"]):
            # This is above the advertised value from 5 year business plan
            business_value = "True"
        # Update this entry
        entry["Business Value"] = business_value


# Run as main method
if __name__ == '__main__':

    # Check that the file exists
    if not dm.check_file(invest_path):
        # Create the file
        dm.invest_data_retrieve(invest_path)

    # If investment list is empty, run function get the values from csv
    if len(invest_list) == 0:
        # Run the data retrieval
        data_retrieve(invest_list, invest_path)

    # Get average gain on investment
    avg_gain, non_zero_avg = average_gain(invest_list)
    # Print out the average
    print("Grades are a ratio of 1 - (Total Assistance / Total Investment)")
    print("Average Investment Grade Across "
          "" + str(len(invest_list)) + " investments: " + str(avg_gain))
    print("\nAverage Investment Grade not including Zero-Gainers Across " +
          str(len(gain_list)) + " investments: "
                                                        "" + str(non_zero_avg))
    print("\n\n\n")

    # Copy the data list into the append list and run it through the functions
    append_list = invest_list.copy()
    job_creation_marker(append_list)
    average_mean_watermark(append_list, avg_gain)
    business_estimation_watermark(append_list)

    # Write this to a new csv
    dm.append_data(append_list, append_path, True)
    
    # Repeat for our gain list 
    job_creation_marker(gain_list)
    average_mean_watermark(gain_list, non_zero_avg)
    business_estimation_watermark(gain_list)
    
    # Write to new csv 
    dm.append_data(gain_list, zero_removed_path, True)
