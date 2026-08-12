from colorama import Fore, Back, Style

from dosmaster.base.printer import print_orbital_list, print_current_DOS

def Get_User_Projection_Orbital_list(orbital_list):
    print_orbital_list(orbital_list)
    print('-------------------------------------------------------------------------------------------')
    print(Style.BRIGHT + Fore.RED)
    print('This is not a number input method.')
    print('Input Method 1 : Select the orbital to project one by one. (ex : px)')
    print('Input Method 2 : Select multiple orbitals at once. (ex : s p => [s + px + py + pz])')
    print(Style.RESET_ALL)
    print("If you input 's p', it generates [s, (px+py+pz)].")
    print("If you input 'd', it generates [(dxy+dyz+dz2+dxz+x2-y2)].")
    print('-------------------------------------------------------------------------------------------')
    orbital_select = input('Please select the Orbitals to project (ex : s py pz or s p) (exit : q) : ')
    if orbital_select == 'q':
        return 'q'
    user_orbital_list = orbital_select.split()
    
    return user_orbital_list
    
def Projected_DOS(data_dict, graph_config):
    DOS_list = data_dict['DOS_list']
    orbital_list = data_dict['orbital_list']
    Labellist = data_dict['Labellist']
    
    print_current_DOS(DOS_list, Labellist, graph_config)
    group_select = input('Please select the DOS for projection (enter index) : ')

    if group_select == 'q':
        return DOS_list, graph_config

    elif group_select.isdigit() == True:
        group_select = int(group_select)
        group_select = group_select - 1

    else:
        print('Please enter again.')
        return DOS_list, graph_config
    
    if isinstance(DOS_list[group_select], list) == False:
        if DOS_list[group_select] == 'Total DOS_all':
            user_orbital_list = Get_User_Projection_Orbital_list(orbital_list)
            if user_orbital_list == 'q':
                return DOS_list, graph_config
            issum=input('Should these be combined? (Combine(1)/Keep separate(2[default])): ')
            if issum == '1':
                new_DOS_group = []
                for u in (user_orbital_list):
                    new_DOS_group.append('Total DOS_'+u)
                DOS_list.insert(group_select+1, new_DOS_group)
                
            else:
                for u in reversed(user_orbital_list):
                    DOS_list.insert(group_select+1, 'Total DOS_'+u)

            return DOS_list, graph_config
            
        else:
            user_orbital_list = Get_User_Projection_Orbital_list(orbital_list)
            if user_orbital_list == 'q':
                return DOS_list, graph_config
            if len(user_orbital_list) == 1:
                old_dos=input('Do you want to keep your old DOS? (Yes(1[default])/No(2)): ')
                if old_dos == '2':
                    graph_config['legend_name'] = [i for j, i in enumerate(graph_config['legend_name']) if j != group_select]
                    graph_config['legend_name_user'] = [i for j, i in enumerate(graph_config['legend_name_user']) if j != group_select]
                    
                if old_dos == '2':
                    DOS_list[group_select] = DOS_list[group_select].split('_')[0]+'_'+user_orbital_list[0]
                else:
                    DOS_list.insert(group_select+1, DOS_list[group_select].split('_')[0]+'_'+user_orbital_list[0])
                return DOS_list, graph_config

            elif len(user_orbital_list) > 1:
                issum=input('Should these be combined? (Combine(1)/Keep separate(2[default])): ')
                old_dos=input('Do you want to keep your old DOS? (Yes(1[default])/No(2)): ')
                if issum == '1':
                    total_save = DOS_list
                    new_DOS_list = []
                    for i, t in enumerate(total_save):
                        if i == group_select:
                            if old_dos == '2':
                                graph_config['legend_name'] = [i for j, i in enumerate(graph_config['legend_name']) if j != group_select]
                                graph_config['legend_name_user'] = [i for j, i in enumerate(graph_config['legend_name_user']) if j != group_select]
                            if old_dos == '2':
                                new_DOS_list.append([total_save[group_select].split('_')[0]+'_'+u for u in user_orbital_list])
                            else:
                                new_DOS_list.append(t)
                                new_DOS_list.append([total_save[group_select].split('_')[0]+'_'+u for u in user_orbital_list])
                        else:
                            new_DOS_list.append(t)
                            
                    return new_DOS_list, graph_config
                            
                else:
                    total_save = DOS_list
                    new_DOS_list = []
                    for i, t in enumerate(total_save):
                        if i == group_select:
                            if old_dos == '2':
                                for u in user_orbital_list:
                                    new_DOS_list.append(total_save[group_select].split('_')[0]+'_'+u)
                            else:
                                new_DOS_list.append(t)
                                for u in user_orbital_list:
                                    new_DOS_list.append(total_save[group_select].split('_')[0]+'_'+u)
                        else:
                            new_DOS_list.append(t)
                    return new_DOS_list, graph_config
                        
    
    elif isinstance(DOS_list[group_select], list) == True:
        print('--------------------------------------------------------------------------------------------------------------------')
        for index, elem in enumerate(DOS_list[group_select]):
            print('{} : {}'.format(index+1, Labellist[int(elem.split('_')[0])-1]))
        print('--------------------------------------------------------------------------------------------------------------------')
        individual_select = input('It is a bound DOS. Which atom do you want to project on? (Enter index) (All : all) : ')
        if individual_select == 'q':
            return DOS_list, graph_config
        user_orbital_list = Get_User_Projection_Orbital_list(orbital_list)
        if user_orbital_list == 'q':
            return DOS_list, graph_config
        
        if individual_select == 'all':
            if len(user_orbital_list) == 1:
                new_group=[]
                group_save = DOS_list[group_select]
                for i, individual_temp in enumerate(DOS_list[group_select]):
                    new_group.append(group_save[i].split('_')[0]+'_'+user_orbital_list[0])
                
                if 'old_dos' in locals():
                    if old_dos == '2':
                        DOS_list[group_select] = new_group
                    else:
                        DOS_list.insert(group_select+1, new_group)
                else:
                    DOS_list.insert(group_select+1, new_group)
                
                return DOS_list, graph_config
            
            elif len(user_orbital_list) > 1:
                issum=input('Should these be combined? (Combine(1)/Keep separate(2[default])): ')
                old_dos=input('Do you want to keep your old DOS? (Yes(1[default])/No(2)): ')
                if issum == '1':
                    new_DOS_list = []
                    group_save = DOS_list[group_select]
                    new_group = []
                    for i, g in enumerate(group_save):
                        for u in user_orbital_list:
                            new_group.append(group_save[i].split('_')[0]+'_'+u)

                    for i, group_temp in enumerate(DOS_list):
                        if i == group_select:
                            if 'old_dos' in locals():
                                if old_dos == '2':
                                    new_DOS_list.append(new_group)
                                else:
                                    new_DOS_list.append(group_save)
                                    new_DOS_list.append(new_group)
                            else:
                                new_DOS_list.append(group_save)
                                new_DOS_list.append(new_group)
                        else:
                            new_DOS_list.append(group_temp)

                else:
                    new_DOS_list = []
                    group_save = DOS_list[group_select]
                    new_group = []
                    for u in user_orbital_list:
                        new_group_temp = []
                        for i, g in enumerate(group_save):
                            new_group_temp.append(group_save[i].split('_')[0]+'_'+u)
                        new_group.append(new_group_temp)
                
                    for i, group_temp in enumerate(DOS_list):
                        if i == group_select:
                            if 'old_dos' in locals():
                                if old_dos == '2':
                                    for ng in new_group:
                                        new_DOS_list.append(ng)
                                else:
                                    new_DOS_list.append(group_save)
                                    for ng in new_group:
                                        new_DOS_list.append(ng)
                            else:
                                new_DOS_list.append(group_save)
                                for ng in new_group:
                                        new_DOS_list.append(ng)
                        else:
                            new_DOS_list.append(group_temp)
                        
                return new_DOS_list, graph_config
            
        elif individual_select.isdigit() == True:
            individual_select=int(individual_select)-1

        else:
            print('Enter again.')

        old_dos=input('Do you want to keep your old DOS? (Yes(1[default])/No(2)): ')
        if old_dos == '2':
            graph_config['legend_name'] = [i for j, i in enumerate(graph_config['legend_name']) if j != group_select]
            graph_config['legend_name_user'] = [i for j, i in enumerate(graph_config['legend_name_user']) if j != group_select]
            
        if len(user_orbital_list) == 1:
            group_save = DOS_list[group_select]
            if old_dos == '2':
                DOS_list[group_select][individual_select] = group_save[individual_select].split('_')[0]+'_'+user_orbital_list[0]
            else:
                group_save[individual_select] = group_save[individual_select].split('_')[0]+'_'+user_orbital_list[0]
                DOS_list.insert(group_select+1, group_save)
            
            return DOS_list, graph_config
            
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
                    if old_dos == '2':
                        new_DOS_list.append(new_group)
                    else:
                        new_DOS_list.append(group_save)
                        new_DOS_list.append(new_group)
                else:
                    new_DOS_list.append(group_temp)
            
            return new_DOS_list, graph_config
