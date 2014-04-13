import json
import os
import sys

path = sys.argv[1]
TMP = "/tmp.json"
CURRENT = "/current_data.json"
DIFF = "/new_data.json"
OLD = "/old_data.json"


if os.path.isfile(path + CURRENT):
    with open(path + TMP) as f:
        new = json.load(f)

    with open(path + CURRENT) as f:
        old = json.load(f)

    difference = []
    for n in new:
        found = False
        for o in old:
            if n["pk"] == o["pk"] and n["model"] == o["model"]:
                found = True
                break
        if not found:
            difference.append(n)

    with open(path + DIFF, "w") as f:
        json.dump(difference, f, indent=4)

    os.rename(path + CURRENT, path + OLD)

os.rename(path + TMP, path + CURRENT)