from dosmaster.subplotter.dosplot_manager import get_current_DOS, split_dos_parser, data_collection, Get_DOS_Label
import pandas as pd
import numpy as np

def Axis_Optimization(data_dict, graph_config):  
    print('Y - Axis will be Optimized.')
    graph_config['ylim_optimization'] = True
    
    DOS_list = data_dict['DOS_list']
    Labellist = data_dict['Labellist']
    color_dict = data_dict['color_dict']
    dos_object_total_dos = data_dict['dos_object_total_dos']
    dos_object_list = data_dict['dos_object_list']
    orbital_list = data_dict['orbital_list']
    is_save = data_dict['is_save']
    is_save_optimization = True
    
    graph_config['legend_name'] = Get_DOS_Label(DOS_list, Labellist, graph_config)

    Total_DOS=False
    data_list_up=[]
    data_list_down=[]
    for index, DOS_temp in enumerate(DOS_list):
        if isinstance(DOS_temp, list) == False:
            if DOS_temp=='Total DOS_all':
                Total_DOS = True
                energy, dos_up, dos_down=split_dos_parser('total', dos_object_total_dos, DOS_temp, orbital_list)
                if graph_config['positive_plot'] == True:
                    data_list_up=data_collection(data_list_up, is_save_optimization, graph_config, energy, dos_up)
                if graph_config['positive_plot'] == True and graph_config['negative_plot'] == True:
                    data_list_down=data_collection(data_list_down, is_save_optimization, graph_config, energy, dos_down)
                if graph_config['positive_plot'] == False and graph_config['negative_plot'] == True:
                    data_list_down=data_collection(data_list_down, is_save_optimization, graph_config, energy, dos_down)

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
                    data_list_up=data_collection(data_list_up, is_save_optimization, graph_config, energy, dos_up_sum)
                if graph_config['positive_plot'] == True and graph_config['negative_plot'] == True:
                    data_list_down=data_collection(data_list_down, is_save_optimization, graph_config, energy, dos_down_sum)
                if graph_config['positive_plot'] == False and graph_config['negative_plot'] == True:
                    data_list_down=data_collection(data_list_down, is_save_optimization, graph_config, energy, dos_down_sum)
                
            else:
                energy, dos_up, dos_down = split_dos_parser(str(DOS_temp.split('_')[0]), dos_object_list[int(DOS_temp.split('_')[0])-1], DOS_temp, orbital_list)
                if graph_config['positive_plot'] == True:
                    data_list_up=data_collection(data_list_up, is_save_optimization, graph_config, energy, dos_up)
                if graph_config['positive_plot'] == True and graph_config['negative_plot'] == True:
                    data_list_down=data_collection(data_list_down, is_save_optimization, graph_config, energy, dos_down)
                if graph_config['positive_plot'] == False and graph_config['negative_plot'] == True:
                    data_list_down=data_collection(data_list_down, is_save_optimization, graph_config, energy, dos_down)
            
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
                    
            try:
                if DOS_temp[0].split('_')[2] == 'avg':
                    dos_up_sum = dos_up_sum/len(DOS_temp)
                    dos_down_sum = dos_down_sum/len(DOS_temp)
            except:
                pass
                    
            if graph_config['positive_plot'] == True:
                data_list_up=data_collection(data_list_up, is_save_optimization, graph_config, energy, dos_up_sum)
            if graph_config['positive_plot'] == True and graph_config['negative_plot'] == True:
                data_list_down=data_collection(data_list_down, is_save_optimization, graph_config, energy, dos_down_sum)
            if graph_config['positive_plot'] == False and graph_config['negative_plot'] == True:
                data_list_down=data_collection(data_list_down, is_save_optimization, graph_config, energy, dos_down_sum)
    
    if is_save_optimization == True:
        
        data_list_up = data_list_up[1:]
        data_list_down  = data_list_down[1:]
        
        np_data_list_up = np.array(data_list_up)
        np_data_list_down = np.array(data_list_down)
        
        max_value = np.amax(np_data_list_up)
        min_value = np.amin(np_data_list_down)
        
        max_value=max(max_value, abs(min_value))
        min_value=-max_value
        
        ylim_min = min_value + min_value*0.1
        ylim_max = max_value + max_value*0.1
        graph_config['ylim'] = [ylim_min, ylim_max]
    
    return graph_config
