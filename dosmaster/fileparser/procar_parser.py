def PROCAR_Parser(file):
    file_data = open(file, 'r')
    file_data=file_data.readlines()
    orbital_list=file_data[7].split()
    orbital_list.remove('ion')
    orbital_list.remove('tot')
    
    return orbital_list