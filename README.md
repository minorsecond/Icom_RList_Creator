# Repeater List Creator for ICOM ID-50 and ID-52

This repository contains the `RListCreator.py` script, which helps you create a repeater list CSV file that can be loaded into your ICOM ID-50 or ID-52 radio.

## Steps to Create and Load the Repeater List

### 1. Download Repeater CSV Files
1. Go to [RepeaterBook](https://www.repeaterbook.com/).
2. Download the CSV files for the repeaters you want to load into your radio.

### 2. Prepare the CSV Directory
1. Create a directory on your computer.
2. Place each downloaded CSV file that you want to load into your radio into this directory.

### 3. Run the Script
1. Make sure you have Python installed on your computer.
2. Download the `RListCreator.py` script from this repository.
3. Open a terminal or command prompt.
4. Navigate to the directory where you saved the `RListCreator.py` script.
5. Run the script by entering the following command:
   ```sh
   python RListCreator.py
   ```
6. Follow the prompts:

    Enter the path to the directory containing the CSV files.
    Enter the group number, group name, and UTC offset for each file.
    Select whether to use the Location or Output Freq column for the Name field.

### 4. Copy the New CSV to the Radio

1. Insert your radio's microSD card into your computer.
2. Navigate to the <radio model>/Csv/RptList directory on the microSD card.
3. Copy the new CSV file created by the script into this directory.

### 5. 
Import the Repeater List on the Radio

1. Insert the microSD card back into the radio.
2. Turn on the radio.
3. Press the menu button.
4. Go to SET.
5. Scroll to the bottom and select SD Card.
6. Select Import/Export. 
7. Select Import. 
8. Select Repeater List. 
9. Choose the new CSV file. 
10. Follow the prompts to import the repeater list. 
11. Restart the radio.

The new data should now be loaded into the Near Repeater list.

### Tested Devices

* ICOM ID-50

The script should also work with:

* ICOM ID-52 (not yet tested)

### License

This project is licensed under the MIT License