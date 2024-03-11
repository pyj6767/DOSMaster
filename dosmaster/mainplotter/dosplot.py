import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

from dosmaster.subplotter.dosplot_manager import get_current_DOS, split_dos_parser, data_collection, Get_DOS_Label, Get_DOS_Legend_User
from dosmaster.base.data_generation import list_to_string_name

def DOSplot(data_dict, graph_config):
    DOS_list = data_dict['DOS_list']
    Labellist = data_dict['Labellist']
    color_dict = data_dict['color_dict']
    dos_object_total_dos = data_dict['dos_object_total_dos']
    dos_object_list = data_dict['dos_object_list']
    orbital_list = data_dict['orbital_list']
    is_save = data_dict['is_save']
    
    graph_config['legend_name'] = Get_DOS_Label(DOS_list, Labellist, graph_config)
    graph_config = Get_DOS_Legend_User(graph_config)

    plt.figure(figsize=(graph_config['figuresize'][0],graph_config['figuresize'][1]))
    Total_DOS=False
    data_list_up=[]
    data_list_down=[]
    for index, DOS_temp in enumerate(DOS_list):
        if isinstance(DOS_temp, list) == False:
            if DOS_temp=='Total DOS_all':
                Total_DOS = True
                energy_save, dos_up, dos_down=split_dos_parser('total', dos_object_total_dos, DOS_temp, orbital_list)
                energy = graph_config['shift_x_axis'] + np.array(energy_save)
                if graph_config['positive_plot'] == True:
                    plt.plot(energy, dos_up, color = color_dict[graph_config['dos_color'][list_to_string_name(DOS_temp)]['color']], 
                             linewidth=graph_config['line_width'], label=graph_config['legend_name'][index])
                    data_list_up=data_collection(data_list_up, is_save, graph_config, energy, dos_up)
                if graph_config['positive_plot'] == True and graph_config['negative_plot'] == True:
                    plt.plot(energy, dos_down, color = color_dict[graph_config['dos_color'][list_to_string_name(DOS_temp)]['color']], 
                             linewidth=graph_config['line_width'])
                    data_list_down=data_collection(data_list_down, is_save, graph_config, energy, dos_down)
                if graph_config['positive_plot'] == False and graph_config['negative_plot'] == True:
                    plt.plot(energy, dos_down*(-1), color = color_dict[graph_config['dos_color'][list_to_string_name(DOS_temp)]['color']], 
                             linewidth=graph_config['line_width'], label=graph_config['legend_name'][index])
                    data_list_down=data_collection(data_list_down, is_save, graph_config, energy, dos_down)

            elif DOS_temp.split('_')[0] == 'Total DOS' and DOS_temp.split('_')[1] != 'all':
                orbital=DOS_temp.split('_')[1]
                dos_up_sum = 0
                dos_down_sum = 0
                for label_index, label in enumerate(Labellist):
                    energy_save, dos_up, dos_down = split_dos_parser(str(label_index+1), dos_object_list[label_index], str(label_index+1)+'_'+str(orbital), orbital_list)
                    energy = graph_config['shift_x_axis'] + np.array(energy_save)
                    if index == 0:
                        dos_up_sum = dos_up
                        dos_down_sum = dos_down
                    else:
                        dos_up_sum += dos_up
                        dos_down_sum += dos_down
                        
                if graph_config['positive_plot'] == True:
                    plt.plot(energy, dos_up_sum, color = color_dict[graph_config['dos_color'][list_to_string_name(DOS_temp)]['color']], 
                             linewidth=graph_config['line_width'], label = graph_config['legend_name'][index])
                    data_list_up=data_collection(data_list_up, is_save, graph_config, energy, dos_up_sum)
                if graph_config['positive_plot'] == True and graph_config['negative_plot'] == True:
                    plt.plot(energy, dos_down_sum, color = color_dict[graph_config['dos_color'][list_to_string_name(DOS_temp)]['color']], 
                             linewidth=graph_config['line_width'])
                    data_list_down=data_collection(data_list_down, is_save, graph_config, energy, dos_down_sum)
                if graph_config['positive_plot'] == False and graph_config['negative_plot'] == True:
                    plt.plot(energy, dos_down_sum*(-1), color = color_dict[graph_config['dos_color'][list_to_string_name(DOS_temp)]['color']], 
                             linewidth=graph_config['line_width'], label = graph_config['legend_name'][index])
                    data_list_down=data_collection(data_list_down, is_save, graph_config, energy, dos_down_sum)
                
            else:
                energy_save, dos_up, dos_down = split_dos_parser(str(DOS_temp.split('_')[0]), dos_object_list[int(DOS_temp.split('_')[0])-1], DOS_temp, orbital_list)
                energy = graph_config['shift_x_axis'] + np.array(energy_save)
                if graph_config['positive_plot'] == True:
                    plt.plot(energy, dos_up, color = color_dict[graph_config['dos_color'][list_to_string_name(DOS_temp)]['color']], 
                             linewidth=graph_config['line_width'], label = graph_config['legend_name'][index])
                    data_list_up=data_collection(data_list_up, is_save, graph_config, energy, dos_up)
                if graph_config['positive_plot'] == True and graph_config['negative_plot'] == True:
                    plt.plot(energy, dos_down, color = color_dict[graph_config['dos_color'][list_to_string_name(DOS_temp)]['color']], 
                             linewidth=graph_config['line_width'])
                    data_list_down=data_collection(data_list_down, is_save, graph_config, energy, dos_down)
                if graph_config['positive_plot'] == False and graph_config['negative_plot'] == True:
                    plt.plot(energy, dos_down*(-1), color = color_dict[graph_config['dos_color'][list_to_string_name(DOS_temp)]['color']], 
                             linewidth=graph_config['line_width'], label = graph_config['legend_name'][index])
                    data_list_down=data_collection(data_list_down, is_save, graph_config, energy, dos_down)
            
        elif isinstance(DOS_temp, list) == True:
            dos_up_sum = 0
            dos_down_sum = 0
            for element_index, element in enumerate(DOS_temp):
                if element.split('_')[0] == 'Total DOS' and element.split('_')[1] != 'all':
                    orbital=element.split('_')[1]
                    for label_index, label in enumerate(Labellist):
                        energy_save, dos_up, dos_down = split_dos_parser(str(label_index+1), dos_object_list[label_index], str(label_index+1)+'_'+str(orbital), orbital_list)
                        
                        energy = graph_config['shift_x_axis'] + np.array(energy_save)
                        if index == 0:
                            dos_up_sum = dos_up
                            dos_down_sum = dos_down
                        else:
                            dos_up_sum += dos_up
                            dos_down_sum += dos_down
                else:
                    energy_save, dos_up, dos_down = split_dos_parser(str(element.split('_')[0]), dos_object_list[int(element.split('_')[0])-1], element, orbital_list)
                    # print(DOS_temp)
                    # print(dos_up)
                    energy = graph_config['shift_x_axis'] + np.array(energy_save)
                    if element_index == 0:
                        dos_up_sum = dos_up
                        dos_down_sum = dos_down
                    else:
                        dos_up_sum += dos_up
                        dos_down_sum += dos_down
                    
            try:
                if DOS_temp[0].split('_')[2] == 'avg':
                    dos_up_sum = dos_up_sum/len(DOS_temp)
                    dos_down_sum = dos_down_sum/len(DOS_temp)
            except:
                pass
                    
            if graph_config['positive_plot'] == True:
                plt.plot(energy, dos_up_sum, color = color_dict[graph_config['dos_color'][list_to_string_name(DOS_temp)]['color']], 
                         linewidth=graph_config['line_width'], label = graph_config['legend_name'][index])
                data_list_up=data_collection(data_list_up, is_save, graph_config, energy, dos_up_sum)
            if graph_config['positive_plot'] == True and graph_config['negative_plot'] == True:
                plt.plot(energy, dos_down_sum, color = color_dict[graph_config['dos_color'][list_to_string_name(DOS_temp)]['color']], 
                         linewidth=graph_config['line_width'])
                data_list_down=data_collection(data_list_down, is_save, graph_config, energy, dos_down_sum)
            if graph_config['positive_plot'] == False and graph_config['negative_plot'] == True:
                plt.plot(energy, dos_down_sum*(-1), color = color_dict[graph_config['dos_color'][list_to_string_name(DOS_temp)]['color']], 
                         linewidth=graph_config['line_width'], label = graph_config['legend_name'][index])
                data_list_down=data_collection(data_list_down, is_save, graph_config, energy, dos_down_sum)
            
    plt.title('DOS', fontsize=graph_config['title_fontsize'])
    plt.xlabel('Energy(eV)', fontsize=graph_config['axis_label_fontsize'])
    plt.ylabel('DOS', fontsize=graph_config['axis_label_fontsize'])
    plt.xticks(fontsize=graph_config['ticks_fontsize'])
    plt.yticks(fontsize=graph_config['ticks_fontsize'])
    if graph_config['legend_display'] == True:
        plt.legend(fontsize=graph_config['legend_fontsize'], bbox_to_anchor=graph_config['bbox_to_anchor'], loc=graph_config['legend_location'])
    else:
        pass
    if graph_config['bbox_to_anchor'] != None:
        plt.tight_layout()
    
    if graph_config['xlim'] == None:
        current_xlim = plt.xlim()
        graph_config['xlim']=[float(current_xlim[0]), float(current_xlim[1])]
        
    else:
        plt.xlim([graph_config['xlim'][0], graph_config['xlim'][1]])
        
    if graph_config['ylim'] == None:
        current_ylim = plt.ylim()
        graph_config['ylim']=[float(current_ylim[0]), float(current_ylim[1])]
        
    else:
        plt.ylim([graph_config['ylim'][0], graph_config['ylim'][1]])
    
    if is_save == True:
        plt.savefig(graph_config['save_filename']+'.'+graph_config['save_format'], dpi=graph_config['save_dpi'])
        table_name_list = get_current_DOS(DOS_list, Labellist, graph_config)
        table_name_list.insert(0, 'Energy')
        dos_data_up = np.array(np.array(data_list_up).T)
        dos_data_down = np.array(data_list_down).T
        
        if len(data_list_up) != 0:
            up_df=pd.DataFrame(dos_data_up, columns=table_name_list)
            number = 1
            file_name = './Up_DOS_Data_{}.csv'.format(number)
            while os.path.exists(file_name) == True:
                if os.path.exists(file_name):
                    number += 1
                    file_name = './Up_DOS_Data_{}.csv'.format(number)
                else:
                    break
            up_df.to_csv(file_name, sep='\t', index=False)
            print('{} is saved!'.format(file_name))
        if len(data_list_down) != 0:
            down_df=pd.DataFrame(dos_data_down, columns=table_name_list)
            number = 1
            file_name = './Down_DOS_Data_{}.csv'.format(number)
            while os.path.exists(file_name) == True:
                if os.path.exists(file_name):
                    number += 1
                    file_name = './Down_DOS_Data_{}.csv'.format(number)
                else:
                    break
            down_df.to_csv(file_name, sep='\t', index=False)
            print('{} is saved!'.format(file_name))
        
    plt.show()

    
    return graph_config