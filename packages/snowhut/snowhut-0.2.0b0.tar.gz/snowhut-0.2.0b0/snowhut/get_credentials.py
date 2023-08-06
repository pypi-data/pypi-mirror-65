

def read_credentials(cred_source, from_file=True):
    ''' Fetch user credentials from text file.

    Converts string input in path to dictionary. Credentials must
    be stored as a dictionary to work properly.

    '''
    if from_file:
        creds = {}
        with open(cred_source) as f:
            lines = f.readlines()
            for line in lines:
                line = line.split()
                creds[line[0]] = line[1]
    else:
        creds = cred_source
    return creds