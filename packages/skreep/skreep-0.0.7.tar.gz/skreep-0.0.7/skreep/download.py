import urllib.request
import os

def dl(url, set='default'):

    if 'default' == set:
        file_name = os.path.basename(url)
        urllib.request.urlretrieve(url, file_name)
    
    if 'list' == set:
        for dl in url:
            file_name = os.path.basename(dl)
            urllib.request.urlretrieve(dl, file_name)