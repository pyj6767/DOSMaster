import csv

from dosmaster.fileparser.structure_parser import ImportCONTCAR, DataRefine_Mainfunction, Coord_to_dict
from dosmaster.base.printer import Reading_Files
from dosmaster.subplotter.colortable import get_color_list
import pkg_resources

def make_data_dict():
    data_dict = {}
    structure_output = ImportCONTCAR()
    data_dict["Direct"]=structure_output[0]
    data_dict["linenumber_dc"]=structure_output[1]
    data_dict["linenumber_Lattice_Parameter"]=structure_output[2]
    data_dict["linenumber_Atom_Name"]=structure_output[3]
    data_dict["linenumber_Atom_Number"]=structure_output[4]
    data_dict["lattice_parameters"]=structure_output[5]
    data_dict["Atom_Name"]=structure_output[6]
    data_dict["Atom_Count"]=structure_output[7]
    data_dict["coordinates"]=structure_output[8]
    
    data_refine_output = DataRefine_Mainfunction(data_dict['lattice_parameters'], 
                                                 data_dict['Atom_Name'], 
                                                 data_dict['Atom_Count'], 
                                                 data_dict['coordinates'], 
                                                 data_dict['Direct'])
    data_dict['LP']=data_refine_output[0]
    data_dict['coordi']=data_refine_output[1]
    data_dict['Separated_List']=data_refine_output[2]
    data_dict['Labellist']=data_refine_output[3]
    
    data_dict['Coordi_dict']=Coord_to_dict(data_dict['Labellist'], data_dict['coordi'])
    data_dict['color_dict']=get_color_list()
        
    data_dict['is_save'] = False
    data_dict['DOS_list'] = ['Total DOS_all']
    data_dict['legend_name_list'] = ['Total DOS(all)']
    
    dos_object_total_dos, dos_object_list, orbital_list, is_spin = Reading_Files()
    
    data_dict['dos_object_total_dos'] = dos_object_total_dos
    data_dict['dos_object_list'] = dos_object_list
    data_dict['orbital_list'] = orbital_list
    data_dict['is_spin'] = is_spin
    
    return data_dict
    
def list_to_string_name(dos_element):
    if isinstance(dos_element, list) == False:
        return dos_element
    else:
        return ' and '.join(dos_element)
    
def Dos_Color_Update(data_dict, graph_config):
    DOS_list = data_dict['DOS_list']
    
    resource_path = pkg_resources.resource_filename('dosmaster', 'subplotter/colors.csv')
    with open(resource_path, 'r') as f:
        reader = csv.reader(f)
        Color_list = list(reader)[0]

    old_dos_color_list = [graph_config['dos_color'][dos_name]['color'] for dos_name in graph_config['dos_color']]
    
    # Add the dos_name that is not in graph_config['dos_color']
    data_dict_dos_name_list = [list_to_string_name(dos) for dos in DOS_list]
    old_graph_dos_name_list = [dos_name for dos_name in graph_config['dos_color']]
    for dos in DOS_list:
        dos_name=list_to_string_name(dos)
        if dos_name not in old_graph_dos_name_list:
            for c in Color_list:
                if c not in old_dos_color_list:
                    graph_config['dos_color'][dos_name]={'color':c, 'User_Edit':None}
                    old_dos_color_list.append(c)
                    break
        elif dos_name in old_graph_dos_name_list:
            pass
        
    # Remove the dos_name that is not in DOS_list 
    remove_index = [i for i, item in enumerate(old_graph_dos_name_list) if item not in data_dict_dos_name_list]
    for index in sorted(remove_index, reverse=True):
        del graph_config['dos_color'][old_graph_dos_name_list[index]]
            
    return graph_config
