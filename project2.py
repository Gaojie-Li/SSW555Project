import os
from collections import defaultdict

file_path = "./My-Family-29-Jan-2018-882.ged"
left_symbol = "<-- "
right_symbol = "--> "
tag_level = {"INDI": "0", "NAME": "1", "SEX": "1", "BIRT": "1", "DEAT": "1", "FAMC": "1", "FAMS": "1", "FAM": "0",
             "MARR": "1", "HUSB": "1", "WIFE": "1", "CHIL": "1", "DIV": "1", "DATE": "2", "HEAD": "0", "TRLR": "0", "NOTE": "0"}
months = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN",
          "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")


def gedcom_check(path):
    try:
        fp = open(path, 'r')
    except FileNotFoundError:
        print("File not found")
    else:
        for line in fp:
            line = line.strip()
            print(right_symbol + line)
            valid = "Y"
            line_list = line.split()
            tag = get_tag(line_list)
            if(check_tag_level(line_list)):
                valid = "Y"
                if tag == "Name":
                    lastName = line_list[len(line_list) - 1]
                    if not lastName.startswith("/") and not lastName.endswith("/"):
                        valid = "N"

                if tag == "DATE":
                    day = int(line_list[2])
                    month = line_list[3]
                    year = line_list[4]
                    if day < 1 and day > 31 and month not in months and len(year) != 4:
                        valid = "N"
            else:
                valid = "N"
            line_list.insert(2, valid)
            if tag == "INDI" or tag == "FAM":
                line_list[1], line_list[3] = line_list[3], line_list[1]
            my_print(line_list)
            line_list = []


def my_print(l_list):
    validated = ""
    index = 0
    for word in l_list:
        index = index + 1
        if word == "Y" or word == "N":
            validated = validated + word
            break
        validated = validated + word + "|"
    if index != len(l_list):
        validated = validated + "|" + " ".join(l_list[index:len(l_list)])
    print(left_symbol + validated)


def check_tag_level(l_list):
    if "INDI" not in l_list and "FAM" not in l_list:
        if l_list[1] in tag_level.keys():
            return tag_level[l_list[1]] == l_list[0]
        else:
            return False
    else:
        if len(l_list) == 3 and (l_list[2] == "INDI" or l_list[2] == "FAM"):
            return True
        else:
            return False


def get_tag(l_list):
    for word in l_list:
        if word in tag_level.keys():
            return word
    return ""


gedcom_check(file_path)
