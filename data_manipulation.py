# File that will retrieve information from the API if there are none found
import requests
import os
import csv

invest_ni_api = "https://www.opendatani.gov.uk/api/3/action/datastore_search?" \
                "resource_id=cd00d300-fcde-4ad8-921e-f1324b75d37e&limit=10000"


# Function to check for the csv is present
def check_file(file_name):
    # Check the data file path
    file_path = file_name

    # Return true or false based on file path
    if os.path.isfile(file_path):
        return True
    else:
        return False


# Function to create the file
def invest_data_retrieve(file_name, overwrite=False):
    # Check if the file name exists already
    if check_file(file_name):
        # If we want to overwrite, then delete the file
        if overwrite:
            print("Overwriting file - deleting original")
            os.remove(file_name)
        # Otherwise, we want to print an error and return
        else:
            # Print out that the file exists
            print("File exists already")
            return None

    # If not exited, continue on
    # Use requests to retrieve the list of data entries
    api_request = requests.get(invest_ni_api)
    output = api_request.json()

    print(api_request)

    # Open our csv writer
    with open(file_name, "w", newline="", encoding="utf-8") as csvfile:
        # Create headings and the writer object
        headers = ["Client Name", "Total Assistance",
                   "Total Investment", "Investment Gain",
                   "Condition", "Estimated Jobs",
                   "Country", "SME", "Ownership", "Status",
                   "Constituency", "Sector"]
        data_writer = csv.DictWriter(csvfile, fieldnames=headers)

        # Write the header
        data_writer.writeheader()
        # Go through each row in the output and write to csv
        for data_row in output['result']["records"]:

            # Calculate the investment gain (investment - assistance)
            gain = float(data_row["Total Investment (Includes Invest NI " \
                                  "Assistance) £"]) - float(data_row["Total " \
                                                                     "Assistance " \
                                                                     "Offered by " \
                                                                     "Invest NI (£)"])

            # Write this row to the csv
            data_writer.writerow({"Client Name": data_row["Client Name"],
                                  "Total Assistance": data_row[
                                      "Total Assistance "
                                      "Offered by "
                                      "Invest NI (£)"],
                                  "Total Investment": data_row[
                                      "Total Investment (Includes "
                                      "Invest NI Assistance) £"],
                                  "Investment Gain": gain,
                                  "Condition": data_row[
                                      "Conditions of Offer"],

                                  "Estimated Jobs": data_row["Jobs "
                                                             "to be "
                                                             "Created "
                                                             "(Assisted)"],
                                  "Country": data_row[
                                      "Country of Ownership "
                                      "when the offer "
                                      "was made"], "SME": data_row["SME"],
                                  "Ownership": data_row[
                                      "Ownership when the "
                                      "offer was made"],
                                  "Status": data_row["Project Status"],
                                  "Constituency": data_row["Constituency "
                                                           "in which "
                                                           "business was "
                                                           "located when "
                                                           "offer "
                                                           "was made"],
                                  "Sector": data_row["SIC Sector"]})


# Function for appending data
def append_data(data_list, file_path, overwrite=False):
    # Check if the file name exists already
    if check_file(file_path):
        # If we want to overwrite, then delete the file
        if overwrite:
            print("Overwriting file - deleting original")
            os.remove(file_path)
        # Otherwise, we want to print an error and return
        else:
            # Print out that the file exists
            print("File exists already")
            return None

    # Go through the data list and write to the csv
    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        # Create headings and the writer object
        headers = ["Client Name", "Total Assistance",
                   "Total Investment", "Investment Gain", "Investment Grade",
                   "Condition", "Estimated Jobs",
                   "Country", "SME", "Ownership", "Status",
                   "Constituency", "Sector", "Business Plan Grade",
                   "Average Grade", "Jobs Created"]
        data_writer = csv.DictWriter(csvfile, fieldnames=headers)

        # Write the header for our file
        data_writer.writeheader()

        # Go through each entry in the datalist and write to the csv
        for data_row in data_list:
            # write row
            data_writer.writerow({"Client Name": data_row["Client Name"],
                                  "Total Assistance":
                                      data_row["Total Assistance"],
                                  "Total Investment": data_row[
                                      "Total Investment"],
                                  "Investment Gain":
                                      data_row["Investment Gain"],
                                  "Investment Grade":
                                      data_row["Investment Grade"],
                                  "Condition": data_row["Condition"],

                                  "Estimated Jobs": data_row["Estimated Jobs"],
                                  "Country": data_row["Country"],
                                  "SME": data_row["SME"],
                                  "Ownership": data_row["Ownership"],
                                  "Status": data_row["Status"],
                                  "Constituency": data_row["Constituency"],
                                  "Sector": data_row["Sector"],
                                  "Jobs Created": data_row["Jobs Created"],
                                  "Average Grade":
                                      data_row["Average Grade"],
                                  "Business Plan Grade":
                                      data_row["Business Value"]})


# Run the retrieval for the Invest NI data if this is the main file
if __name__ == '__main__':
    invest_data_retrieve("Data/invest_ni.csv", True)

