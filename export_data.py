"""
This file provides functionality to export data from the PhysioNet 2023 challenge to *.csv files.

All of the features extracted from the team_code.py/get_features function are exported to *.csv files.
Run:
python3 export_data.py data_in data_out n
where:
    - data_in is the path to the folders containing the original training data provided by the PhysioNet 2023 challenge, i.e. data/training,
    - data_out is the path where the exported files are written,
    - n (optional) is the number of patients for which the data is exported. If not provided, the entire data is exported.

After execution, the data_out folder contains a directory structure similar to the one provided by the PhysioNet 2023 challenge where each subfolder contains data of a single patient. The patient id is implicit in the file and folder name, i.e. ICARE_0284 is the folder for patient 0284. Within each folder, two *.csv files are produced:
    - one, e.g. patient_ICARE_0284.csv, contains the patient data and the quality score
    - the other, e.g. recordings_ICARE_0284.csv, contains the recordings as time series data, i.e. each row contains data of a specific time stamp.

Martin Boehm
May 2, 2023

"""

import sys
from helper_code import find_data_folders, is_integer, load_challenge_data
from team_code import get_features
import csv
import os
import numpy as np

if __name__ == '__main__':
    # Parse the arguments.
    if not (len(sys.argv) == 3 or len(sys.argv) == 4):
        raise Exception('Include the data folders for import and export as argument, e.g., python export_data.py data_in data_out.')


    # Define the data and limit
    data_folder = sys.argv[1]
    export_folder = sys.argv[2]
    patient_ids = find_data_folders(data_folder)
    num_patients = len(patient_ids)
   

    if num_patients==0:
        raise FileNotFoundError('No data was provided.')
    
    limit = num_patients
    
    if (len(sys.argv) == 4):
        if is_integer(sys.argv[3]):
            limit = min(int (sys.argv[3]), num_patients)
        else: 
            raise Exception('If third argument is provided, it must be an integer, e.g., python export_data.py data_in data_out 50.')
    print(limit)
    for i in range(limit):
        patient_id = patient_ids[i]
        patient_metadata, recording_metadata, recording_data = load_challenge_data(data_folder, patient_id)
        patient_features, recordings_sum, recordings_raw = get_features(patient_metadata, recording_metadata, recording_data, stacked=False, encode_sex=False)


        if not os.path.exists(export_folder):
            os.makedirs(export_folder)

        subdir = os.path.join(export_folder, patient_id)
        if not os.path.exists(subdir):
            os.makedirs(subdir)

        file = os.path.join(subdir, 'patient_'+patient_id+'.csv')
        with open(file, mode='w', newline='') as f:
            writer = csv.writer(f)

            writer.writerow(patient_features)
        f.close()
                            
        file = os.path.join(subdir, 'recordings_summary_'+patient_id+'.csv')
        with open(file, mode='w', newline='') as f:
            header = "signal mean, signal std, delta psd mean, theta psd mean, alpha psd mean, beta psd mean"
            np.savetxt(f, recordings_sum, delimiter=',', header=header, fmt='%.16f', comments='')
        f.close()

        headers = ("alpha_psd", "beta_psd", "delta_psd", "theta_psd");

        for j in range(0,4):
            file = os.path.join(subdir, headers[j]+' '+patient_id+'.csv')
            with open(file, mode='w', newline='') as f:
                np.savetxt(f, recordings_raw[j], delimiter=',', fmt='%.16f', comments='')
            f.close()


  