'''CONTCAR Parser'''


#### 1) Fetching data ####
def ImportCONTCAR():
    #Open POSCAR File
    #===================================================================================
    with open('CONTCAR','r') as POSCARfile: #Read POSCAR file
        linedata=POSCARfile.readlines()
        for i in range(len(linedata)): #Among linedata, if Direct or Cartesian is present, then linenumber_dc
            if linedata[i].find('Direct')>-1 or linedata[i].find('direct')>-1:
                linenumber_dc=i
                Direct=True
            elif linedata[i].find('Cartesian')>-1 or linedata[i].find('cartesian')>-1:
                linenumber_dc=i
                Direct=False
    #===================================================================================

    #Storing information about each line
    #===================================================================================
    linenumber_Lattice_Parameter=2
    linenumber_Atom_Name=5
    linenumber_Atom_Number=6
    #===================================================================================

    #Fetch data
    #===================================================================================
    lattice_parameters=linedata[2:5] #Extract Lattice Parameter
    Atom_Name=linedata[5].split() #Extract atom names
    Atom_Count=linedata[6].split() #Extract atom count
    Atom_Count=[int(i) for i in Atom_Count] #Convert to integer
    coordinates=linedata[linenumber_dc+1:] #Extract Coordination
    #===================================================================================

    return Direct, linenumber_dc, linenumber_Lattice_Parameter, linenumber_Atom_Name, linenumber_Atom_Number, lattice_parameters, Atom_Name, Atom_Count, coordinates

#### 2) Data refinement: Convert to list, table for easy handling, and convert numbers to int, float ####

def LP_Refine(lattice_parameters):
    #Lattice Parameter Refine
    #===================================================================================
    LP=[]
    for i in range(len(lattice_parameters)):
        lattice_parameters[i]=lattice_parameters[i].replace('\n','').replace('\r','')
        LP.append(lattice_parameters[i].split(' '))

    for j in range(len(LP)):
        LP[j] = [float(k) for k in LP[j] if k != '']
    #===================================================================================
    return LP

def Coordination_Refine(coordinates, LP, Direct):
    #Coordination Refine
    #===================================================================================
    coordi=[]
    for i in range(len(coordinates)):
        if len(coordinates[i]) <= 2: #If empty space is created, then Stop
            break
        coordinates[i]=coordinates[i].replace('\n','').replace('\r','')
        coordi.append(coordinates[i].split(' '))

    for j in range(len(coordi)):
        coordi[j] = [k for k in coordi[j] if k != '']

    #Direct -> Cartesian Transform
    #----------------------------------------------------------------------------------
    if Direct == True:
        for d in range(len(coordi)):
            cart_coordi_a=float(coordi[d][0])*LP[0][0] + float(coordi[d][1])*LP[1][0] + float(coordi[d][2])*LP[2][0]
            cart_coordi_b=float(coordi[d][0])*LP[0][1] + float(coordi[d][1])*LP[1][1] + float(coordi[d][2])*LP[2][1]
            cart_coordi_c=float(coordi[d][0])*LP[0][2] + float(coordi[d][1])*LP[1][2] + float(coordi[d][2])*LP[2][2]
            coordi[d] = [str(cart_coordi_a), str(cart_coordi_b), str(cart_coordi_c)]

    return coordi
    #===================================================================================

def Generate_Separated_List(coordi, Atom_Name, Atom_Count):
    #Generate Separated Coordination
    #===================================================================================
    #Coordination Separated by Atom Type
    Separated_List=[] #★★★Separated_List : Individual Coordination according to Atom Type ★★★
    Previous_Start=0
    for i in range(len(Atom_Name)):
        Separated_List.append(coordi[Previous_Start:Previous_Start + Atom_Count[i]])
        Previous_Start+=Atom_Count[i]
    return Separated_List

def DataRefine_Mainfunction(lattice_parameters, Atom_Name, Atom_Count, coordinates, Direct):
    LP = LP_Refine(lattice_parameters)
    coordi = Coordination_Refine(coordinates, LP, Direct)
    Separated_List = Generate_Separated_List(coordi, Atom_Name, Atom_Count)

    #Atom Labeling
    #===================================================================================
    #Get a list made only of labels, initially performed by this process
    #-----------------------------------------------------------------------------------
    Labellist=[]
    for Total_Atoms, Atom in zip(Atom_Count, Atom_Name):
        for Atom_Iteration in range(1,Total_Atoms+1):
            label=Atom+str(Atom_Iteration)
            Labellist.append(label)
    #-----------------------------------------------------------------------------------

    #If the number of labels and coordi do not match, print a warning
    #-----------------------------------------------------------------------------------
    if len(Labellist) != len(coordi):
        print("The number of atoms indicated above does not match the number of coordinates!")
        print('Number of atoms indicated above : {}'.format(len(Labellist)))
        print('Number of coordinates : {}'.format(len(coordi)))

    return LP, coordi, Separated_List, Labellist

#Combine Labellist and Coordination to display as a Dictionary
#-----------------------------------------------------------------------------------
def Coord_to_dict(Labellist, coordi):
    Coordi_dict={i:j for i, j in zip(Labellist,coordi)}

    print('======================= Coordination Information ==============================')
    print('{:^5} | {:^5} | {:^20}|{:^20}|{:^20}'.format('Index', 'Label', 'X', 'Y', 'Z'))
    print('===============================================================================')
    for en, i in enumerate(range(len(Coordi_dict.keys()))):
        print('{:^5} : {:^5} : {:^20} {:^20} {:^20}'.format(en+1,
                                                            list(Coordi_dict.keys())[i],
                                                            Coordi_dict[list(Coordi_dict.keys())[i]][0],
                                                            Coordi_dict[list(Coordi_dict.keys())[i]][1],
                                                            Coordi_dict[list(Coordi_dict.keys())[i]][2]))
    print('===============================================================================')
    return Coordi_dict
#-----------------------------------------------------------------------------------
