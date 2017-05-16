from owlready import get_ontology, onto_path, Thing, Property, NOT, restriction, SOME, MIN

#this bases entirely on http://pythonhosted.org/Owlready/


onto = get_ontology("http://cstenkamp.bplaced.net/onto_base.owl")
onto_path.append("./owlready/")

onto.load()

class Object(Thing):
     ontology = onto
     
class FilmFigure(Object):
    pass

class Vehicle(Object):
     pass

class Part(Object):
    pass  

class Terrain(Object):
    pass

class Plane(Vehicle):
    pass
######################################################


class Tire(Part):
    pass

class Ground(Terrain):
    pass

class Water(Terrain):
    pass

class Air(Terrain):
    pass

    
class has_part(Property):
    ontology = onto
    domain   = [Vehicle]
    range    = [Part]    
    
    
class acts_on(Property):
    ontology = onto
    domain   = [Vehicle]
    range    = [Terrain]    


class GroundVehicle(Vehicle):
     equivalent_to = [Vehicle & NOT(restriction(acts_on, SOME, Water)) & NOT(restriction(acts_on, SOME, Air))]
     
class Car(Vehicle):
     equivalent_to = [GroundVehicle & restriction(has_part, MIN, 4, Tire)]   



class Boat(Vehicle):
     equivalent_to = [Vehicle & NOT(GroundVehicle) & NOT(Plane)]


earth = Ground("earth")
sea = Water("sea")
germanair = Air("AirInGermany")

goodyear = Tire("goodyear")

#Car.acts_on.append(earth)
#Boat.acts_on.append(Water)
#warum schmeißen die beiden nen Error, warum kann ich das nicht ausführen?
#würde ich die Klassen eindeutig ("class Car(Vehicle): ....") definieren, ginge es...
#...und funny enough, wenn ich diesen export in protege einlese kann ich das äquivalent dazu machen (also manuell)



Plane.acts_on.append(germanair)

######################################################

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

print_what_is(Car)
print_what_is(Boat)
print_what_is(Plane)

#print(Car.has_part)
 
#######################################################
herbie = Car("Herbie")
KIT = Car("KIT")
famousplane = Plane("famousplane")

herbie.is_a.append(FilmFigure)
KIT.is_a.append(FilmFigure)
for i in Car.instances(): print_what_is(i)


#print(herbie.is_a[0].acts_on)
print(famousplane.is_a[0].acts_on)
#######################################################


onto.save()

#diese ontology kann ich jetzt in bspw protege weiter extenden