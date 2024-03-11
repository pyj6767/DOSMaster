import numpy as np

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
    
def split_dos_parser(atom_number, dataframe_object, element, orbital_list):
    #print(dataframe_object)
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
    
def Check_Legend_Name_Changed(graph_config, name, index):
    try:
        if graph_config['legend_name_user'][index] == True:
            return graph_config['legend_name'][index]
        else:
            return name
    except:
        return name
            
def Get_DOS_Label(DOS_list, Labellist, graph_config):
    name_list = []
    for index, element in enumerate(DOS_list):
        if isinstance(element, list) == False:
            if element.split('_')[0] == 'Total DOS':
                if element.split('_')[1] == 'all':
                    name = element.split('_')[0] + '(' + element.split('_')[1] + ')'
                else:
                    name = 'Total DOS' + '(' + element.split('_')[1] + ')'
            else:
                name = Labellist[int(element.split('_')[0])-1] + '(' + element.split('_')[1] + ')'
                    
            
        else:
            #get net_list and net_orbital_list
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
                    if net == 'Total DOS':
                        name += net
                    else:
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
                    if net == 'Total DOS':
                        name += net
                    else:
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

                
        if '_avg' in element[0]:
            name = 'avg[' + name + ']'

        name=Check_Legend_Name_Changed(graph_config, name, index)
                    
        name_list.append(name)
    
    return name_list

def Get_DOS_Legend_User(graph_config):
    new_legend_name_user = []
    for i in range(len(graph_config['legend_name'])):
        try:
            if graph_config['legend_name_user'][i] == True:
                new_legend_name_user.append(True)
            else:
                new_legend_name_user.append(False)
        
        except:
            new_legend_name_user.append(False)

    graph_config['legend_name_user'] = new_legend_name_user
    return graph_config

def data_collection(data_list, is_save, graph_config, energy, dos_data):
    if is_save == True:
        if len(data_list) == 0:
            data_list.append(energy)
            data_list.append(dos_data)
        else:
            data_list.append(dos_data)
    return data_list