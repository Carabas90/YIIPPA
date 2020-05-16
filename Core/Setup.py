import os

def setup():
    """
    Checks if Data-Folders exist, creates them if not.
    """
    if not os.path.exists(os.path.join(os.curdir, 'PatientData/')):
        os.mkdir('PatientData')
    if not os.path.exists(os.path.join(os.curdir, 'Archive/')):
        os.mkdir('Archive')

if __name__ == '__main__':
    setup()