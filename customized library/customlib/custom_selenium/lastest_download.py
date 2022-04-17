import os

def latest_download_file(path):
    """
    function to wait for pending downloads to finish
    :param path: str 
            the directory to check for the lastest download file
    :return: str
            the string of the lastest downloaded file name
    """
    os.chdir(path)
    files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
    newest = files[-1]

    return newest