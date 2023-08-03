def Change_Sign(data_dict, graph_config):
    dos_object_total_dos = data_dict['dos_object_total_dos']
    
    while True:
        user_choice=input('Only Positive plot(1) / Only Negative plot(2) / Original (3) (Back : [q]) : ')
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
            print('Enter again.')