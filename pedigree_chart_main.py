
"""
# This code was designed to generate and display a 'Game of Thrones' type family tree.
# All names used in this project were taken from https://blog.reedsy.com/character-name-generator/
"""

import pedigree_chart_display
import pedigree_chart_expand_tree
import pedigree_chart_csv
import pedigree_chart_sql
import pedigree_chart_web

fam_dict = {} #Family is contained in this dictionary


#Comment and uncomment the functions you want to execute.

# Generate starting person.
#fam_dict = pedigree_chart_expand_tree.make_initial_tree(0) # Argument is the beginning year.

# Read and put family from csv into a dictionary format.
#pedigree_chart_csv.read_csv('pedigree_chart_test_file.csv', fam_dict) #Example csv can be found in folder.

# Expand family tree.
# Second argument is how many generations to add.
#fam_dict = pedigree_chart_expand_tree.expand_tree(fam_dict, 2)

# Print current family tree data as text.
#pedigree_chart_display.show_info(fam_dict)

# Write data from dictionary into csv.
#pedigree_chart_csv.make_csv('pedigree_chart_test_file.csv', fam_dict)

# Print instructions to be inputted into Graphviz to display family tree.
#pedigree_chart_display.print_instructions(fam_dict)

# Generate a database in mySQL, resetting the previous database.
# You will have to add your own host, username and password to this code to get it to work.
#pedigree_chart_sql.make_database(fam_dict)

# Generate a webpage with all the data in a table.
# You will need to have generate a database already.
#pedigree_chart_web.run_web_table()

# Find a specific person in people table.
#pedigree_chart_sql.request_person_record( 'Oda0L06' )
