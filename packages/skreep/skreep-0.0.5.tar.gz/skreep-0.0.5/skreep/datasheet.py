import csv

def sheet(dt):
    o = open(dt, "rb")
    r = o.readlines()
    return [i.decode("utf-8").strip() for i in r]