"""
This file generates the tree and new generations, from a dictionary fortmat.
"""

from random import randint
from pedigree_chart_classes import Descendant


def make_initial_tree(start_year):
    """
    Generates a person with no ancestors to start the tree.

    Args:
        start_year (int): The birth year of the person to create as the root of the tree.

    Returns:
        Dict: A dictionary representing the initial family tree with the root node.
    """

    # Print a message to indicate that we're making the initial tree.
    print('\nMAKING INITIAL TREE')

    # Create a new person with no ancestors using the Descendant class.
    # Randomly determine the gender of the person using randint(0, 1),
    # where 0 represents male and 1 represents female.
    # Set [0,0,0] to show person has no defined surname and no parentsID,
    # as well as setting sexuality as straight to increase chance of having children.
    # Set the position of child produced in relationship as None,
    # as person is not created from any relationship.
    ancestor = Descendant(start_year, randint(0, 1), [0, 0, True], None)

    # Create a new dictionary to represent the family tree and add the root node to it.
    fam_dict = {ancestor.label: ancestor}

    # Return the dictionary representing the initial family tree.
    return fam_dict


def expand_tree(fam_dict, max_gen):
    """
    Generates new generations to add to the family tree.

    Args:
        Dict (dict): A dictionary representing the current family tree.
        max_gen (int): The maximum number of generations to generate.

    Returns:
        dict: A dictionary representing the updated family tree.
    """
    # Print a message to indicate that we're expanding the family tree.
    print('\nEXPANDING FAMILY TREE')

    # Split the dictionary into two groups: married and unmarried people.
    [old_dict, new_dict] = split_dict(fam_dict)

    # Set the minimum age for legal marriage and the minimum age for illegitimate relationships.
    marriage_age = 18
    romance_age = 16

    # Iterate through each generation, creating marriages and generating children.
    for _ in range(0, max_gen):
        # Print a message indicating that we're starting a new generation.
        print('\nNew Gen!')

        # Create a new dictionary to store the children generated in this generation.
        kid_dict = {}

        # For each unmarried person, generate marriages and potential children.
        for person in new_dict.values():

            # Generate legitimate marriages for the person if they are old enough.
            Descendant.generate_legit_marriage(person, marriage_age)

            # Generate illegitimate marriages for the person if they are old enough.
            Descendant.generate_illegit_marriage(person, romance_age)

            # For each new child, add to the kid_dict.
            for couple in person.marriages:
                for child in couple.kids:
                    kid_dict[child.label] = child

        # Add the newly-weds to the married dictionary.
        old_dict = old_dict|new_dict

        # Print the number of unmarried people in the previous generation and the new generation.
        print('Previous Unmarried Pop:',len(new_dict))

        new_dict = kid_dict
        print('Current Unmarried Pop:',len(new_dict))

    # Combine the old and new dictionaries to create the final family tree.
    fam_dict = old_dict|new_dict

    # Return the updated family tree.
    return fam_dict



def split_dict(fam_dict):
    """
    Splits the input dictionary into two new dictionaries,
    One for married people and one for unmarried people.

    Args:
        fam_dict (dict): A dictionary representing the current family tree.

    Returns:
        old_dict (dict): A dictionary of married individuals.
        new_dict (dict): A dictionary of unmarried individuals.
    """

    new_dict = {}  # Dictionary to store unmarried people
    old_dict = {}  # Dictionary to store married people

    # Loop through each key in the input dictionary and check if the person has any marriages.
    for key in fam_dict:
        person = fam_dict[key]

        # If the person has no marriages, add them to the new_dict for unmarried people.
        if len(person.marriages) == 0:
            new_dict[key] = person
        else:
            # Otherwise, add them to the old_dict for married people.
            old_dict[key] = person

    # Return a list with two dictionaries, one for married and one for unmarried people.
    return [old_dict, new_dict]
