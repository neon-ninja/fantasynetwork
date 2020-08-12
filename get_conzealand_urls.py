#!/usr/bin/env python3

import requests
import json
import os

tabLookup = {}
videoLookup = {}

with open("api2_get_tab.json") as f:
    tab = json.load(f)
    for t in tab:
        tabLookup[t["TabId"]] = t

with open("api2_get_video.json") as f:
    video = json.load(f)
    for v in video:
        videoLookup[v["VideoId"]] = v

for t in tab:
    if t["Name"] == "CoNZealand Programming":
        items = t["Items"]

def make_safe(s):
    return "".join([c for c in s if c.isalpha() or c.isdigit() or c==' ']).rstrip()

for item in items:
    t = tabLookup[item["ChildId"]]
    top_level = make_safe(t["Name"])
    print(f"mkdir -p '{top_level}'")
    for child in t["Items"]:
        if child["Type"] == "collection":
            child = tabLookup[child["ChildId"]]
            second_level = make_safe(child["Name"])
            print(f"mkdir -p '{os.path.join(top_level, second_level)}'")
            for subchild in child["Items"]:
                v = videoLookup[subchild["ChildId"]]
                for f in v["Files"]:
                    if f["Type"] == "1080":
                        print(f"wget -N '{f['URL']}' -O '{os.path.join(top_level, second_level, make_safe(v['Title']))}.mp4'")
        else:
            v = videoLookup[child["ChildId"]]
            for f in v["Files"]:
                if f["Type"] == "1080":
                    print(f"wget -N '{f['URL']}' -O '{os.path.join(top_level, make_safe(v['Title']))}.mp4'")