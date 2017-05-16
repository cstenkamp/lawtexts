# -*- coding: utf-8 -*-
"""
Created on Tue May  9 16:39:48 2017

@author: csten_000
"""
import xml.etree.ElementTree as ET
import types
from owlready import get_ontology, onto_path, Thing, Property, NOT, restriction, SOME, MIN


onto = get_ontology("http://cstenkamp.bplaced.net/onto_base.owl")
onto_path.append("./owlready/")
onto.load()
class Object(Thing):
     ontology = onto


def load_tree(FileName):
    tree = ET.parse(FileName)
    root = tree.getroot()
    for norm in root:    
        for point in norm:
            for p2 in point:
                for p3 in p2:
                    for p4 in p3:
                        if p4.text is not None and "Diese Verordnung gilt für die Bereitstellung auf dem Markt und die Inbetriebnahme von folgenden neuen Produkten" in p4.text:
                            Machine = types.new_class("Maschinen", (Object,), kwds = { "ontology" : onto })
                            for p5 in p4:
                                for p6 in p5:
                                    for p7 in p6:
                                        #print(p7.text)
                                        Machine(p7.text)
                                        
    for i in Machine.instances(): print_what_is(i)


def print_what_is(origobj):
    obj = origobj
    what_it_is = []
    while True:
        try:
            what_it_is.extend(obj.is_a)
            obj = obj.is_a[0]
        except IndexError:
            break
    print(origobj.name, "is", what_it_is)
    
    

def read_tree(FileName):
    tree = ET.parse(FileName)
    root = tree.getroot()
    for norm in root:    
        for point in norm:
            print(point.tag)
            for p2 in point:
                print("   ",p2.tag)
                for p3 in p2:
                    print("      ", p3.tag)
                    for p4 in p3:
                        print("         ", p4.text)
                        for p5 in p4:
                            for p6 in p5:
                                for p7 in p6:
                                    print("            ", p7.text)



def main():
    read_tree("prodsv9.xml")
    print("")
    print("")
    load_tree("prodsv9.xml")





if __name__ == '__main__':    
    main()