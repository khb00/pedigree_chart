# pedigree_chart

This code was designed to generate and display a 'Game of Thrones' type family tree.

Download all and open pedigree_chart_main.py. Choose which functions to execute to get desired output.

If you wish to run anything in regards to databases, you will have to have mysql installed. Edit the establish_connection function in pedigree_chart_sql.py and add your host name, username and password.

When using the print_info function, a person and their family is printed in this format: 

- Novius Coleyer 21 49
 - Partner: Panne Bronzedall 25 70
 - Kids:
   - Mais Coleyer 48 126

where Novius Coleyer is the original person, born in the year 21 and died in the year 49. He had one partner called Panne Bronzedall, born in 25 and died in 70. Their child is Mais Coleyer, born in 48 and died in 126.

If you wish to display the graph in graphviz, you can print the instructions to do so using the using the print_instructions function in pedigree_chart_display_py. Then input it into graphviz, which can either be installed or is available online.
