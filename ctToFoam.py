def header(var,fieldType, dim):
    line1 = '/*--------------------------------*- C++ -*----------------------------------*\\\n'
    line2 = '| =========                 |                                                 |\n'
    line3 = '| \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |\n'
    line4 = '|  \\\\    /   O peration     | Version:  5                                     |\n'
    line5 = '|   \\\\  /    A nd           | Web:      www.OpenFOAM.org                      |\n'
    line6 = '|    \\\\/     M anipulation  |                                                 |\n'
    line7 = '\*---------------------------------------------------------------------------*/\n'
    line8 = 'FoamFile\n'
    line9 = '{\n'
    line10= '    version     2.0;\n'
    line11= '    format      ascii;\n'
    line12= '    class       {};\n'.format(fieldType)
    line13= '    location    "0";\n'
    line14= '    object      {};\n'.format(var)
    line15= '}\n'
    line16= '// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n'
    line17= '\n'
    line18='dimensions      {};\n'.format(dim)
    line19= '\n'
    line20= 'internalField   nonuniform List<{}>'.format('scalar' if fieldType == 'volScalarField' else 'vector')

    return ([line1+line2+line3+line4+line5+line6+line7+line8+line9+line10+line11+line12+line13+line14+line15+line16+line17+line18+line19+line20])

def internal_data(var, internal): #internal for internal data
    DataStart = '{:d}\n('.format(len(internal))
    Data   = []
    Data.append(DataStart)

    if var == 'U':
        for item in internal:
            Data.append('(' + str(item) + ' 0 0)')  
    else:
        for item in internal:
            Data.append(str(item)) 

    DataEnd = ')\n;\n'
    Data.append(DataEnd)
    return (Data)

def boundary_data(var, fieldType, boundary): #boundary for boundary data
    """
    DataStart = 'boundaryField\n{}\n    wall\n    {}\n        type            empty;\n        value           nonuniform List<{}>\n{:d}\n('.format('{', '{', 'scalar' if fieldType == 'volScalarField' else 'vector', len(BD))
    Data   = []
    Data.append(DataStart)
    for item in BD:
        Data.append(str(item))        
    DataEnd = ');\n    {}'.format('}')
    Data.append(DataEnd)
    """

    if var == 'U':
        DataStart = 'boundaryField\n{}\n    inlet\n    {}\n        type            fixedValue;\n        value           uniform ({} 0 0);\n    {}'.format('{', '{', boundary, '}')
    else:
        DataStart = 'boundaryField\n{}\n    inlet\n    {}\n        type            fixedValue;\n        value           uniform {};\n    {}'.format('{', '{', boundary, '}')
    Data   = []
    Data.append(DataStart)

    Data2 = '    wall\n    {\n        type            empty;\n    }\n'
    Data3 = '    outlet\n    {\n        type            zeroGradient;\n    }\n}\n\n\n// ************************************************************************* //'

    Data.append(Data2)
    Data.append(Data3)
    return (Data)

    ##########################################################
if __name__ == '__main__':

    import cantera as ct
    import numpy as np
    import pandas as pd
    import os

    ##########################################################
    flame_dir = './cantera_save.csv'
    os.makedirs('0', exist_ok=True)

    p   = 101325 #inert into dataframe if not exported from cantera
    gas = ct.Solution("./mechanism/jws-kin_therm.cti") # methonal mechanism for test

    species_names  = [name for name in gas.species_names]
    list_to_0 = ['U'] + ['T'] + ['p'] + species_names

    ID   = pd.read_csv(flame_dir) # ID = internal data
    ID.insert(2, 'p', np.repeat(p, len(ID))) #inert pressure with value = P, length = length of data

    #replace old cantera name with name in 0 folder
    #data_col = ID.columns #get data columns
    ID.rename(columns = {'velocity':'U'}, inplace = True) # replace velocity to U
    ID.rename(columns = {'u (m/s)':'U'} , inplace = True)
    ID.rename(columns = {'grid':'z'}    , inplace = True) # replace grid to z
    ID.rename(columns = {'T (K)':'T'}   , inplace = True)
    #

    BD   = ID.iloc[0] #BD = boundary data at row 0

    for idx2_, var in enumerate(list_to_0):
        if var == 'U':
            fieldType = 'volVectorField'
            dimension = '[0 1 -1 0 0 0 0]'
        else:
            fieldType = 'volScalarField'
            dimension = '[0 0 0 0 0 0 0]'
            if var  == 'T':
                dimension = '[0 0 0 1 0 0 0]'
            elif var == 'p':
                dimension = '[1 -1 -2 0 0 0 0]'
                   
        print ('Converting....')
        print ('    {}, dimension = {}'.format(var.replace('X_', ''), dimension))
        boundary = BD[var] #boundary = boundary data
        internal = ID[var] #internal = internal data

        txt  = header(var.replace('X_', ''), fieldType, dimension) + internal_data(var, internal) + boundary_data(var.replace('X_', ''), fieldType, boundary)
        np.savetxt( './0/{}'.format(var.replace('X_', '')),  txt, fmt="%s")
    print ('Done conversion!')
