from jsonHandler import *
from itertools import chain

jsonFile = {"Name":"", "Kundennummer":"", "Ort":"", "Herstellungsdatum":"", \
                 "Prüfdatum":"ab"}
print(any(jsonFile[key] == "ab" for key in jsonFile))
