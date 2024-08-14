"""This module predicts the next 3 values of a stock price based on a value of 10 consecutive data points chosen at random.
By default, it can operate on 2 files at the same time in the same directory and will produce predicted data points.

The number of files processed, consecutive data points chosen at random and even the number data points generated 
can be specified under the variables section in main below."""

import csv
import random
import datetime
import os
import sys

def select_data(file_path, num_points):
    """Reads data and performs some validation on it"""
    data = []
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            """Check if format of the data is under the expected dd-MM-YYYY,
            assuming there are no headers in the file."""
            try:
                datetime.datetime.strptime(row[1], "%d-%m-%Y")
            except ValueError:
                print(error_log_1, row[2])
                exit()
            """Check if third column contains anything which can't be cast as a float"""
            try:
                float(row[2])
            except ValueError:
                print(error_log_2, row)
                exit()
            data.append(row)

    """Check if available range is length of data set minus the required number of points""" 
    if (len(data) >= num_points):
        start_index = random.randint(0, len(data) - num_points)
        return data[start_index:start_index + num_points]
    else:
        print(error_log_3)
        exit()

def predict_data_LSEG(data, data_points_number):
    """Implementation of default LSEG algotithm proposed in the exercise"""
    prices = []
    for row in data:
        price = float(row[2])
        prices.append(price)
        
    def recursive_predict(prices, n, result):
     """The first two values are appended to the list according to the list of prices.
     Afterwards, we append further elements according to the previous 2 values of the list."""
     if n == 1:
        result.append(sorted(prices)[-2])
     elif n == 2:
        result.append(sorted(prices)[-2] + (prices[-1] - sorted(prices)[-2]) / 2)
     else:
        prev = result[-1]
        ante_prev = result[-2]
        next_value = prev + (prev - ante_prev) / 2**(n-1)
        result.append(next_value)

    def predict_data_recursive(prices, num_predictions):
        """We create the function which will populate our predicted prices with the function above.
        It is assumed num_prediction >= 3, otherwise change code below.
        """
        result=[]
        recursive_predict(prices, 1, result)
        recursive_predict(prices, 2, result)
        for i in range(3, num_predictions + 1):
            recursive_predict(prices, i, result)
        return result
    
    """One-liner which may work to avoid calling predict_data_recursive with some changes but not recommended"""
    # predicted_prices = [recursive_predict(prices, i, []) for i in range(1, num_predictions + 1)]

    predicted_prices= predict_data_recursive(prices,data_points_number)

    """Using datetime to avoid erroneous incrementation over the date (e.g. 32-01-2023)
    We process the date using the last data point, expecting it to be on the 2nd column."""

    last_date_str = data[-1][1]
    last_date = datetime.datetime.strptime(last_date_str, "%d-%m-%Y")
    stock_id = data[-1][0]  

    """Having the stock ID, date and predicted price, we construct the predicted data"""
    predicted_data = []
    for index, price in enumerate(predicted_prices):
        predicted_date = last_date + datetime.timedelta(days=index+1)
        predicted_date_str = predicted_date.strftime("%d-%m-%Y")
        predicted_data.append([stock_id, predicted_date_str, price])
    return predicted_data

if __name__ == "__main__":

    """VARIABLES"""
    num_files_to_sample = 2
    num_points = 10
    data_points_number = 3

    """ERROR LOG TEXT"""

    error_log_1 = "ERROR: Incorrect date & time format in the second column. Expected dd-mm-yyyy.\
                   \nPlease remove any headers in the file if present. Issue occurred at price: "
    error_log_2 = "ERROR: Third row does not contain a number or it is missing.\
                   \nPlease check:"
    error_log_3 = "ERROR: Available data set does not exceed number of requested consecutive data points."
    error_log_4 = "ERROR: No files found in the directory."
    error_log_5 = "ERROR: No CSV files found in the directory."
    error_log_6 = "WARNING: Skipping non-CSV object."
    error_log_7 = "ERROR: Please run the python script with the following format\
                    \npython3 task.py <FILE/INPUT DIRECTORY PATH> <OUTPUT DIRECTORY PATH>"

    """MAIN"""
    if len(sys.argv) != 3:
        print(error_log_7)
        sys.exit(1)

    exchange_dir = sys.argv[1]
    exchange_dir_output = sys.argv[2]

    files = os.listdir(exchange_dir)
    print ("Files detected:", files)

    if not files:
        print(error_log_4)
        exit()

    csv_files = [file for file in files if file.endswith('.csv')]
    if not csv_files:
            print(error_log_5)
            exit()

    """Per requirement, if fewer files than what is hardcoded exists then we set the # of files accordingly"""
    if len(files) < num_files_to_sample:
        num_files = len(files)

    """If there are more than 2 files in the folder, we slice the files to only include the first num_files_to_sample files"""
    for file in files[:num_files_to_sample]:
        """If file is not .csv, it is skipped."""
        if not file.endswith('.csv'):
            print(error_log_6)
            continue
        file_path = os.path.join(exchange_dir, file)
        print ("Processing file with name:", file)
        data = select_data(file_path, num_points)
        predicted_prices = predict_data_LSEG(data, data_points_number)

    """Writing output to new CSV file in a different folder to avoid errors on reruns, with the same format (i.e. no header)"""
    output_file = f"{file}_predicted.csv"
    output_path = os.path.join(exchange_dir_output, output_file)
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(predicted_prices)