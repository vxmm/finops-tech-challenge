# lseg-tech-challenge
Pre-interview coding challenge for LSEG 

## About
LSEG pre-interview coding challenge is a novel implementation of a prediction algorithm which is aims to determine the price of a particular stock based on subset of data chosen at random in a .csv file. 

## Important 

The algorithm proposed contains a part which could result in very extreme deviations if interpreted literary:

![image](https://github.com/user-attachments/assets/977e961c-3aca-452c-baca-f87994d3e86b)

If, for example, we are looking at two consecutive values e.g. 104 and 105 then the predicted value would be equal to half the difference between the two at -0.5 which can appear to be misleading. 

**Therefore**, I've chosen to interpret the following requirement in a non-literal sense, which results in a more robust and realistic prediction overall:

• n+2 data point ~~has~~ accumulates half the difference between n and n+1

• n+3 data point ~~has~~ accumulates 1/4th the difference between n+1 and n+2

## Optimisation

• supports more than 2 files to be processed was added by modifying the ```num_files_to_sample``` variable (default=2).

• supports choosing any number of consecutive data points chosen at random by modifying the ```num_points variable``` (default=10).

• recursive implementation of the prediction algorithm allows for increasing the number of prediction data points being made by modifying the ```data_points_number``` variable (default=3).


## Validations

The program performs validation on two disctinct levels: 

### Object level validation

We perform object level validation during __main__ for the following: 

1. Enssuring files are present in the respective folder, exit if not. 
2. If files are present, we check if there are any files ending in .csv
3. If the number of files in the folder is less than what is specified in ```num_files_to_sample``` (default = 2), we process a total number of files less than our specified value.
4. If the number of files in the folder is greater than what is specified in ```num_files_to_sample``` (default = 2), we process only the first number of files which match our specified value.
5. If the file being processed does not end with .csv, the program continues with the other files and sends a warning in the terminal. The name of the skipped file is not shown to avoid exposing folder contents.

### File level validation

We perform file level validation during **select_data** for the following:

1. Date format is present in the second column of each row under the format dd-mm-yyyy.
2. Ensure that the price of the stock is of ``float`` type.
3. Verify that the available range in the data is greater or equal than the required number of points to be utilized in the prediction.

We recommend saving the file with UTF-8 encoding. Any non-UTF-8 encoding will output the first error available in the program.

## How to Run

1. Download the project: git clone
2. Open task.py in a text editor and change the following path accordingly:
```
    exchange_dir = "FILE/INPUT DIRECTORY"
    exchange_dir_output = "OUTPUT DIRECTORY"
```


## Troubleshooting
1. Ensure Python is [configured](https://www.python.org/downloads/) to run: ```python3 --version```
2. Allow execution role for the script: ```chmod +x task.py```
3. Ensure script and user is allowed to read from the source files and output to the desired location, see [chown](https://linuxcommand.org/lc3_man_pages/chown1.html). 
4. Verify that the file is in UTF-8 encoding.
5. If possible, please ensure that the output directory is not in the same root directory of the files. 

## Further imporvements 

• Implementation of other prediction algorithms.

• Load standard error messages and variables as separate files to improve readability. 

• Allow user to input path in the terminal.

• Support for non-UTF8 encoding.
