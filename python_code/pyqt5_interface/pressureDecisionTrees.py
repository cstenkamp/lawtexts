
def Graph1_descision_tree(volume,druck):
    result = "no result"
    
    PS_1 = 0.5
    PS_2 = 200
    PS_3 = 1000
    
    PS_V_1 = 25
    PS_V_2 = 50
    PS_V_3 = 200
    PS_V_4 = 1000

    if volume < 1:
        if druck < PS_2:
            result = "Artikel 4, Absatz 3"
        elif druck >= PS_2 and druck < PS_3:
            result = "Gruppe III"
        elif druck >= PS_3: 
            result = "Gruppe IV"
    elif volume >= 1 and volume < 2000:
        if volume*druck < PS_V_1:
            result = "Artikel 4, Absatz 3"
        elif volume*druck >= PS_V_1 and druck < GPS_V_2:
            result = "Gruppe I"
        elif volume*druck >= PS_V_2 and druck < PS_V_3:
            result = "Gruppe II"
        elif volume*druck >= PS_V_3 and druck < PS_V_4:
            result = "Gruppe III"
        elif volume*druck >= PS_V_4:
            result = "Gruppe IV"

    elif volume >= 2000: 
        if volume*druck < PS_V_4:
            result = "Gruppe III"
        elif volume*druck >= PS_V_4:   
            result = "Gruppe IV"
    return result

def Graph2_descision_tree(volume,druck):
    result = "no result"
    
    PS_1 = 0.5
    PS_2 = 4
    PS_3 = 1000
    PS_4 = 3000
    
    PS_V_1 = 50
    PS_V_2 = 200
    PS_V_3 = 1000
    PS_V_4 = 3000

    if volume < 1:
        if druck < PS_3:
            result = "Artikel 4, Absatz 3"
        elif druck >= PS_3 and druck < PS_4:
            result = "Gruppe III"
        elif druck >= PS_4: 
            result = "Gruppe IV"
    elif volume >= 1 and volume <= 750:
        if volume*druck < PS_V_1:
                result = "Artikel 4, Absatz 3"
        elif volume*druck >= PS_V_1 and druck < PS_V_2:
                result = "Gruppe I"
        elif volume*druck >= PS_V_2 and druck < PS_V_3:
                result = "Gruppe II"
        elif volume*druck >= PS_V_3 and druck < PS_V_4:
                result = "Gruppe III"
        elif volume*druck >= PS_V_4:
                result = "Gruppe IV"
    elif volume < 750 and volume <= 2000:
        if volume*druck < PS_V_3:
                result = "Gruppe II"
        elif volume*druck >= PS_V_3 and druck < PS_2:
                result = "Gruppe III"
        elif volume*druck >= PS_V_3 and druck > PS_2:
                result = "Gruppe IV"
    elif volume > 2000:
        if volume*druck < PS_V_4:
            result = "Gruppe III"
        elif volume*druck >= PS_V_4:
            result = "Gruppe IV"
    return result
        

def Graph3_descision_tree(volume,druck):
    result = "no result"
    
    PS_1 = 0.5
    PS_2 = 10
    PS_3 = 500
    
    PS_V_1 = 200
   

    if volume < 1:
        if druck < PS_3:
            result = "Artikel 4, Absatz 3"
        elif druck >= PS_3 and druck < PS_4:
                result = "Gruppe II"
    elif volume >= 1 and volume <= 400:
        if volume*druck < PS_V_1:
                result = "Artikel 4, Absatz 3"
        elif volume*druck >= PS_V_1 and druck < PS_2:
                result = "Gruppe I"
        elif volume*druck >= PS_V_1 and (druck > PS_2 and druck < PS_3):
                result = "Gruppe II"
        elif volume*druck >= PS_V_1 and druck > PS_3:
                result = "Gruppe III"
    elif volume > 400:
        if druck < PS_2:
                result = "Gruppe I"
        elif druck >= PS_2 and druck < PS_3:
                result = "Gruppe II"
        elif druck >= PS_3:
                result = "Gruppe III"
    return result
    
             

def Graph4_descision_tree(volume,druck):
    result = "no result"
    
    PS_1 = 0.5
    PS_2 = 10
    PS_3 = 500
    PS_4 = 1000
    
    PS_V_1 = 10000
 
   
    if volume < 10:
        if druck < PS_4:
            result = "Artikel 4, Absatz 3"
        elif druck >= PS_4:
                result = "Gruppe I"
    elif volume >= 10 and volume <= 1000:
        if volume*druck < PS_V_1:
                result = "Artikel 4, Absatz 3"
        elif volume*druck >= PS_V_1 and druck < PS_3:
                result = "Gruppe I"
        elif volume*druck >= PS_V_1 and druck >= PS_3:
                result = "Gruppe II"
    elif volume > 1000:
        if druck < PS_2:
                result = "Artikel 4, Absatz 3"
        elif druck >= PS_2 and druck < PS_3:
                result = "Gruppe I"
        elif druck >= PS_3:
                result = "Gruppe II"
    return result
        
def Graph5_descision_tree(volume,druck):
    result = "no result"
    
    PS_1 = 0.5
    PS_2 = 32
    
    PS_V_1 = 50
    PS_V_2 = 200
    PS_V_3 = 3000
 

    if volume < 2:
        result = "Artikel 4, Absatz 3"
       
    elif volume >= 2 and volume <= 100:
        if volume*druck < PS_V_1:
            result = "Gruppe I"
        elif volume*druck >= PS_V_1 and druck < PS_V_2:      
            result = "Gruppe II"
        elif volume*druck >= PS_V_2 and druck <= PS_2:
            result = "Gruppe III"
        elif druck >= PS_2:
            result = "Gruppe IV"
    elif volume > 100 and volume <= 1000:
        if volume*druck < PS_V_2:
                result = "Gruppe II"
        elif volume*druck >= PS_V_2 and volume*druck < PS_V_3:
                result = "Gruppe III"
        elif volume*druck >= PS_V_3:
                result = "Gruppe IV"
    elif volume >= 1000:
        result = "Gruppe IV"
    return result
        


def Graph6_descision_tree(dn,druck):
    result = "no result"
    
    PS_1 = 0.5
    PS_2 = 32
    
    PS_DN_1 = 1000
    PS_DN_2 = 3500

    print(dn*druck)

    if dn < 25:
        result = "Artikel 4, Absatz 3"
    elif dn >= 2 and dn <= 100:
        if dn*druck < PS_DN_1 :
            result = "Gruppe I"
        elif dn*druck >= PS_DN_1:      
            result = "Gruppe II"
    elif dn > 100 and dn <= 350:
        if dn*druck < PS_DN_2:
                result = "Gruppe II"
        elif dn*druck >= PS_DN_2:
                result = "Gruppe III"
    elif dn >= 350:
        result = "Gruppe III"
    return result


def Graph7_descision_tree(dn,druck):
    result = "no result"
    
    PS_1 = 0.5
    PS_2 = 32
    
    PS_DN_1 = 1000
    PS_DN_2 = 3500
    PS_DN_3 = 5000

    print(dn*druck)

    if dn < 32:
        result = "Artikel 4, Absatz 3"
    elif dn >= 32 and dn < 100:
        if dn*druck < PS_DN_1 :
            result = "Artikel 4, Absatz 3"
        elif dn*druck >= PS_DN_1:      
            result = "Gruppe I"
    elif dn >= 100 and dn <= 250:
        if dn*druck < PS_DN_1 :
            result = "Artikel 4, Absatz 3"
        elif dn*druck >= PS_DN_1 and dn*druck < PS_DN_2:
            result = "Gruppe I"
        elif dn*druck >= PS_DN_2:
            result = "Gruppe II"
    elif dn >= 250:
        if dn*druck < PS_DN_1:
            result = "Artikel 4, Absatz 3"
        elif dn*druck >= PS_DN_1 and dn*druck < PS_DN_2:
            result = "Gruppe I"
        elif dn*druck >= PS_DN_2 and dn*druck < PS_DN_3:
            result = "Gruppe II"
        elif dn*druck >= PS_DN_3:
            result = "Gruppe III"
    return result


def Graph8_descision_tree(dn,druck):
    result = "no result"
    
    PS_1 = 0.5
    PS_2 = 10
    PS_3 = 500
    
    PS_DN_1 = 2000

    print(dn*druck)

    if dn < 25:
        result = "Artikel 4, Absatz 3"
    elif dn >= 24 and dn < 4000:
        if dn*druck < PS_DN_1 :
            result = "Artikel 4, Absatz 3"
        elif dn*druck >= PS_DN_1 and druck < PS_2:
            result = "Gruppe I"
        elif dn*druck >= PS_DN_1 and (druck > PS_2 and druck < PS_3):
            result = "Gruppe II"
        elif druck > PS_3:
            result = "Gruppe III"  
    elif dn >= 4000:
        print('here')
        if druck < PS_2:
            result = "Gruppe I"
        elif druck >= PS_2 and druck < PS_3:
            result = "Gruppe II"
        elif druck >= PS_3:
            result = "Gruppe III"
    return result


def Graph9_descision_tree(dn,druck):
    result = "no result"
    
    PS_1 = 0.5
    PS_2 = 10
    PS_3 = 500
    
    PS_DN_1 = 5000


    if dn < 200:
        result = "Artikel 4, Absatz 3"
    elif dn >= 200 and dn < 500:
        if dn*druck < PS_DN_1 :
            result = "Artikel 4, Absatz 3"
        elif dn*druck >= PS_DN_1 and druck < PS_3:
            result = "Gruppe I"
        elif druck >= PS_3:
            result = "Gruppe II"
    elif dn >= 500:
        if druck < PS_2:
            result = "Artikel 4, Absatz 3"
        elif druck >= PS_2 and druck < PS_3:
            result = "Gruppe I"
        elif druck >= PS_3:
            result = "Gruppe II"
    return result



def pressureMainTree(objekt,stateOfMatter,group,pressure,volume):
    print(objekt,stateOfMatter,group,pressure,volume)
    message = ""
    if objekt in ["Behälter"] and stateOfMatter == "verfüssigtes Gas":
        if group == 1: 
            result = Graph1_descision_tree(volume,pressure)
        if group == 2: 
            result = Graph2_descision_tree(volume,pressure)
            print("el resultado que llega es:::::")
    if objekt in ["Behälter"] and stateOfMatter == "flüssig":
        if group == 1: 
            result = Graph3_descision_tree(volume,pressure)
        if group == 2: 
            result = Graph4_descision_tree(volume,pressure)
    if objekt == "Dampferzeuger (Kessel)":
            result = Graph5_descision_tree(volume,pressure)        
    if objekt in ["Rohrleitung",'Druckrohr'] and stateOfMatter == "verflüssigtes Gas":
        if group == 1: 
            result = Graph6_descision_tree(volume,pressure)
        if group == 2: 
            result = Graph7_descision_tree(volume,pressure)
    if objekt in ["Rohrleitung",'Druckrohr'] and stateOfMatter == "flüssig":
        if group == 1: 
            result = Graph8_descision_tree(volume,pressure)
        if group == 2: 
            result = Graph9_descision_tree(volume,pressure)
    return result
