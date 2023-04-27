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
    
    if (len(sys.argv) == 4):
        if is_integer(sys.argv[3]):
            limit = min(int (sys.argv[3]), num_patients)
        else: 
            raise Exception('If third argument is provided, it must be an integer, e.g., python export_data.py datain data_out 50.')
    
    for i in range(limit):
        patient_id = patient_ids[i]
        patient_metadata, recording_metadata, recording_data = load_challenge_data(data_folder, patient_id)
        patient_features, quality_score, recordings = get_features(patient_metadata, recording_metadata, recording_data, stacked=False, encode_sex=False)

        if not os.path.exists(export_folder):
            os.makedirs(export_folder)

        subdir = os.path.join(export_folder, 'ICARE_'+patient_id)
        if not os.path.exists(subdir):
            os.makedirs(subdir)

        file = os.path.join(subdir, 'patient_'+patient_id+'.csv')
        with open(file, mode='w', newline='') as f:
            writer = csv.writer(f)
            patient_features.append(quality_score)
            writer.writerow(patient_features)

        f.close()
                            
        file = os.path.join(subdir, 'recordings_'+patient_id+'.csv')
        with open(file, mode='w', newline='') as f:
            np.savetxt(f, recordings, delimiter=',', fmt='%.16f')


        f.close()


  