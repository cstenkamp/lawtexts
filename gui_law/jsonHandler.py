import sys
import json
import os
from itertools import chain
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


def read_json_file(jsonFile):
    """ reads the jsonFiles and returns it """
    if not jsonFile.lower().endswith('.json'):
        print("Given File is no json")
        return
    with open(jsonFile, 'r') as f:
        datastor = json.load(f)
        return datastor


def write_json_file(item, path):
    """ writes the jsonFile to path, overwrites if existing """
    if not path.lower().endswith('.json'):
        path += ".json"
    # with open(path, "w") as f:
        # json.dump(item, f, ensure_ascii=False)
    final_json = json.dumps(item, indent=4, ensure_ascii=True)
    with open(path, "w") as file:
        file.write(final_json)
    print("wrote file")

ORDER = ["Name", "Kundennummer", "Ort", "Herstellungsdatum", "Prüfdatum", \
         "Komponenten", "Verwendungszwecke", "Verwendungsorte"]
MY_PATH = os.path.abspath(os.path.dirname(__file__))
MACHINE_PATH = MY_PATH + "/machines/"
JSON_PATH = os.path.abspath(os.path.join(MY_PATH, os.pardir)) + "/python_code/Main/json/"
ICON_PATH = MY_PATH + "/icons/"
EINHEITEN = [x.lower() for x in list(chain(*list(read_json_file(JSON_PATH + "/features.json")["Features"].values())))] + \
            [x.lower() for x in read_json_file(JSON_PATH + "/contents.json")["Aggregatszustand"]]
