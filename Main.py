###############################################################################
#                   DECLARATION
# == Class ==

from Tools.IO import IOMethod;
from Tools.Parser import ParserMethod;
from Tools.Analysis import AnalysisMethod;
from copy import deepcopy;

# == Variables == 
# Constants
c = 2.99792458*(10**10);
pi = 3.14159265359;

# List of input files
input_file = ['E:\\Programs\\Cygwin\\home\\Admin\\Duo\\IO\\dan.inp'];
read_path_list = [
    'E:\\Programs\\Cygwin\\home\\Admin\\Duo\\IO\\m.out',
    'E:\\Programs\\Cygwin\\home\\Admin\\Duo\\IO\\m_star.out'
    ];

# Path to output file
write_path = 'E:\\Programs\\Cygwin\\home\\Admin\\Duo\\IO\\analysis_out.txt';

# Input file information index [index, mass 1, mass 2]
input_file_index = {0 : ['m', 600.00, 600.00],
                    1 : ['m_star', 600.30, 600.30]
                    };

# IO routine variables
section_divider = '================================================================='
level = 2; # Specify energy level to display transitions (start level 1)
file_select_1 = 0;
file_select_2 = 1;
level_i = 0; # Initial energy level to specify transition
level_f = 1; # Final energy level to specify transition
maxima_number = 50; # Number of max omega values to be obtained

# == Functions ==

def FileRead(read_path_list, key_1, key_2, target_column) :
    """
    Function pulls values from different DUO output files which correspond to 
    different values of mass.
    
    Arguments:
        read_path_list: List of addresses to different DUO .out files (list)
        key_1, key_2: keys to delimit extraction section in file
        target_column: specify column to extract from section
        
    Return: List
    """
    
    # -- Initialize master list
    
    output_list = [0 for i in range(0, len(read_path_list))];
        
    # -- Parse input file
    
    for i in range(0, len(read_path_list)) :
        dummy = IOMethod()
        duo_input = dummy.InMethod(read_path_list[i]);
    
        dummy = ParserMethod();
        parsed_duo_input = dummy.Parse(duo_input, key_1, key_2);

        # -- Extract energy values

        column = dummy.ColumnExtract(parsed_duo_input, target_column);
        # Values stored as strings. Convert to floating point values next
        for j in range(0, len(column)) :
            column[j] = float(column[j]);
        
        # -- Store energy values of a particular file to master list
        output_list[i] = column;
    
    return output_list;
    

def AllTransitionsCalc(energy_list) :
    """
    Calculates all transitions between all energy levels disregarding selection
    rules. Values stored in n x n symmetric matricies.
    
    Arguments: 
        <energies> refers to list of energies for calculation. Sets of separate
        energy levels can be dealt with by nesting lists (list)
        
    Return: List
    """
    
    limit = len(energy_list[0]);
    transition_list = [[[0 for i in range(0, limit)] for j in range(0, limit)]
                        for k in range(0, len(energy_list))];
    
    # Initializes 2D array to hold transition magnitude values

    for i in range(0, len(transition_list)) :
        for j in range(0, limit) :
            for k in range(j, limit):
                transition_list[i][j][k] = energy_list[i][k] - energy_list[i][j];
                transition_list[i][k][j] = transition_list[i][j][k];
    # Above operation allows for index independent frequency value calculations
    # throughout grid. Thus one only needs to quote correct indices for energy 
    # levels and not worry about their order (i.e. indexing [i][j] and [j][i] 
    # return the same value for frequency)
    
    return transition_list


def WriteKnKappa(level_i, level_f) :
    dummy = IOMethod();
    formatter = '{:<10}{:<10}{:<30}{:<30}'; # Variable to store formatting info
    text = """
            Transitions between energy levels {0} and {1}
            """
    
    dummy.OutMethod(text.format(level_i, level_f), write_path, 
                    'append', 'no separate');
    dummy.OutMethod(formatter.format('Mass 1', 'Mass 2', 'K', 'kappa'), 
                    write_path, 'append', 'no separate');
    for i in range(1, len(K)) :
        dummy.OutMethod(formatter.format(input_file_index[i][1], 
                                         input_file_index[i][2],
                                         K[i][level_i][level_f], 
                                         kappa[i][level_i][level_f]),
                        write_path, 'append', 'no separate');
                
    dummy.OutMethod('', write_path, 'append', 'separate'); # Spacer


def FindMax(subject) :
    max_value = 0;
    max_value_info = [];
    
    for i in range(0, len(subject)) :
        for j in range(0, len(subject[i])) :
            if subject[i][j] >= max_value :
                max_value = subject[i][j];
    
    for i in range(0, len(subject)) :
        for j in range(0, len(subject[i])) :
            if subject[i][j] == max_value :
                max_value_info = max_value_info + [[max_value, i, j]];
                
    return(max_value_info);








#######################################################################################
#                    MAIN
# -- File read operations
# Pull energies
energy_master = FileRead(read_path_list, " energyStart", " energyEnd", 3);

# Pull values for parameter space
parameter_space = FileRead([read_path_list[0]], "values", "end", 2);
# Parameter space has format [[v0, r0, lambda, qm, j]]

barrier = FileRead([read_path_list[0]], " barrierStart", " barrierEnd", 5); 

# Variable declaration for potential
var_lambda = parameter_space[0][2];
var_qm = parameter_space[0][3];
var_j = parameter_space[0][4];
var_2jay = (2 * var_j) / var_lambda;
 

# -- Calculate transition magnitudes between 2 energy levels (neglect rules)
transition_master = AllTransitionsCalc(energy_master);

# Convert transitions to frequencies
omega_master = deepcopy(transition_master);

#for i in range(0, len(transition_master)) :
#    for j in range(0, len(transition_master[0])) :
#        for k in range(0, len(transition_master[0][0])) :
#            omega_master[i][j][k] = 2*pi*c*(transition_master[i][j][k]);
            

# -- Calculate changes in transition frequency magnitudes (delta omega)
#    between different input settings 
dummy = AnalysisMethod();
 
delta_omega_master = [[0 for i in range(0, len(omega_master))]
                      for j in range(0, len(omega_master))];

for i in range(0, len(delta_omega_master)) :
    for j in range(0, len(delta_omega_master[0])) :
        delta_omega_master[i][j] = dummy.TwoMatrixOperation(omega_master[i], 
                                                            omega_master[j], 
                                                            "sub");


# -- Calculate Q = (delta omega / omega) for all transitions
Q = [[0 for i in range(0, len(delta_omega_master))]
                      for j in range(0, len(delta_omega_master))];
 
for i in range(0, len(delta_omega_master)) :
    for j in range(0, len(delta_omega_master[0])) :
        Q[i][j] = dummy.TwoMatrixOperation(delta_omega_master[i][j],
                                           omega_master[i],
                                           "div");
                                         
                                
# -- Calculate K and kappa
K = [[[0 for i in range(0, len(Q[0][0]))] for j in range(0, len(Q[0][0]))] 
     for k in range(0, len(energy_master))];
kappa = [[[0 for i in range(0, len(Q[0][0]))] for j in range(0, len(Q[0][0]))]
         for k in range(0, len(energy_master))];
base_rm = (((input_file_index[0][1]) * (input_file_index[0][2])) / 
          ((input_file_index[0][1]) + (input_file_index[0][2]))); # Base reduced mass

# Calculate K         
for i in range(1, len(energy_master)) :
    for j in range(0, len(Q[0][0])) :
        for k in range(0, len(Q[0][0])) :
            rm = (((input_file_index[i][1]) * (input_file_index[i][2])) / 
                  ((input_file_index[i][1]) + (input_file_index[i][2]))); 
            # rm = Reduced mass
            K[i][j][k] = (Q[0][i][j][k]) / ((rm - base_rm) / base_rm);

# Calculate kappa
for i in range(1, len(energy_master)) :
    for j in range(0, len(Q[0][0])) :
        for k in range(0, len(Q[0][0])) :
            rm = (((input_file_index[i][1]) * (input_file_index[i][2])) / 
                  ((input_file_index[i][1]) + (input_file_index[i][2]))); 
            # rm = Reduced mass
            kappa[i][j][k] = ((delta_omega_master[0][i][j][k]) / 
                              ((rm - base_rm) / base_rm));
        
# Calculate barrier height
'''
Need to fix this (doesn't interfere with anything yet so don't need to comment out)
Subtle divide by 0 problem here and for K calculation from Q calculations but this 
is solved by setting to 0 as this is trivial and does not interfere with result
interpretation.
'''
min_coord = var_qm * ((1-((var_2jay)**2))**(1/2))
barrier_height = (((var_lambda / 4) * ((min_coord / var_qm)**2)) +
                  var_j * (1 - (1 + (var_2jay**(-2)) *
                                ((min_coord / var_qm)**2))**(0.5))
                  );


# Find maximum K
print(FindMax(K[1]));

# -- Results
'''
K and kappa calculated relative to file with default value (whatever that is).
'''
for i in range(1, len(K)) :
    print(K[i][49][1]);










# ===============================================================================
#                    IO SECTION
# -- Write to file
# Write parameter space specifications
dummy = IOMethod();

#0000000000000000000000000000000000000000000000000000000000000000000000000000000000
text = """
        Parameter space
            Lambda:            {0}
            Qm:                {1}
            J:                 {2}
            Mass sets:         {3}    {4}
            (L, R energy       {5}    {6}
            columns)
        
        Other info
            Barrier height:    {7}
        """

dummy.OutMethod(text.format(var_lambda, var_qm, var_j,
                            input_file_index[file_select_1][1],
                            input_file_index[file_select_1][2],
                            input_file_index[file_select_2][1],
                            input_file_index[file_select_2][2],
                             abs(barrier[0][0])), 
                write_path, 'overwrite', 'separate');

#0000000000000000000000000000000000000000000000000000000000000000000000000000000
# !!! Applicable warnings !!!
# Barrier deficiency warning
counter = 0;
for i in range(0, len(energy_master[file_select_1])) :
    if energy_master[file_select_1][i] <= abs(barrier[0][0]) :
        counter = counter + 1;

if counter < 5 :
    dummy.OutMethod('WARNING: LOW BARRIER (LESS THAN 5 LVLS IN WELL)', 
                    write_path, 'append', 'separate');
if counter > 10 :
    dummy.OutMethod('WARNING: HIGH BARRIER (MORE THAN 10 LVLS IN WELL)', 
                    write_path, 'append', 'separate');

#00000000000000000000000000000000000000000000000000000000000000000000000000000000
# Write energy levels and corresponding transitions to a specific energy level
# for 2 specific inputs
formatter = '{:<15}{:<40}{:<15}{:<40}'; # Variable to store formatting info
text = """
        Transitions to energy level {0}
        """

dummy.OutMethod(text.format(level), write_path, 
                'append', 'no separate'); # Level toggle at the top

dummy.OutMethod(formatter.format('Energy', 'Transition', 'Energy', 'Transition'), 
                write_path, 'append', 'no separate');
                
for i in range(0, len(energy_master[0])) :
    dummy.OutMethod(formatter.format(energy_master[file_select_1][i], 
                                     transition_master[file_select_1][level - 1][i],
                                     energy_master[file_select_2][i],
                                     transition_master[file_select_2][level - 1][i]), 
                    write_path, 
                    'append', 'no separate');

#000000000000000000000000000000000000000000000000000000000000000000000000000000
# Section divider
dummy.OutMethod('', write_path, 'append', 'separate');
dummy.OutMethod(section_divider, write_path, 'append', 'separate');

# Write K and kappa values for specified energy levels with varying mass
# '''
# K and kappa for transitions between adjacent lvls up to 15
# '''
# for i in range(0, 15) :
#     WriteKnKappa(i, i+1); 

#00000000000000000000000000000000000000000000000000000000000000000000000000000000
# # Section divider
# dummy.OutMethod('', write_path, 'append', 'separate');
# dummy.OutMethod(section_divider, write_path, 'append', 'separate');
# 
'''
K and kappa for transitions between lvl 0 and 0, 1, 2, 3, 4 
'''
for i in range(1, 6) :
    WriteKnKappa(0, i);     
 
#000000000000000000000000000000000000000000000000000000000000000000000000000000000
# # Section divider
# dummy.OutMethod('', write_path, 'append', 'separate');
# dummy.OutMethod(section_divider, write_path, 'append', 'separate');
# 
'''
K and kappa for transitions between lvl 10 and 12, 13, 14, 15 
'''
for i in range(11, 16) :
    WriteKnKappa(10, i);     

#00000000000000000000000000000000000000000000000000000000000000000000000000000000000        
'''
# Display n maximum delta omega values and their corresponding conditions
text = '{0} largest delta omega values'

dummy.OutMethod(text.format(maxima_number), write_path, 'append', 'separate')

formatter = '{:<40}{:<40}';

for i in range(0, len(max_value_master_delta_omega)) :
    dummy.OutMethod(formatter.format(max_value_master_delta_omega[i][0], 
                                     max_value_master_delta_omega[i][1]),
                    write_path, 'append', 'no separate');

dummy.OutMethod('', write_path, 'append', 'separate'); # Spacer

# Display n maximum Q values and their corresponding conditions
text = '{0} largest [delta omega / omega] values (referred herein as Q)'

dummy.OutMethod(text.format(maxima_number), write_path, 'append', 'separate')

formatter = '{:<40}{:<40}';

for i in range(0, len(max_value_master_Q)) :
    dummy.OutMethod(formatter.format(max_value_master_Q[i][0], 
                                     max_value_master_Q[i][1]),
                    write_path, 'append', 'no separate');

'''
