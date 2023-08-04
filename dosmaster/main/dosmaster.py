#!/usr/bin/env python
#======================================================================================================
#Script Name : dosmaster Program(ver.1.7.13)
#Made by Youngjun Park (yjpark29@postech.ac.kr)
#Inspired by Jaesun Kim
#Edit Date : 23/08/02
#======================================================================================================
#Description : DOS Plot Smartly in Terminal Environment
#======================================================================================================
#: 1) Add Atom DOS
#: 2) DOS Projection
#: 3) Sum DOS
#: 4) Average DOS
#: 5) Remove DOS
#: 6) Plot only Positive/Negative part
#: 7) Edit Graph Style
#: 8) Axis Optimization

# Future Update (ver.1.8.0)
#: 9) ISPIN=1 Support (Not Implemented)
#: 10) Group Projection for Same Orbital (Not Implemented)
#======================================================================================================

import matplotlib.pyplot as plt
from colorama import Fore, Back, Style

from dosmaster.main import __version__


from dosmaster.fileparser.doscar_split import *
from dosmaster.fileparser.procar_parser import *

from dosmaster.subplotter.dosplot_manager import *

from dosmaster.base.printer import print_current_DOS
from dosmaster.base.data_generation import make_data_dict, list_to_string_name, Dos_Color_Update
from dosmaster.mainplotter.dosplot import DOSplot

from dosmaster.features.a_add_atom_dos import Add_Atom_DOS
from dosmaster.features.b_dos_projection import Projected_DOS
from dosmaster.features.c_dos_sum import DOS_Sum
from dosmaster.features.d_avergae_dos import Average_DOS
from dosmaster.features.e_remove_dos import Remove_DOS
from dosmaster.features.f_change_sign import Change_Sign
from dosmaster.features.g_graph_editor import Graph_Editor
from dosmaster.features.h_axis_optimization import Axis_Optimization



def StartMessage():
    print("#############################################################################################")
    print("###################                                                   #######################")
    print("###################                      DOSMaster                    #######################")
    print("###################                                                   #######################")
    print("###################                          version : {:5}          #######################".format(__version__))
    print("###################                                                   #######################")
    print("###################                                2023.08.02         #######################")
    print("###################                        yjpark29@postech.ac.kr     #######################")
    print("###################                          Young-jun Park(CNMD)     #######################")
    print("###################                                                   #######################")
    print("#############################################################################################")
            
def main():
    print(Style.RESET_ALL)

    data_dict = make_data_dict()
    graph_config = {'figuresize' : [8, 6],
                    'axis_label_fontsize' : 13,
                    'legend_fontsize' : 13,
                    'ticks_fontsize' : 13,
                    'title_fontsize' : 13,
                    'legend_name' : data_dict['legend_name_list'],
                    'legend_location' : 'best',
                    'bbox_to_anchor' : None,
                    'line_width' : 1,
                    'xlim' : None,
                    'ylim' : None,
                    'positive_plot' : True,
                    'negative_plot' : True,
                    'save_filename' : 'DOS',
                    'save_format' : 'pdf',
                    'save_dpi' : 200,
                    'dos_color' : {list_to_string_name(data_dict['DOS_list'][0]) : {'color':'gray', 'User_Edit':None}},
                    'ylim_optimization' : False,
                    }
        
    StartMessage()
            
    while True:
        # Main Loop
        print_current_DOS(data_dict['DOS_list'], data_dict['Labellist'], graph_config)
        print('What would you like to do? (Exit : q or qq)')
        print('==================================================================================================================')
        print('1 : Add Atom DOS')
        print('2 : Project DOS')
        print('3 : Sum DOS')
        print('4 : Average DOS')
        print('5 : Remove specific DOS')
        print('6 : Show only positive/negative part')
        print('7 : Edit graph style')
        print('8 : ylim optimization')
        print('==================================================================================================================')
        Input_Work=input('Choice : ')
        print('-'*80)

        # User Selection
        if Input_Work == 'q':
            user_is_save=input('o you want to save the currently drawn DOS? (1 : yes / 2 : no(default) : ')
            if user_is_save == '1':
                data_dict['is_save'] = True
            else:
                data_dict['is_save'] = False
            DOSplot(data_dict, graph_config)
            break
        elif Input_Work == '1':
            data_dict['DOS_list'], graph_config = Add_Atom_DOS(data_dict, graph_config)
        elif Input_Work == '2':
            data_dict['DOS_list'], graph_config = Projected_DOS(data_dict, graph_config)
        elif Input_Work == '3':
            data_dict['DOS_list'], graph_config = DOS_Sum(data_dict, graph_config)
        elif Input_Work == '4':
            data_dict['DOS_list'], graph_config = Average_DOS(data_dict, graph_config)
        elif Input_Work == '5':
            data_dict['DOS_list'], graph_config = Remove_DOS(data_dict, graph_config)
        elif Input_Work == '6':
            graph_config = Change_Sign(data_dict, graph_config)
        elif Input_Work == '7':
            graph_config = Graph_Editor(data_dict, graph_config)
        elif Input_Work == '8':
            graph_config = Axis_Optimization(data_dict, graph_config)
        
        # Modified DOS Plot
        graph_config = Dos_Color_Update(data_dict, graph_config)
        graph_config = DOSplot(data_dict, graph_config)

if __name__ == "__main__":
    main()
