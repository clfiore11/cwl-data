import pandas as pd
import numpy as np
import os
import warnings
import csv
import re

os.chdir("../data")
files = os.listdir(os.curdir)


def load_csv(filename):
    """Helper to load the tournament data from csv."""
    rows = []
    with open(filename) as f:
        reader = csv.DictReader(f)
        rows.extend(iter(reader))
    return rows


data_files = [item for item in files if item.startswith("data")]

# Initialize two empty list
cwl_2018 = []
cwl_2019 = []

for data in sorted(data_files)[1:]:
    # If file is 2018 add the cwl 2018
    if re.search("2018", data) or re.search("2017", data):
        df = pd.DataFrame(load_csv(data))
        df["tournament"] = data.split("-")[-1].replace(".csv", "")
        cwl_2018.append(df)
    # If file is 2019 add the cwl 2019
    if re.search("2019", data):
        df = pd.DataFrame(load_csv(data))
        df["tournament"] = data.split("-")[-1].replace(".csv", "")
        cwl_2019.append(df)

# Creating the stacked df
cwl_2018_season = pd.concat(cwl_2018)
cwl_2019_season = pd.concat(cwl_2019)

# add year label
cwl_2018_season["year"] = 2018
cwl_2019_season["year"] = 2019

# Cleaning up the System
del cwl_2018, cwl_2019

hp = [
    "year",
    "tournament",
    "match id",
    "series id",
    "end time",
    "duration (s)",
    "mode",
    "map",
    "team",
    "player",
    "win?",
    "score",
    "kills",
    "deaths",
    "+/-",
    "k/d",
    "kills per 10min",
    "deaths per 10min",
    "assists",
    "headshots",
    "suicides",
    "team kills",
    "team deaths",
    "kills (stayed alive)",
    "hits",
    "shots",
    "accuracy (%)",
    "num lives",
    "time alive (s)",
    "avg time per life (s)",
    "hill time (s)",
    "hill captures",
    "hill defends",
    "2-piece",
    "3-piece",
    "4-piece",
    "4-streak",
    "5-streak",
    "6-streak",
    "7-streak",
    "8+-streak",
]

snd = [
    "year",
    "tournament",
    "match id",
    "series id",
    "end time",
    "duration (s)",
    "mode",
    "map",
    "team",
    "player",
    "win?",
    "score",
    "kills",
    "deaths",
    "+/-",
    "k/d",
    "kills per 10min",
    "deaths per 10min",
    "assists",
    "headshots",
    "suicides",
    "team kills",
    "team deaths",
    "kills (stayed alive)",
    "hits",
    "shots",
    "accuracy (%)",
    "num lives",
    "time alive (s)",
    "avg time per life (s)",
    "snd rounds",
    "snd firstbloods",
    "snd firstdeaths",
    "snd survives",
    "bomb pickups",
    "bomb plants",
    "bomb defuses",
    "bomb sneak defuses",
    "snd 1-kill round",
    "snd 2-kill round",
    "snd 3-kill round",
    "snd 4-kill round",
    "2-piece",
    "3-piece",
    "4-piece",
    "4-streak",
    "5-streak",
    "6-streak",
    "7-streak",
    "8+-streak",
]

# CWL 2018 HP Data & CWL 2018 SND Data
cwl_2018_hp = cwl_2018_season[cwl_2018_season["mode"] == "Hardpoint"][hp]
cwl_2018_snd = cwl_2018_season[cwl_2018_season["mode"] == "Search & Destroy"][snd]

# CWL 2018 HP Data & CWL 2018 SND Data
cwl_2019_hp = cwl_2019_season[cwl_2019_season["mode"] == "Hardpoint"][hp]
cwl_2019_snd = cwl_2019_season[cwl_2019_season["mode"] == "Search & Destroy"][snd]

cwl_2018_2019_hp = pd.concat([cwl_2018_hp, cwl_2019_hp])
cwl_2018_2019_snd = pd.concat([cwl_2018_snd])

cwl_2018_2019_hp["accuracy (%)"] = cwl_2018_2019_hp["accuracy (%)"].str.replace("%", "")
cwl_2018_2019_hp["duration (s)"] = cwl_2018_2019_hp["duration (s)"].astype(float)

cwl_2018_2019_hp.iloc[:, range(10, 40)] = cwl_2018_2019_hp.iloc[:, range(10, 40)].apply(
    pd.to_numeric, errors="coerce"
)

cwl_2018_2019_snd["accuracy (%)"] = cwl_2018_2019_snd["accuracy (%)"].str.replace(
    "%", ""
)
cwl_2018_2019_snd["duration (s)"] = cwl_2018_2019_snd["duration (s)"].astype(float)

cwl_2018_2019_snd.iloc[:, range(10, 40)] = cwl_2018_2019_snd.iloc[
    :, range(10, 40)
].apply(pd.to_numeric, errors="coerce")

cwl_2018_2019_snd.to_csv("cwl_2018_2019_snd.csv")
cwl_2018_2019_hp.to_csv("cwl_2018_2019_hp.csv")
