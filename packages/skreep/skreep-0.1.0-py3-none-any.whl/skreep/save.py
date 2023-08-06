import csv

class Save:
    def __init__(self, name='data', ext='csv'):
        file = open(name+'.'+ext, mode='w', newline='')
        self.w = csv.writer(file)
    
    def save(self, *args):
        data = list(args)
        self.w.writerow(data)