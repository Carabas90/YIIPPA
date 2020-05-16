import csv
import datetime
import random
import os
import shutil


def create_new(first_name, last_name, birthdate):
    """
    Creates a new CSV-File with the standard header and adds an entry in legend.csv. The filename 
    is based on datetime.now() with a random int thrown in as a last digit, to avoid collisions if
    application is ever used in a large scale setting.
    """
    filename = datetime.datetime.now().strftime(format='%Y%m%d%H%M%S')+str(random.randint(0,9))+'.csv'
    p = os.path.join(os.curdir , 'PatientData/', filename)
    with open(p, 'w', newline='\n') as f:
        writer = csv.writer(f)
        header = ['date','time', 'insulin_rate', 'blood_glucose' ]
        writer.writerow(header)
    
    p = os.path.join(os.curdir, 'PatientData/', 'legend.csv')
    
    if os.path.exists(p):
        with open(p, 'a', newline='\n') as l:
            writer = csv.writer(l)
            data = [first_name, last_name, birthdate, filename]
            writer.writerow(data)
    else:
        with open(p, 'w', newline='\n') as l:
            writer = csv.writer(l)
            header = ['first_name', 'last_name', 'birthdate', 'filename']
            writer.writerow(header)
            data = [first_name, last_name, birthdate, filename]
            writer.writerow(data) 
    

def import_data(filename):
    """
    Imports the Data of a csv file as a nested list, including the header.
    """
    path = os.path.join(os.curdir, 'PatientData/', filename)
    with open(path, 'r', newline='\n') as f:
        reader = csv.reader(f, delimiter=',')
        data = []
        for r in reader:
            data.append(r)
        return data


def archive_patient(first_name, last_name, birthdate):
    """
    Moves the CSV-File corresponding to the Patient into the Archive Folder and deletes
    the Entry in the legend.csv .
    """
    legend = import_data('legend.csv')
    for s in legend:
        if s[0]==first_name and s[1]==last_name and s[2]==birthdate:
            filename = s[3]
            i = legend.index(s)
    
    src = os.path.join(os.curdir, 'PatientData/', filename)
    dest = os.path.join(os.curdir, 'Archive/', filename)
    shutil.move(src, dest)
    
    del legend[i]
    path = os.path.join(os.curdir, 'PatientData/', 'legend.csv')
    with open(path, 'w', newline='\n') as l:
        writer = csv.writer(l)
        for p in legend:
            writer.writerow(p)

def write_line(filename, data_list):
    """
    Writes one line of Data to the corresponding Patients File.
    """
    path = os.path.join(os.curdir, 'PatientData/', filename)
    with open(path, 'a', newline='\n') as f:
        writer = csv.writer(f)
        writer.writerow(data_list)


if __name__ == '__main__':
    print(import_data('legend.csv'))
    
