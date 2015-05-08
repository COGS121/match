"""
Convert the grades of submitted assignment to excel.
"""
import csv, re

#global variables
RECORDS = {}
TITLE = ""

def isPID(pid):
    """
    Checks if PID is valid
    """
    return bool(re.match(r'[AUau][0-9]{8}', pid))

def getRecord(filename):
    """
    Grabs PID, total score, and comment.
    Temporarily saves to RECORDS dictionary.
    """

    print "Retrieving grades from \"" + filename + "\""
    sheet = open(filename, "r")
    grades = csv.DictReader(sheet, delimiter='\t')
    for grade in grades:
        content = {"Score": grade["Total"], "Comment": grade["Comments"]}

        # grabs PID of first partner and validate PID
        pid = grade["PID1"].strip()
        if pid and isPID(pid):
            RECORDS[pid] = content

        # grabs PID of second partner and validate PID
        pid = grade["PID2"].strip()
        if pid and isPID(pid):
            RECORDS[pid] = content

    sheet.close() # close file
    print "Retrieval success!"

def setGrade(filename):
    """
    Parse through roster, then add the values from RECORDS as tmp.
    Write tmp to resulted value.
    """

    print "Writing grades to \"" + filename + "\""
    roster = open(filename, "rU")
    header = True
    tmp = ""
    for line in roster:
        line = line.strip() # remove all trailing whitespaces

        # write appropriate header
        if header:
            tmp += line + "\t"+TITLE+" Score\t"+TITLE+" Comment\n"
            header = False
            continue

        data = line.split("\t")  # grab specific part of current line

        # if PID doesn't exist in submitted form do not write score or comment
        if data[0] not in RECORDS:
            if isPID(data[0]):
                print "NOT SUBMITTED:",data[0]
                tmp += line + "\n"
            continue

        # concatenate score and comment of this student
        current = RECORDS[data[0]]
        tmp += line + "\t" + current["Score"] + "\t" + current["Comment"] + "\n"
    roster.close()

    # write concatenated string to target file. Override previous
    roster = open("files/result.tsv", "w")
    roster.write(tmp)
    roster.close()
    print "All Grades have been written"

if __name__ == "__main__":
    TITLE = raw_input("Type your Assignment Title: ").strip()
    getRecord("files/a2grades.tsv")
    setGrade("files/roster.tsv")
