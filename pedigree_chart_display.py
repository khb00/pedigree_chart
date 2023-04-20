"""
#Display information about the tree or how to graph it.
"""

def show_info(fam_dict):
    """
    Print out family information in text.
    Partner and their shared children are also printed in relation to their partner/relative.

    Args:
        fam_dict (dict): A dictionary of Descendant objects.

    Returns:
        None
    """

    print('\nDISPLAY FAMILY TREE')
    for person in fam_dict.values():
        if len(fam_dict) == 1:
            # If only one person in the tree, print their info.
            print('\n')
            print_info(person)
        if len(person.marriages) != 0 :
            # Only display person if they have been married.
            # Their partner and children are displayed in relation to them.
            print('\n')
            print_info(person) # Print the personal information.
            for couple in person.marriages:
                # For every relationship person has, display partner.
                partner = couple.partner2
                print(' Partner: ', end="")
                print_info(partner)
                if len(couple.kids) > 0:
                    # Display all shared kids.
                    print(' Kids:')
                    for kid in couple.kids:
                        print('  ', end="")
                        print_info(kid)


def print_info(person):
    """
    Print out individual's name, surname, birth date, and death date.
    
    Args:
    person (Descendant): The individual whose information will be printed.
    
    Returns:
    None
    """
    print(person.name, person.house, person.birth, person.death)


def print_person(person):
    """
    Output the instructions to display an individual's box in the graph.
    
    Args:
    person (Descendant): The individual whose information will be displayed.
    
    Returns:
    None
    """
    # Define the color of the box according to the gender
    if person.gender == 0:
        colour = 'azure2'  # blue for male
    else:
        colour = 'bisque'  # pink for female
    # Output the details necessary to display the box.
    # The displayed information is their name, year of birth, and year of death.
    print(person.label,
          '[label="',
          person.name,
          person.house,
          r'\n',
          person.birth,
          ' † ',
          person.death,
          '",style=filled,fillcolor=',
          colour,'];')



def print_list(fam_dict):
    """
    Cycle through all the people in the dictionary and their partners,
    to print their box information.

    Args:
    fam_dict (dict): a dictionary containing Person objects, with unique IDs as keys.
    """
    for person in fam_dict.values():
        print_person(person) # Print the individual box information.
        #If this person has been married, print information about their partners.
        if len(person.marriages) > 0 :
            # Cycle through all their relationships.
            for marriage in person.marriages:
                print_person(marriage.partner2)


def print_marriage_connections(couple, i):
    """
    Print out the graphviz instructions for the relationship connections.

    Args:
    couple (Couple): a couple object containing information about a couple's relationship.
    i (int): a unique identifier for this relationship connection.
    """
    husband = couple.partner1
    wife = couple.partner2
    kids = couple.kids
    marriage_label = str('h'+str(i)) # Each connection must have its own ID that starts with 'h'.
    # Print the instructions.
    # If they are of the same gen, i.e. partners, they will be on the same level in the graph.
    print('{ rank=same;')
    print( husband.label, '  -> ', marriage_label, ' -> ', wife.label ,';')
    print( marriage_label,'[shape=circle,label="",height=0.01,width=0.01];}')
    if len(kids) > 0 :
        print('{ rank=same;')
        # For all the kids born from this relationship
        for j in range(0, len(kids)):
            # Every child is identified by the connectionID and the number of children before them.
            kid_label = marriage_label + ('_')+ str(j)
            print(kid_label, end='')
            # If this is the last kid, print,
            if j+1 == len(kids):
                print(';')
            # If there are more kids to be added,
            else:
                print('->',end='')
        # For every child of this relationship
        for j in range(0, len(kids)):
            kid_label = marriage_label + ('_')+ str(j)
            # Print the instructions for each child
            print(kid_label,end='')
            print('[shape=circle,label="",height=0.01,width=0.01];')
        print('}')
        pos = round(len(kids)/2) # Parents are positioned at halfway between all their children.
        print(marriage_label, ' -> ', marriage_label + ('_') + str(0), ';')
        # For every child:
        for j in range(0, len(kids)):
            # This is the IDspecific to graphviz instructions.
            kid_label = marriage_label + ('_')+ str(j)
            # This relates the graphviz ID to their dictionary ID.
            print(kid_label, ' -> ', kids[j].label , ';')


def print_all_marriage(fam_dict, i):
    """
    Prints connections between married couples and their children.

    Parameters:
    fam_dict (dict): A dictionary containing information about individuals and their relationships.
    i (int): An integer that is used for connection ID.

    Returns:
    None
    """
    for person in fam_dict.values():
        # If a person has been married,
        # print the connetions between them, their partner and children.
        if len(person.marriages) > 0 :
            for marriage in person.marriages:
                print_marriage_connections(marriage, i) # Print individual marriage connections.
                i = i + 1 # Increment i, which will be used for the connection ID.


def print_instructions(fam_dict):
    """
    Prints instructions for generating a family tree on Graphviz.

    Parameters:
    fam_dict (dict): A dictionary containing information about individuals and their relationships.

    Returns:
    None
    """
    # I recommend using an online Graphviz application.
    print('\n\nPRINTING GRAPHVIZ INSTRUCTIONS')
    print('\n\ndigraph {')
    print('node [shape=box];')
    print('edge [dir=none];')
    print_list(fam_dict) # The individual  box information about each person must be printed first.
    i=0
    print_all_marriage(fam_dict, i) # The instructions about each person is printed. connection
    print('{ rank=same;}')
    print('}')
