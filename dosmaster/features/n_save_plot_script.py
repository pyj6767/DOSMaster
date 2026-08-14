import numpy as np
import pandas as pd
import os
import json
from colorama import Fore, Back, Style

from dosmaster.subplotter.dosplot_manager import get_current_DOS, split_dos_parser, data_collection, Get_DOS_Label, Get_DOS_Legend_User, gaussian_smearing, get_dos_divisor
from dosmaster.base.data_generation import list_to_string_name

def get_unique_filename(template, name):
    # Fill 'name' into the template. If the file already exists, append _2, _3, ...
    file_name = template.format(name)
    number = 2
    while os.path.exists(file_name) == True:
        file_name = template.format('{}_{}'.format(name, number))
        number += 1
    return file_name

def Save_Data(data_dict, graph_config, csv_name):
    DOS_list = data_dict['DOS_list']
    Labellist = data_dict['Labellist']
    dos_object_total_dos = data_dict['dos_object_total_dos']
    dos_object_list = data_dict['dos_object_list']
    orbital_list = data_dict['orbital_list']

    graph_config['legend_name'] = Get_DOS_Label(DOS_list, Labellist, graph_config)
    graph_config = Get_DOS_Legend_User(graph_config)

    data_list_up=[]
    data_list_down=[]
    for index, DOS_temp in enumerate(DOS_list):
        if isinstance(DOS_temp, list) == False:
            if DOS_temp=='Total DOS_all':
                energy_save, dos_up, dos_down=split_dos_parser('total', dos_object_total_dos, DOS_temp, orbital_list)
                energy = graph_config['shift_x_axis'] + np.array(energy_save)
                divisor = get_dos_divisor(DOS_temp, Labellist, graph_config)
                dos_up = dos_up / divisor
                dos_down = dos_down / divisor
                if graph_config['smearing'] != 0:
                    energy, dos_up, dos_down = gaussian_smearing(energy, dos_up, dos_down, graph_config['smearing'])
                if graph_config['positive_plot'] == True:
                    data_list_up=data_collection(data_list_up, True, graph_config, energy, dos_up)
                if graph_config['positive_plot'] == True and graph_config['negative_plot'] == True:
                    data_list_down=data_collection(data_list_down, True, graph_config, energy, dos_down)
                if graph_config['positive_plot'] == False and graph_config['negative_plot'] == True:
                    data_list_down=data_collection(data_list_down, True, graph_config, energy, dos_down)

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
                divisor = get_dos_divisor(DOS_temp, Labellist, graph_config)
                dos_up_sum = dos_up_sum / divisor
                dos_down_sum = dos_down_sum / divisor
                if graph_config['smearing'] != 0:
                    energy, dos_up_sum, dos_down_sum = gaussian_smearing(energy, dos_up_sum, dos_down_sum, graph_config['smearing'])
                if graph_config['positive_plot'] == True:
                    data_list_up=data_collection(data_list_up, True, graph_config, energy, dos_up_sum)
                if graph_config['positive_plot'] == True and graph_config['negative_plot'] == True:
                    data_list_down=data_collection(data_list_down, True, graph_config, energy, dos_down_sum)
                if graph_config['positive_plot'] == False and graph_config['negative_plot'] == True:
                    data_list_down=data_collection(data_list_down, True, graph_config, energy, dos_down_sum)

            else:
                energy_save, dos_up, dos_down = split_dos_parser(str(DOS_temp.split('_')[0]), dos_object_list[int(DOS_temp.split('_')[0])-1], DOS_temp, orbital_list)
                energy = graph_config['shift_x_axis'] + np.array(energy_save)
                divisor = get_dos_divisor(DOS_temp, Labellist, graph_config)
                dos_up = dos_up / divisor
                dos_down = dos_down / divisor
                if graph_config['smearing'] != 0:
                    energy, dos_up, dos_down = gaussian_smearing(energy, dos_up, dos_down, graph_config['smearing'])
                if graph_config['positive_plot'] == True:
                    data_list_up=data_collection(data_list_up, True, graph_config, energy, dos_up)
                if graph_config['positive_plot'] == True and graph_config['negative_plot'] == True:
                    data_list_down=data_collection(data_list_down, True, graph_config, energy, dos_down)
                if graph_config['positive_plot'] == False and graph_config['negative_plot'] == True:
                    data_list_down=data_collection(data_list_down, True, graph_config, energy, dos_down)

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
            divisor = get_dos_divisor(DOS_temp, Labellist, graph_config)
            dos_up_sum = dos_up_sum / divisor
            dos_down_sum = dos_down_sum / divisor
            if graph_config['smearing'] != 0:
                energy, dos_up_sum, dos_down_sum = gaussian_smearing(energy, dos_up_sum, dos_down_sum, graph_config['smearing'])
            if graph_config['positive_plot'] == True:
                data_list_up=data_collection(data_list_up, True, graph_config, energy, dos_up_sum)
            if graph_config['positive_plot'] == True and graph_config['negative_plot'] == True:
                data_list_down=data_collection(data_list_down, True, graph_config, energy, dos_down_sum)
            if graph_config['positive_plot'] == False and graph_config['negative_plot'] == True:
                data_list_down=data_collection(data_list_down, True, graph_config, energy, dos_down_sum)

    table_name_list = get_current_DOS(DOS_list, Labellist, graph_config)
    table_name_list.insert(0, 'Energy')

    up_file_name = None
    down_file_name = None

    if len(data_list_up) != 0:
        up_df=pd.DataFrame(np.array(data_list_up).T, columns=table_name_list)
        up_file_name = get_unique_filename('./dosmaster_saved_{}.csv', csv_name+'_up')
        up_df.to_csv(up_file_name, sep='\t', index=False)
        print('{} is saved!'.format(up_file_name))
    if len(data_list_down) != 0:
        down_df=pd.DataFrame(np.array(data_list_down).T, columns=table_name_list)
        down_file_name = get_unique_filename('./dosmaster_saved_{}.csv', csv_name+'_down')
        down_df.to_csv(down_file_name, sep='\t', index=False)
        print('{} is saved!'.format(down_file_name))

    return up_file_name, down_file_name

def Save_Plot_Script(data_dict, graph_config):
    DOS_list = data_dict['DOS_list']
    color_dict = data_dict['color_dict']

    # 0) Ask the user for the file names to save.
    print(Style.BRIGHT + Fore.RED)
    print('The CSV file is saved as   ./dosmaster_saved_<name>.csv')
    print('The ipynb file is saved as ./dosmaster_script_<name>.ipynb')
    print('(To go back without saving, press [q])')
    print(Style.RESET_ALL)
    csv_name = input('Enter a name for the CSV file : ')
    if csv_name == 'q':
        print('Canceled. Returning to the main screen.')
        return data_dict, graph_config
    ipynb_name = input('Enter a name for the ipynb file : ')
    if ipynb_name == 'q':
        print('Canceled. Returning to the main screen.')
        return data_dict, graph_config
    if csv_name == '':
        csv_name = 'DOS'
    if ipynb_name == '':
        ipynb_name = 'DOS'

    # 1) Save the currently drawn DOS as CSV files.
    up_file_name, down_file_name = Save_Data(data_dict, graph_config, csv_name)

    # 2) Collect the labels / colors / style exactly as they were drawn.
    labels = list(graph_config['legend_name'])
    colors = [color_dict[graph_config['dos_color'][list_to_string_name(DOS_temp)]['color']] for DOS_temp in DOS_list]

    if graph_config['legend_display'] == True:
        legend_line = "plt.legend(fontsize={}, loc={}, bbox_to_anchor={})".format(graph_config['legend_fontsize'], repr(graph_config['legend_location']), repr(graph_config['bbox_to_anchor']))
    else:
        legend_line = "# legend is hidden"

    # 3) Build a simple script that just reads the CSV files and re-draws the DOS.
    code_text = (
        "import pandas as pd\n"
        "import matplotlib.pyplot as plt\n"
        "\n"
        "# ===== DOS data & style captured from DOSMaster =====\n"
        "up_file = {up_file}\n"
        "down_file = {down_file}\n"
        "colors = {colors}\n"
        "labels = {labels}\n"
        "line_width = {line_width}\n"
        "positive_plot = {positive_plot}\n"
        "negative_plot = {negative_plot}\n"
        "figuresize = {figuresize}\n"
        "xlim = {xlim}\n"
        "ylim = {ylim}\n"
        "shading = {shading}\n"
        "\n"
        "plt.figure(figsize=(figuresize[0], figuresize[1]))\n"
        "\n"
        "# Positive (spin-up) part\n"
        "if up_file is not None:\n"
        "    up_df = pd.read_csv(up_file, sep='\\t')\n"
        "    energy = up_df[up_df.columns[0]]\n"
        "    for i, col in enumerate(up_df.columns[1:]):\n"
        "        plt.plot(energy, up_df[col], color=colors[i], linewidth=line_width, label=labels[i])\n"
        "\n"
        "# Negative (spin-down) part\n"
        "if down_file is not None:\n"
        "    down_df = pd.read_csv(down_file, sep='\\t')\n"
        "    energy = down_df[down_df.columns[0]]\n"
        "    for i, col in enumerate(down_df.columns[1:]):\n"
        "        if positive_plot == False:\n"
        "            plt.plot(energy, -down_df[col], color=colors[i], linewidth=line_width, label=labels[i])\n"
        "        else:\n"
        "            plt.plot(energy, down_df[col], color=colors[i], linewidth=line_width)\n"
        "\n"
        "# Shade the area between the x-axis and each DOS curve\n"
        "if shading:\n"
        "    ax = plt.gca()\n"
        "    for line in ax.get_lines():\n"
        "        ax.fill_between(line.get_xdata(), 0, line.get_ydata(), color=line.get_color(), alpha=0.3)\n"
        "\n"
        "plt.title('DOS', fontsize={title_fontsize})\n"
        "plt.xlabel('Energy(eV)', fontsize={axis_label_fontsize})\n"
        "plt.ylabel('DOS', fontsize={axis_label_fontsize})\n"
        "plt.xticks(fontsize={ticks_fontsize})\n"
        "plt.yticks(fontsize={ticks_fontsize})\n"
        "{legend_line}\n"
        "if xlim is not None:\n"
        "    plt.xlim(xlim[0], xlim[1])\n"
        "if ylim is not None:\n"
        "    plt.ylim(ylim[0], ylim[1])\n"
        "plt.tight_layout()\n"
        "plt.show()\n"
    ).format(up_file=repr(up_file_name),
             down_file=repr(down_file_name),
             colors=repr(colors),
             labels=repr(labels),
             line_width=graph_config['line_width'],
             positive_plot=graph_config['positive_plot'],
             negative_plot=graph_config['negative_plot'],
             figuresize=repr(list(graph_config['figuresize'])),
             xlim=repr(graph_config['xlim']),
             ylim=repr(graph_config['ylim']),
             shading=graph_config.get('shading', True),
             title_fontsize=graph_config['title_fontsize'],
             axis_label_fontsize=graph_config['axis_label_fontsize'],
             ticks_fontsize=graph_config['ticks_fontsize'],
             legend_line=legend_line)

    markdown_text = ("# DOSMaster plot reproduction\n"
                     "\n"
                     "This notebook reproduces the DOS drawn in DOSMaster from the saved CSV files.\n"
                     "Run it in the same directory as the CSV files.\n")

    # 4) Assemble the .ipynb file.
    notebook = {'cells': [{'cell_type': 'markdown',
                           'metadata': {},
                           'source': markdown_text.splitlines(keepends=True)},
                          {'cell_type': 'code',
                           'execution_count': None,
                           'metadata': {},
                           'outputs': [],
                           'source': code_text.splitlines(keepends=True)}],
                'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
                             'language_info': {'name': 'python'}},
                'nbformat': 4,
                'nbformat_minor': 5}

    notebook_file_name = get_unique_filename('./dosmaster_script_{}.ipynb', ipynb_name)

    with open(notebook_file_name, 'w') as f:
        json.dump(notebook, f, indent=1)
    print('{} is saved!'.format(notebook_file_name))

    return data_dict, graph_config
