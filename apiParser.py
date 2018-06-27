import requests
import json
import re


time_pattern = "(\d+)'\+(\d+)"


def get_data():
    r = requests.get('https://world-cup-json.herokuapp.com/matches/today')
    return r.json()


def load_data(path):
    with open(path) as f:
        data = json.load(f)
    return data


# fix for  "90'+1'" and "half-time" or "null"
def fix_time(time):
    if time:
        if time == "half-time":
            return "HALF "
        elif time == "null":
            return "0    "
        elif time == "full-time":
            return "FULL "
        elif "+" in time:
            m = re.search(time_pattern, time)
            return str(int(m.group(1)) + int(m.group(2))) + "'"
        else:
            return time + "  "
    return "NEXT "


# format string (separated with commas):
#   N1 - first home team name,
#   N2 - first away team name,
#   S1 - first home team score,
#   S2 - first away team score,
#   t - time for second match (example 45')
#   s - space
# example format string: "s,s,s,N1,S1,-,N1,S1"
def create_data_string(data, format, match_number):
    #active_matches = get_active_matches(data)
    commands = format.split(sep=',')
    result = ""
    for command in commands:
        if command == 's':
            result += " "
        elif command == 'N1':
            result += data[match_number]["home_team"]["code"]
        elif command == 'N2':
            result += data[match_number]["away_team"]["code"]
        elif command == 'S1':
            result += str(data[match_number]["home_team"]["goals"])
        elif command == 'S2':
            result += str(data[match_number]["away_team"]["goals"])
        elif command == 't':
            result += fix_time(data[match_number]["time"])
        else:
            result += command
    return result


if __name__ == "__main__":
    data = get_data()
    i = 0
    for match_data in data:
        print(create_data_string(data, "t,s,s,s,N1,s,S1,-,S2,s,N2,s", i))
        i = i+1

