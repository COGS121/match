import csv
from collections import OrderedDict

def get_pids(file_obj):
    reader = csv.DictReader(file_obj, delimiter=',')
    pids = OrderedDict()
    for line in reader:
        pid = line["PID"]
        print pid
        if (pid != ''):
            pids[pid] = "-1"
    return pids

# takes a dict of pids and maps the corresponding grades to each one
def assign_grades(file_obj, pids):
    reader = csv.DictReader(file_obj, delimiter=',')
    for line in reader:
        pid1 = line["PID1"]
        pid2 = line["PID2"]

        if (pid1 in pids):
            pids[pid1] = line
            if (pid2 != '' and pid2 in pids):
                pids[pid2] = line
        else:
            print "error. pid not found! ", pid1

    return pids

if __name__ == "__main__":
    with open("files/roster.csv") as f_obj:
        pids = get_pids(f_obj)

    with open("files/a2grades.csv") as f_obj:
        hwgrades = assign_grades(f_obj, pids)
