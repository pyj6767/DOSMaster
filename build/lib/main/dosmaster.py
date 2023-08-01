#!/usr/bin/env python
#======================================================================================================
#Script Name : dosmaster Program(ver.1.4.2)
#Made by Youngjun Park (yjpark29@postech.ac.kr)
#Inspired by Jaesun Kim
#Edit Date : 23/06/21
#======================================================================================================
#Description : DOS Plot Smartly
#======================================================================================================
#: 1) Add Atom DOS
#: 2) DOS Projection
#: 3) Remove DOS
#: 4) Edit Graph Style
#: 5) Plot only Positive/Negative part
#: 6) DOS sum (Not Implemented)
#: 7) ISPIN=1 Support (Not Implemented)
#: 8) Find Max Contribution Atom DOS (Not Implemented)
#: 9) Edit Legend Name (Not Implemented)
#======================================================================================================

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib._color_data import BASE_COLORS, TABLEAU_COLORS, CSS4_COLORS, XKCD_COLORS
import ase
import os.path
from os import path
import pickle


def StartMessage():
    print("#############################################################################################")
    print("###################                                                   #######################")
    print("###################                      dosmaster                    #######################")
    print("###################                                                   #######################")
    print("###################                            version : 1.0          #######################")
    print("###################                                                   #######################")
    print("###################                                2023.06.15         #######################")
    print("###################                        yjpark29@postech.ac.kr     #######################")
    print("###################                          Young-jun Park(CNMD)     #######################")
    print("###################                                                   #######################")
    print("#############################################################################################")

#### 1) 데이터 들고 오기 ####
#◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇

def ImportCONTCAR():
    #Open POSCAR File
    #===================================================================================
    POSCARfile = open('CONTCAR','r') #POSCAR 파일 읽기
    linedata=POSCARfile.readlines()
    for i in range(len(linedata)): #linedata들 중에서 Direct 또는 Cartesian이 있으면, linenumber_dc
        if linedata[i].find('Direct')>-1 or linedata[i].find('direct')>-1:
            linenumber_dc=i
            Direct=True
        elif linedata[i].find('Cartesian')>-1 or linedata[i].find('cartesian')>-1:
            linenumber_dc=i
            Direct=False
    #===================================================================================

    #각각의 줄이 나타내는 정보 저장하기
    #===================================================================================
    linenumber_Lattice_Parameter=2
    linenumber_Atom_Name=5
    linenumber_Atom_Number=6
    #===================================================================================

    #데이터 불러오기
    #===================================================================================
    lattice_parameters=linedata[2:5] #Lattice Parameter 추출
    Atom_Name=linedata[5].split() #원소 이름 추출
    Atom_Count=linedata[6].split() #원소 개수 추출
    Atom_Count=[int(i) for i in Atom_Count] #정수로 바꾸기
    coordinates=linedata[linenumber_dc+1:] #Coordination 추출하기
    #===================================================================================

    return Direct, linenumber_dc, linenumber_Lattice_Parameter, linenumber_Atom_Name, linenumber_Atom_Number, lattice_parameters, Atom_Name, Atom_Count, coordinates

#◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇


#### 2) 데이터 정제 작업 : 다루기 쉽게 리스트, 테이블 형태로 전환하고, 숫자는 int, float 형식으로 바꾸기 ####
#◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇◇

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
        if len(coordinates[i]) <= 2: #빈 영역이 생기면 바로 Stop
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

    #Atom Labeling하기
    #===================================================================================
    #Label로만 이루어진 리스트 얻기, 초기에만 이 과정으로 수행
    #-----------------------------------------------------------------------------------
    Labellist=[]
    for Total_Atoms, Atom in zip(Atom_Count, Atom_Name):
        for Atom_Iteration in range(1,Total_Atoms+1):
            label=Atom+str(Atom_Iteration)
            Labellist.append(label)
    #-----------------------------------------------------------------------------------

    #Label 개수와 coordi 개수가 맞지 않으면, 경고를 Print
    #-----------------------------------------------------------------------------------
    if len(Labellist) != len(coordi):
        print("위쪽에 표시한 원자 개수와, 좌표의 개수가 달라요!")
        print('위쪽에 표시한 원자 개수 : {}'.format(len(Labellist)))
        print('좌표의 개수 : {}'.format(len(coordi)))

    return LP, coordi, Separated_List, Labellist

#Labellist와 Coordination을 묶어서 Dictionary로 나타내기
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

def print_current_DOS(DOS_list, Labellist, graph_config):
    print('=============================================[현재 출력되는 DOS 리스트]============================================')
    for i, d in enumerate(DOS_list):
        if isinstance(d, list)==True:
            labeled_d = [Labellist[int(d_temp.split('_')[0])-1]+'('+d_temp.split('_')[1]+')' for d_temp in d]
            print_element=' + '.join(labeled_d)

        else:
            if d == 'Total DOS_all':
                print_element='Total DOS(all)'
                
            elif d.split('_')[0] == 'Total DOS' and d.split('_')[1] != 'all':
                print_element='Total DOS_{}'.format(d.split('_')[1])

            else:
                print_element=Labellist[int(d.split('_')[0])-1]+'('+d.split('_')[1]+')'

        print('{:<4} : {:<80} | color : {:<30}'.format(i+1, print_element, graph_config['Color_list'][i]))
    print('==================================================================================================================')
    
def get_current_DOS(DOS_list, Labellist, graph_config):
    dos_column_list=[]
    for i, d in enumerate(DOS_list):
        if isinstance(d, list)==True:
            labeled_d = [Labellist[int(d_temp.split('_')[0])-1]+'('+d_temp.split('_')[1]+')' for d_temp in d]
            print_element='+'.join(labeled_d)

        else:
            if d == 'Total DOS_all':
                print_element='Total_DOS(all)'
                
            elif d.split('_')[0] == 'Total DOS' and d.split('_')[1] != 'all':
                print_element='Total_DOS_{}'.format(d.split('_')[1])

            else:
                print_element=Labellist[int(d.split('_')[0])-1]+'('+d.split('_')[1]+')'
        
        dos_column_list.append(print_element)
        
    return dos_column_list
    
def print_orbital_list(orbital_list):
    for i, orbital in enumerate(orbital_list):
        print('{} : {}'.format(i+1, orbital))
        
#===============================================[get Color list]================================================
def get_color_list():
    colors = mcolors.CSS4_COLORS
    # Sort colors by hue, saturation, value and name.
    sort_colors=True
    
    if sort_colors is True:
        by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgb(color))),
                         name)
                        for name, color in colors.items())
        names = [name for hsv, name in by_hsv]
    else:
        names = list(colors)
        
    new_color_dict={c:colors[c] for c in names}
        
    return new_color_dict

def python_color_list():
    def plot_colortable(colors, title, sort_colors=True, emptycols=0, shows=True):

        cell_width = 212
        cell_height = 22
        swatch_width = 48
        margin = 12
        topmargin = 40

        # Sort colors by hue, saturation, value and name.
        if sort_colors is True:
            by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgb(color))),
                             name)
                            for name, color in colors.items())
            names = [name for hsv, name in by_hsv]
        else:
            names = list(colors)

        #Modify : color name list change => label : name
        #----------------------------------------------------------------------------
        label_names={i+1:j for i,j in zip(range(len(names)),names)}
        #print(label_names)
        #----------------------------------------------------------------------------

        n = len(names)
        ncols = 4 - emptycols
        nrows = n // ncols + int(n % ncols > 0)

        width = cell_width * 4 + 2 * margin
        height = cell_height * nrows + margin + topmargin
        dpi = 72

        fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)
        fig.subplots_adjust(margin/width, margin/height,
                            (width-margin)/width, (height-topmargin)/height)
        ax.set_xlim(0, cell_width * 4)
        ax.set_ylim(cell_height * (nrows-0.5), -cell_height/2.)
        ax.yaxis.set_visible(False)
        ax.xaxis.set_visible(False)
        ax.set_axis_off()
        ax.set_title(title, fontsize=24, loc="left", pad=10)

        for i, name in enumerate(names):
            row = i % nrows
            col = i // nrows
            y = row * cell_height

            swatch_start_x = cell_width * col
            text_pos_x = cell_width * col + swatch_width + 7
            outputname = '{} : {}'.format(i, name)

            ax.text(text_pos_x, y, outputname, fontsize=14,
                    horizontalalignment='left',
                    verticalalignment='center')

            ax.add_patch(
                Rectangle(xy=(swatch_start_x, y-9), width=swatch_width,
                          height=18, facecolor=colors[name], edgecolor='0.7')
            )

        
        return fig, label_names, colors, names

    fig,names, colors, color_names=plot_colortable(mcolors.CSS4_COLORS, "CSS Colors")
    
    plt.show()
        
#===============================================[get Color list]================================================
        
#==========================================================================================[split_dos]===============================================================================
### Class to store DOS data ###
class DOSData:
    def __init__(self, e_f, dos_values):
        self.e_f = e_f
        self.dos_values = dos_values

### READ DOSCAR ###
def read_dosfile():
    f = open("DOSCAR", 'r')
    lines = f.readlines()
    f.close()
    index = 0
    natoms = int(lines[index].strip().split()[0])
    index = 5
    nedos = int(lines[index].strip().split()[2])
    efermi = float(lines[index].strip().split()[3])
    #print(natoms, nedos, efermi)

    return lines, index, natoms, nedos, efermi

### READ POSCAR or CONTCAR and save pos ###
def read_posfile():
    from ase.io import read

    try:
        atoms = read('POSCAR')
    except IOError:
        print("[__main__]: Couldn't open input file POSCAR, atomic positions will not be written...\n")
        atoms = []

    return atoms

### WRITE DOS0 CONTAINING TOTAL DOS ###
def write_dos0(lines, index, nedos, efermi):
    dos_data = []

    line = lines[index+1].strip().split()
    ncols = int(len(line))

    for n in range(nedos):
        index += 1
        e = float(lines[index].strip().split()[0])
        e_f = e - efermi

        dos_values = []
        for col in range(1, ncols):
            dos = float(lines[index].strip().split()[col])
            dos_values.append(dos)

        dos_entry = DOSData(e_f, dos_values)
        dos_data.append(dos_entry)

    return index, dos_data

### LOOP OVER SETS OF DOS, NATOMS ###
def write_nospin(lines, index, nedos, natoms, ncols, efermi):
    dos_data = []
    atoms = read_posfile()
    if len(atoms) < natoms:
        pos = np.zeros((natoms, 3))
    else:
        pos = atoms.get_positions()

    for i in range(1, natoms+1):
        si = str(i)

        index += 1
        ia = i - 1
        dos_values = []

        for n in range(nedos):
            index += 1
            e = float(lines[index].strip().split()[0])
            e_f = e - efermi
            dos_values.append([e_f] + [float(lines[index].strip().split()[col]) for col in range(1, ncols)])

        dos_entry = DOSData(pos[ia, 0], pos[ia, 1], pos[ia, 2], dos_values)
        dos_data.append(dos_entry)

    return index, dos_data

def write_spin(lines, index, nedos, natoms, ncols, efermi):
    dos_data = []
    atoms = read_posfile()
    if len(atoms) < natoms:
        pos = np.zeros((natoms, 3))
    else:
        pos = atoms.get_positions()

    nsites = int((ncols - 1) / 2)

    for i in range(1, natoms+1):
        si = str(i)

        index += 1
        ia = i - 1
        dos_values = []

        for n in range(nedos):
            index +=1
            e = float(lines[index].strip().split()[0])
            e_f = e - efermi

            dos_entries = [e_f]
            for site in range(nsites):
                dos_up = float(lines[index].strip().split()[site * 2 + 1])
                dos_down = float(lines[index].strip().split()[site * 2 + 2]) * -1
                dos_entries.extend([dos_up, dos_down])

            dos_values.append(dos_entries)
        dos_entry = DOSData(e_f, dos_values)
        dos_data.append(dos_entry)

    return index, dos_data

def split_dos():
    lines, index, natoms, nedos, efermi = read_dosfile()
    index, dos_data_total = write_dos0(lines, index, nedos, efermi)
    ## Test if a spin polarized calculation was performed ##
    line = lines[index+2].strip().split()
    ncols = int(len(line))

    if ncols == 7 or ncols == 19 or ncols == 9 or ncols == 33:
        index, dos_data = write_spin(lines, index, nedos, natoms, ncols, efermi)
        is_spin = True
    else:
        index, dos_data = write_nospin(lines, index, nedos, natoms, ncols, efermi)
        is_spin = False
    
    return dos_data_total, dos_data

#==========================================================================================[split_dos]===============================================================================

def PROCAR_Parser(file):
    file_data = open(file, 'r')
    file_data=file_data.readlines()
    orbital_list=file_data[7].split()
    orbital_list.remove('ion')
    orbital_list.remove('tot')
    
    return orbital_list

def Make_DOS_Dataframe():
    if path.isfile('./dos_data_total.pkl') == True:
        with open('./dos_data_total.pkl', 'rb') as f:
            dos_data_total = pickle.load(f)
        dos_object_total_dos=dos_data_total[0]
        dos_object_list=dos_data_total[1]
        orbital_list=dos_data_total[2]
    else:
        #0. split_dos 함수 실행
        dos_data_total, dos_data = split_dos()
    
        #1. PROCAR에서 orbital_list 받아오기
        orbital_list = PROCAR_Parser('./PROCAR')

        #2. 2차원 리스트 형태로 변환
        dos_data_total_list=[[dos_temp.e_f] + dos_temp.dos_values for dos_temp in dos_data_total]
        dos_object_list=[np.array(dos_object.dos_values) for dos_object in dos_data]

        column_names = []
        for ol in orbital_list:
            column_names.append(ol+'_up')
            column_names.append(ol+'_down')
        column_names.insert(0, 'Energy')

        #3. dos_data[각각]을 table로 변환하기(df)
        dos_object_total_dos = pd.DataFrame(dos_data_total_list)
        dos_object_list=[pd.DataFrame(dos_object, columns=column_names) for dos_object in dos_object_list]
        
        dos_data_total=[dos_object_total_dos, dos_object_list, orbital_list]
        with open('./dos_data_total.pkl', 'wb') as f:
            pickle.dump(dos_data_total, f)
            
    return dos_object_total_dos, dos_object_list, orbital_list
    
def split_dos_parser(atom_number, dataframe_object, element, orbital_list):
    if atom_number == 'total':
        energy=np.array(dataframe_object[0], dtype=np.float64)
        dos_up=np.array(dataframe_object[1], dtype=np.float64)
        dos_down=(-1)*np.array(dataframe_object[2], dtype=np.float64)
        return energy, dos_up, dos_down

    else:
        column_names = []
        for ol in orbital_list:
            column_names.append(ol+'_up')
            column_names.append(ol+'_down')
        column_names.insert(0, 'Energy')
        energy=np.array(list(dataframe_object['Energy']), dtype=np.float64)
        orbital_select_element = element.split('_')[1]
        
        if orbital_select_element == 'all':
            dos_up = np.array([0 for e in energy], dtype=np.float64)
            dos_down = np.array([0 for e in energy], dtype=np.float64)
            for cn in column_names[1:]:
                if cn.split('_')[1] == 'up':
                    dos_up += np.array(dataframe_object[cn])
                elif cn.split('_')[1] == 'down':
                    dos_down += np.array(dataframe_object[cn])
        
        elif orbital_select_element == 'p':
            dos_up = np.array([0 for e in energy], dtype=np.float64)
            dos_down = np.array([0 for e in energy], dtype=np.float64)
            for cn in column_names[1:]:
                if cn[0] == 'p':
                    if cn.split('_')[1] == 'up':
                        dos_up += np.array(dataframe_object[cn])
                    elif cn.split('_')[1] == 'down':
                        dos_down += np.array(dataframe_object[cn])
                        
        elif orbital_select_element == 'd':
            dos_up = np.array([0 for e in energy], dtype=np.float64)
            dos_down = np.array([0 for e in energy], dtype=np.float64)
            for cn in column_names[1:]:
                if cn[0] == 'd' or cn == 'x2-y2':
                    if cn.split('_')[1] == 'up':
                        dos_up += np.array(dataframe_object[cn])
                    elif cn.split('_')[1] == 'down':
                        dos_down += np.array(dataframe_object[cn])

        else:
            for cn in column_names[1:]:
                if cn == orbital_select_element+'_up':
                    dos_up = np.array(dataframe_object[cn], dtype=np.float64)
                elif cn == orbital_select_element+'_down':
                    dos_down = np.array(dataframe_object[cn], dtype=np.float64)
        
        return energy, dos_up, dos_down
    
def Get_DOS_Name(DOS_list, Labellist):
    name_list = []
    for index, element in enumerate(DOS_list):
        if isinstance(element, list) == False:
            if element.split('_')[0] == 'Total DOS':
                if element.split('_')[1] == 'all':
                    name = element.split('_')[0] + '(' + element.split('_')[1] + ')'
                else:
                    name = ''
            else:
                name = Labellist[int(element.split('_')[0])-1] + '(' + element.split('_')[1] + ')'
            
        else:
            net_list=[]
            net_orbital_list=[]
            for i, e in enumerate(element):
                if e.split('_')[0] not in net_list:
                    net_list.append(e.split('_')[0])
                    net_orbital_list.append([e.split('_')[1]])
                else:
                    net_orbital_list[net_list.index(e.split('_')[0])].append(e.split('_')[1])
            
            if len(net_list) == 1:
                name = ''
                for net, net_orbital in zip(net_list, net_orbital_list):
                    name += Labellist[int(net)-1]
                    name += '('
                    if len(net_orbital) == 1:
                        name += net_orbital[0]
                    elif len(net_orbital) > 1:
                        for no in net_orbital:
                            name += no
                            name += ','
                        name = name[:-1]
                    name += ')'
                    
            elif len(net_list) > 1:
                name = ''
                for net, net_orbital in zip(net_list, net_orbital_list):
                    name += Labellist[int(net)-1]
                    name += '('
                    if len(net_orbital) == 1:
                        name += net_orbital[0]
                    elif len(net_orbital) > 1:
                        for no in net_orbital:
                            name += no
                            name += ','
                        name = name[:-1]
                    name += ')'
                    name += ' + '
                name = name[:-3]
                    
        name_list.append(name)
            
    return name_list

def Get_User_Projection_Orbital_list(orbital_list):
    print_orbital_list(orbital_list)
    print('-------------------------------------------------------------------------------------------')
    print('이것은 번호입력방식이 아닙니다.')
    print('s p 라고만 입력하면, px py pz를 모두 합칩니다.')
    print('d 라고만 입력하면, dxy, dyz, dz2 dxz, x2-y2를 모두 합칩니다.')
    print('-------------------------------------------------------------------------------------------')
    orbital_select = input('Projection시킬 Orbital들을 선택하세요 (ex : s py pz 또는 s p) : ')

    user_orbital_list = orbital_select.split()
    
    return user_orbital_list
    
def data_collection(data_list, is_save, graph_config, energy, dos_data):
    if is_save == True:
        if len(data_list) == 0:
            data_list.append(energy)
            data_list.append(dos_data)
        else:
            data_list.append(dos_data)
    return data_list
    
def DOSplot(DOS_list, Color_list, Labellist, graph_config, color_dict, dos_object_total_dos, dos_object_list, orbital_list, is_save):
    name_list = Get_DOS_Name(DOS_list, Labellist)
    plt.figure(figsize=(graph_config['figuresize'][0],graph_config['figuresize'][1]))
    Total_DOS=False
    data_list_up=[]
    data_list_down=[]
    for index, DOS_temp in enumerate(DOS_list):
        if isinstance(DOS_temp, list) == False:
            if DOS_temp=='Total DOS_all':
                Total_DOS = True
                energy, dos_up, dos_down=split_dos_parser('total', dos_object_total_dos, DOS_temp, orbital_list)
                if graph_config['positive_plot'] == True:
                    plt.plot(energy, dos_up, color = color_dict[graph_config['Color_list'][index]], linewidth=graph_config['line_width'], label='Total DOS')
                    data_list_up=data_collection(data_list_up, is_save, graph_config, energy, dos_up)
                if graph_config['positive_plot'] == True and graph_config['negative_plot'] == True:
                    plt.plot(energy, dos_down, color = color_dict[graph_config['Color_list'][index]], linewidth=graph_config['line_width'])
                    data_list_down=data_collection(data_list_down, is_save, graph_config, energy, dos_down)
                if graph_config['positive_plot'] == False and graph_config['negative_plot'] == True:
                    plt.plot(energy, dos_down*(-1), color = color_dict[graph_config['Color_list'][index]], linewidth=graph_config['line_width'], label='Total DOS')
                    data_list_down=data_collection(data_list_down, is_save, graph_config, energy, dos_down)

            elif DOS_temp.split('_')[0] == 'Total DOS' and DOS_temp.split('_')[1] != 'all':
                orbital=DOS_temp.split('_')[1]
                dos_up_sum = 0
                dos_down_sum = 0
                for label_index, label in enumerate(Labellist):
                    energy, dos_up, dos_down = split_dos_parser(str(label_index+1), dos_object_list[label_index], str(label_index+1)+'_'+str(orbital), orbital_list)
                    if index == 0:
                        dos_up_sum = dos_up
                        dos_down_sum = dos_down
                    else:
                        dos_up_sum += dos_up
                        dos_down_sum += dos_down
                        
                if graph_config['positive_plot'] == True:
                    plt.plot(energy, dos_up_sum, color = color_dict[graph_config['Color_list'][index]], linewidth=graph_config['line_width'], label = 'Total DOS({})'.format(orbital))
                    data_list_up=data_collection(data_list_up, is_save, graph_config, energy, dos_up_sum)
                if graph_config['positive_plot'] == True and graph_config['negative_plot'] == True:
                    plt.plot(energy, dos_down_sum, color = color_dict[graph_config['Color_list'][index]], linewidth=graph_config['line_width'])
                    data_list_down=data_collection(data_list_down, is_save, graph_config, energy, dos_down_sum)
                if graph_config['positive_plot'] == False and graph_config['negative_plot'] == True:
                    plt.plot(energy, dos_down_sum*(-1), color = color_dict[graph_config['Color_list'][index]], linewidth=graph_config['line_width'], label = 'Total DOS({})'.format(orbital))
                    data_list_down=data_collection(data_list_down, is_save, graph_config, energy, dos_down_sum)
                
            else:
                energy, dos_up, dos_down = split_dos_parser(str(DOS_temp.split('_')[0]), dos_object_list[int(DOS_temp.split('_')[0])-1], DOS_temp, orbital_list)
                if graph_config['positive_plot'] == True:
                    plt.plot(energy, dos_up, color = color_dict[graph_config['Color_list'][index]], linewidth=graph_config['line_width'], label = name_list[index])
                    data_list_up=data_collection(data_list_up, is_save, graph_config, energy, dos_up)
                if graph_config['positive_plot'] == True and graph_config['negative_plot'] == True:
                    plt.plot(energy, dos_down, color = color_dict[graph_config['Color_list'][index]], linewidth=graph_config['line_width'])
                    data_list_down=data_collection(data_list_down, is_save, graph_config, energy, dos_down)
                if graph_config['positive_plot'] == False and graph_config['negative_plot'] == True:
                    plt.plot(energy, dos_down*(-1), color = color_dict[graph_config['Color_list'][index]], linewidth=graph_config['line_width'], label = name_list[index])
                    data_list_down=data_collection(data_list_down, is_save, graph_config, energy, dos_down)
            
        elif isinstance(DOS_temp, list) == True:
            dos_up_sum = 0
            dos_down_sum = 0
            for element_index, element in enumerate(DOS_temp):
                energy, dos_up, dos_down = split_dos_parser(str(element.split('_')[0]), dos_object_list[int(element.split('_')[0])-1], element, orbital_list)
                if element_index == 0:
                    dos_up_sum = dos_up
                    dos_down_sum = dos_down
                else:
                    dos_up_sum += dos_up
                    dos_down_sum += dos_down
                    
            if graph_config['positive_plot'] == True:
                plt.plot(energy, dos_up_sum, color = color_dict[graph_config['Color_list'][index]], linewidth=graph_config['line_width'], label = name_list[index])
                data_list_up=data_collection(data_list_up, is_save, graph_config, energy, dos_up_sum)
            if graph_config['positive_plot'] == True and graph_config['negative_plot'] == True:
                plt.plot(energy, dos_down_sum, color = color_dict[graph_config['Color_list'][index]], linewidth=graph_config['line_width'])
                data_list_down=data_collection(data_list_down, is_save, graph_config, energy, dos_down_sum)
            if graph_config['positive_plot'] == False and graph_config['negative_plot'] == True:
                plt.plot(energy, dos_down_sum*(-1), color = color_dict[graph_config['Color_list'][index]], linewidth=graph_config['line_width'], label = name_list[index])
                data_list_down=data_collection(data_list_down, is_save, graph_config, energy, dos_down_sum)
            
    plt.title('DOS', fontsize=graph_config['title_fontsize'])
    plt.xlabel('Energy(eV)', fontsize=graph_config['axis_label_fontsize'])
    plt.ylabel('DOS', fontsize=graph_config['axis_label_fontsize'])
    plt.xticks(fontsize=graph_config['ticks_fontsize'])
    plt.yticks(fontsize=graph_config['ticks_fontsize'])
    plt.legend(fontsize=graph_config['legend_fontsize'])
    
    if graph_config['xlim'] == None:
        current_xlim = plt.xlim()
        graph_config['xlim']=[current_xlim[0], current_xlim[1]]
        
    else:
        plt.xlim([graph_config['xlim'][0], graph_config['xlim'][1]])
        
    if graph_config['ylim'] == None:
        current_ylim = plt.ylim()
        graph_config['ylim']=[current_ylim[0], current_ylim[1]]
        
    else:
        plt.ylim([graph_config['ylim'][0], graph_config['ylim'][1]])
    
    if is_save == True:
        plt.savefig('DOS.'+graph_config['save_format'], dpi=graph_config['save_dpi'])
        table_name_list = get_current_DOS(DOS_list, Labellist, graph_config)
        table_name_list.insert(0, 'Energy')
        dos_data_up = np.array(np.array(data_list_up).T)
        dos_data_down = np.array(data_list_down).T
        
        if len(data_list_up) != 0:
            up_df=pd.DataFrame(dos_data_up, columns=table_name_list)
            up_df.to_csv("Up_DOS_Data.csv", sep='\t', index=False)
            print('Up_DOS_Data.csv is saved!')
        if len(data_list_down) != 0:
            down_df=pd.DataFrame(dos_data_down, columns=table_name_list)
            down_df.to_csv("Down_DOS_Data.csv", sep='\t', index=False)
            print('Down_DOS_Data.csv is saved!')
        
    plt.show()

    
    return graph_config
    
def Add_Atom_DOS(DOS_list, Labellist, coordi):
    Coordi_dict=Coord_to_dict(Labellist, coordi)
    Selected_atoms=[]
    while True:
        Input_Work=input('Atom의 Index를 선택하세요(선택이 모두 끝났으면 q 입력) : ')
        if Input_Work == 'q':
            break
        elif Input_Work.isdigit() == True:
            Selected_atoms.append(Input_Work+'_all')
        else:
            print('다시 입력해주세요')
    
    if len(Selected_atoms) != 0:
        print('-------------------------------------------------------------------------------')
        print('1 : 이 atom들을 별개로 그리기')
        print('2 : 이 atom들의 기여분을 합쳐서 그리기')
        print('-------------------------------------------------------------------------------')
        print('(방금 작업에서 1개만 추가했으면, 그냥 엔터를 누르세요.)')
        Input_Work2=input('기여분을 어떻게 처리할지 선택하세요. (default : 1) : ')
        
        if Input_Work2 != '2':
            for s in Selected_atoms:
                DOS_list.append(s)
        else:
            DOS_list.append(Selected_atoms)
        return DOS_list
    
    else:
        return DOS_list
    
def Projected_DOS(DOS_list, orbital_list, Labellist, graph_config):
    print_current_DOS(DOS_list, Labellist, graph_config)
    group_select = input('Projection 시킬 DOS를 선택하세요 (index 입력) : ')
    
    if group_select == 'q':
        return DOS_list

    elif group_select.isdigit() == True:
        group_select = int(group_select)
        group_select = group_select - 1
    
    else:
        print('다시 입력해주세요')
        
    if isinstance(DOS_list[group_select], list) == False:                           
        if DOS_list[group_select] == 'Total DOS_all':
            user_orbital_list = Get_User_Projection_Orbital_list(orbital_list)
            issum=input('얘네를 합칠까요? (합치기(1)/별개로 두기(2[default])): ')
            for u in user_orbital_list:
                DOS_list.append('Total DOS_'+u)
                
            return DOS_list
            
        else:
            user_orbital_list = Get_User_Projection_Orbital_list(orbital_list)
            if len(user_orbital_list) == 1:
                DOS_list[group_select] = DOS_list[group_select].split('_')[0]+'_'+user_orbital_list[0]
                return DOS_list

            elif len(user_orbital_list) > 1:
                issum=input('얘네를 합칠까요? (합치기(1)/별개로 두기(2[default])): ')
                if issum == '1':
                    total_save = DOS_list
                    new_DOS_list = []
                    for i, t in enumerate(total_save):
                        if i == group_select:
                            new_DOS_list.append([total_save[group_select].split('_')[0]+'_'+u for u in user_orbital_list])
                        else:
                            new_DOS_list.append(t)
                            
                    return new_DOS_list
                            
                else:
                    total_save = DOS_list
                    new_DOS_list = []
                    for i, t in enumerate(total_save):
                        if i == group_select:
                            for u in user_orbital_list:
                                new_DOS_list.append(total_save[group_select].split('_')[0]+'_'+u)
                        else:
                            new_DOS_list.append(t)
                    return new_DOS_list
                        
    
    elif isinstance(DOS_list[group_select], list) == True:
        print('--------------------------------------------------------------------------------------------------------------------')
        for index, elem in enumerate(DOS_list[group_select]):
            print('{} : {}'.format(index+1, Labellist[int(elem.split('_')[0])-1]))
        print('--------------------------------------------------------------------------------------------------------------------')
        individual_select = input('묶어진 DOS네요. 이 중 어떤 원자에 대한 Projection을 진행할까요? (index 입력) (얘네 모두 : all) : ')
        user_orbital_list = Get_User_Projection_Orbital_list(orbital_list)
        
        if individual_select == 'all':
            if len(user_orbital_list) == 1:
                new_group=[]
                group_save = DOS_list[group_select]
                for i, individual_temp in enumerate(DOS_list[group_select]):
                    print(individual_temp)
                    new_group.append(group_save[i].split('_')[0]+'_'+user_orbital_list[0])
                DOS_list[group_select] = new_group
                return DOS_list
            
            elif len(user_orbital_list) > 1:
                new_DOS_list = []
                group_save = DOS_list[group_select]
                new_group = []
                for i, g in enumerate(group_save):
                    for u in user_orbital_list:
                        new_group.append(group_save[i].split('_')[0]+'_'+u)
                
                for i, group_temp in enumerate(DOS_list):
                    if i == group_select:
                        new_DOS_list.append(new_group)
                    else:
                        new_DOS_list.append(group_temp)
                        
                return new_DOS_list
            
        elif individual_select.isdigit() == True:
            individual_select=int(individual_select)-1
            
        if len(user_orbital_list) == 1:
            group_save = DOS_list[group_select]
            DOS_list[group_select][individual_select] = group_save[individual_select].split('_')[0]+'_'+user_orbital_list[0]
            
            return DOS_list
            
        elif len(user_orbital_list) > 1:
            new_DOS_list = []
            group_save = DOS_list[group_select]
            new_group = []
            for i, g in enumerate(group_save):
                if i == individual_select:
                    for u in user_orbital_list:
                        new_group.append(group_save[individual_select].split('_')[0]+'_'+u)
                else:
                    new_group.append(g)
            
            for i, group_temp in enumerate(DOS_list):
                if i == group_select:
                    new_DOS_list.append(new_group)
                else:
                    new_DOS_list.append(group_temp)
            
            return new_DOS_list
        
def Remove_DOS(DOS_list, Labellist, graph_config):
    print_current_DOS(DOS_list, Labellist, graph_config)
    group_index = input('어떤 DOS를 삭제하시겠습니까? (index 입력) : ')
    if isinstance(DOS_list[int(group_index)-1], list) == False:
        individual_index = 'all'
    else:
        for index, element in enumerate(DOS_list[int(group_index)-1]):
            print('{} : {}'.format(index+1, element))
        individual_index = input('묶어진 DOS입니다. 어떤 요소를 삭제하시겠습니까? (index 입력) (묶음 전체 삭제 : all) : ')
    
    new_DOS_list = []
    for index, DOS_temp in enumerate(DOS_list):
        if index == int(group_index)-1:
            if individual_index == 'all':
                pass
            else:
                new_group=[g for i, g in enumerate(DOS_list[index]) if i != int(individual_index)-1]
                new_DOS_list.append(new_group)
        else:
            new_DOS_list.append(DOS_list[index])
        
    return new_DOS_list

def color_selection(DOS_list, Labellist, graph_config, color_dict):
    color_list=list(color_dict.keys())
    Color_list_save = graph_config['Color_list']
    while True:
        print_current_DOS(DOS_list, Labellist, graph_config)
        print('모든 설정이 끝나면 q를 누르세요.')
        dos_choice = input('어떤 DOS의 색깔을 바꾸시겠습니까 ? (번호 입력) (뒤로 가기 : q) : ')
        if dos_choice.isdigit() == True:
            python_color_list()
            color_choice = input('색깔 번호를 적어주세요 : ')
            if color_choice.isdigit() == True:
                Color_list_save.append(Color_list_save[int(dos_choice)-1])
                Color_list_save.remove(color_list[int(color_choice)])
                Color_list_save[int(dos_choice)-1] = color_list[int(color_choice)]
                graph_config['Color_list'] = Color_list_save
                #graph_config['Color_list'][int(dos_choice)]=color_list[int(color_choice)]
            else:
                print('잘못 입력했습니다.')
                
        elif dos_choice == 'q':
            return graph_config
        else:
            print('DOS 선택을 다시 해주세요')
            
    
    
def graph_editor(DOS_list, Labellist, graph_config, color_dict):
    key_list=list(graph_config.keys())
    print('===========================================[Graph Configuration]==================================================')
    for index, key in enumerate(key_list):
        if key == 'Color_list':
            print('{:<5} : {:<30} -- {}'.format(index+1, key, graph_config[key][:len(DOS_list)]))
        else:
            print ('{:<5} : {:<30} -- {}'.format(index+1, key, graph_config[key]))
    print('==================================================================================================================')
    while True:
        graph_index_input = input('어떤 것을 수정하시겠습니까? (index 입력 , q: 뒤로가기) : ')
        if graph_index_input == 'q':
            break
        elif graph_index_input.isdigit() == False:
            print('다시 입력해주세요')
            
        elif key_list[int(graph_index_input)-1] == 'Color_list':
            graph_config = color_selection(DOS_list, Labellist, graph_config, color_dict)
            return graph_config
        
        elif key_list[int(graph_index_input)-1] == 'positive_plot' or key_list[int(graph_index_input)-1] == 'negative_plot':
            graph_value_input = input('True(1, default) or False(2) : ')
            if graph_value_input == '2':
                graph_config[key_list[int(graph_index_input)-1]] = False
            else:
                graph_config[key_list[int(graph_index_input)-1]] = True
            return graph_config
            
        else:
            graph_value_input = input('새로운 값을 입력하세요. (리스트 형태는 "[]"로 묶어 리스트로 입력, 숫자는 그냥 숫자로 입력): ')
            if graph_value_input[0] == '[':
                graph_value=graph_value_input.replace('[','').replace(']','').split(',')
                if key_list[int(graph_index_input)-1] != 'Color_list' or key_list[int(graph_index_input)-1] != 'legend_name_list':
                    graph_value=[float(g) for g in graph_value]
                graph_config[key_list[int(graph_index_input)-1]] = graph_value
                return graph_config
            else:
                try:
                    graph_value=float(graph_value_input)
                    graph_config[key_list[int(graph_index_input)-1]] = graph_value
                    return graph_config
                except:
                    print('다시 입력하세요')
            
    return graph_config

def change_sign(graph_config, dos_object_total_dos):
    while True:
        user_choice=input('양수만 plot(1) / 음수만 plot(2) / 원래대로(3) (뒤로가기 : q) : ')
        if user_choice == 'q':
            return graph_config
        if user_choice == '1':
            graph_config['positive_plot'] = True
            graph_config['negative_plot'] = False
            if graph_config['ylim'] == None:
                graph_config['ylim'] = [0, max(dos_object_total_dos[1])+max(dos_object_total_dos[1])*0.02]
            else:
                graph_config['ylim'] = [0, graph_config['ylim'][1]]
            return graph_config
        elif user_choice == '2':
            graph_config['positive_plot'] = False
            graph_config['negative_plot'] = True
            if graph_config['ylim'] == None:
                graph_config['ylim'] = [0, max(dos_object_total_dos[2])+max(dos_object_total_dos[2])*0.02]
            else:
                graph_config['ylim'] = [0, graph_config['ylim'][0]*(-1)]
            return graph_config
        elif user_choice == '3':
            graph_config['positive_plot'] = True
            graph_config['negative_plot'] = True
            graph_config['ylim'] = None
            return graph_config
        else:
            print('다시 입력해주세요')
            
def main():
    Direct, linenumber_dc, linenumber_Lattice_Parameter, linenumber_Atom_Name, linenumber_Atom_Number, lattice_parameters, Atom_Name, Atom_Count, coordinates = ImportCONTCAR()
    LP, coordi, Separated_List, Labellist = DataRefine_Mainfunction(lattice_parameters, Atom_Name, Atom_Count, coordinates, Direct)
    Coordi_dict=Coord_to_dict(Labellist, coordi)
    color_dict = get_color_list()

    Default_Color_list = ['gray', 'red', 'blue', 'green', 'darkorange', 'magenta', 'lightcoral', 'khaki', 'forestgreen', 'darkslategray', 
                        'slategrey', 'navy', 'darkorchid', 'lightpink', 'darkgoldenrod', 'chartreuse', 'aqua', 'lightblue', 
                        'midnightblue', 'violet', 'darkred', 'coral', 'seagreen', 'paleturquoise', 'dodgerblue', 'cornflowerblue', 
                        'purple', 'pink', 'moccasin', 'lightgreen', 'darkcyan', 'powderblue', 'mediumblue', 'slateblue', 'crimson', 
                        'tan', 'mediumspringgreen', 'aquamarine', 'slategray', 'darkblue', 'indigo', 'indianred', 'darkkhaki', 'darkolivegreen', 
                        'turquoise', 'skyblue', 'royalblue', 'blueviolet', 'brown', 'blanchedalmond', 'mediumseagreen', 'darkslategrey', 'cadetblue', 
                        'hotpink', 'palevioletred', 'navajowhite', 'darkseagreen', 'mediumturquoise', 'deepskyblue', 'thistle', 'firebrick', 'chocolate', 
                        'lawngreen', 'teal', 'lightskyblue', 'mediumslateblue', 'maroon', 'goldenrod', 'limegreen', 'cyan', 'lightslategrey', 'mediumpurple', 
                        'rosybrown', 'saddlebrown', 'olivedrab', 'lightseagreen', 'lightsteelblue', 'deeppink', 'darksalmon', 'olive', 'darkturquoise', 
                        'steelblue', 'plum', 'gold', 'yellowgreen', 'mediumaquamarine', 'lightslategray', 'mediumvioletred', 'peachpuff', 'lime', 'orchid', 
                        'orangered', 'springgreen', 'darkviolet', 'papayawhip', 'yellow', 'darkslateblue', 'lemonchiffon', 'palegreen', 'darkmagenta', 
                        'antiquewhite', 'greenyellow', 'rebeccapurple', 'orange', 'mediumorchid', 'burlywood', 'palegoldenrod', 'cornsilk', 'sienna', 
                        'peru', 'wheat', 'lightsalmon', 'bisque', 'salmon', 'tomato', 'sandybrown']

    Color_list = Default_Color_list
    is_save = False
    DOS_list = ['Total DOS_all']
    legend_name_list=['Total DOS(all)']

    graph_config = {'figuresize' : [8, 6],
                    'axis_label_fontsize' : 13,
                    'legend_fontsize' : 13,
                    'ticks_fontsize' : 13,
                    'title_fontsize' : 13,
                    'Color_list' : Color_list,
                    'legend_name_list' : legend_name_list,
                    'line_width' : 1,
                    'xlim' : None,
                    'ylim' : None,
                    'positive_plot' : True,
                    'negative_plot' : True,
                    'save_format' : 'pdf',
                    'save_dpi' : 200
                }

    StartMessage()
    print('                         DOG version 1.0 : 현재는 ISPIN = 2 계산만 지원됩니다.              ')
    print()
    print('============================= Reading DOSCAR (Start) ======================================')
    print('                                          ...                                              ')
    if path.exists("DOSCAR") == False:
        print('DOSCAR 파일을 찾을 수 없습니다.')
        exit()
        
    if path.exists("PROCAR") == False:
        print('PROCAR 파일을 찾을 수 없습니다.')
        exit()

    dos_object_total_dos, dos_object_list, orbital_list = Make_DOS_Dataframe()
    print('============================= Reading DOSCAR (Finish)======================================')
    print()
        
    while True:
        #print('현재 출력되는 DOS 리스트 : | color')
        print_current_DOS(DOS_list, Labellist, graph_config)
        print('하고싶은 작업이 무엇인가? (Exit : q or qq)')
        print('==================================================================================================================')
        print('1 : Atom DOS 추가')
        print('2 : DOS Projection 시키기')
        print('3 : 특정 DOS 제거')
        print('4 : 그래프 스타일 수정')
        print('5 : 양수/음수 부분만 나타내기')
        print('==================================================================================================================')
        Input_Work=input('선택 : ')
        print('-'*80)

        if Input_Work == 'q':
            user_is_save=input('현재까지 그린 DOS를 저장하시겠습니까? (1 : yes / 2 : no(default) : ')
            if user_is_save == '1':
                is_save = True
            else:
                is_save = False
            DOSplot(DOS_list, Color_list, Labellist, graph_config, color_dict, dos_object_total_dos, dos_object_list, orbital_list, is_save)
            break
        elif Input_Work == '1':
            DOS_list = Add_Atom_DOS(DOS_list, Labellist, coordi)
        elif Input_Work == '2':
            DOS_list = Projected_DOS(DOS_list, orbital_list, Labellist, graph_config)
        elif Input_Work == '3':
            DOS_list = Remove_DOS(DOS_list, Labellist, graph_config)
        elif Input_Work == '4':
            graph_config = graph_editor(DOS_list, Labellist, graph_config, color_dict)
        elif Input_Work == '5':
            graph_config = change_sign(graph_config, dos_object_total_dos)
        
        graph_config = DOSplot(DOS_list, Color_list, Labellist, graph_config, color_dict, dos_object_total_dos, dos_object_list, orbital_list, is_save)

if __name__ == "__main__":
    main()
