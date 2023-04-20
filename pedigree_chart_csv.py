"""
Read and write the fam_dict to and from a csc file.
Example file is included in this project.
"""

#import classes
import csv
from pedigree_chart_classes import Couple, Descendant


def write_bio(person, writer):
    """
    Write a row of data about a person to a CSV file.

    Args:
        person (Descendant): An instance of the descendant class.
        writer (csv.writer): A csv writer instance to write to a file.

    Returns:
        None
    """
    # Determine the value for the ParentsID column based on the person's parentage.
    if isinstance(person.parents, Couple):
        parents_label = person.parents.label
    elif person.label.split(person.name)[1] == ('0'):
        parents_label = 'TRUE'
    else:
        parents_label = 'FALSE'

    # Write a row of data about the person to the CSV file.
    data = [person.label,
            person.name,
            person.house,
            person.gender,
            person.sexuality,
            person.birth,
            person.death,
            parents_label]
    writer.writerow(data)


def write_marriage(couple, writer):
    """
    Write a row of data about a marriage to a CSV file.

    Args:
        couple (Couple): An instance of the Couple class.
        writer (csv.writer): A csv writer instance to write to a file.

    Returns:
        None
    """
    # Write a row of data about the marriage to the CSV file.
    data = [couple.label,
            couple.partner1.label,
            couple.partner2.label,
            couple.begin,
            couple.end,
            couple.legit]
    writer.writerow(data)



def read_bio(row):
    """
    Reads and classifies information in the row, and creates an instance of the Descendant class.

    Args:
        row (list): A row of data from the CSV file.

    Returns:
        A Descendant instance with information assigned from the input row.
    """
    label = row[0]
    name = row[1]
    house = row[2]
    gender = int(row[3])
    sexuality = int(row[4])
    birth = int(row[5])
    death = int(row[6])
    # Create an instance of Descendant class.
    person = Descendant(birth, gender, [0,0,0], 0)
    # Assign all information about the person.
    person.label = label
    person.name = name
    person.house = house
    person.sexuality = sexuality
    person.death = death
    return person


def find_parents(row, person, marriage_dict):
    """
    Appends a person to the marriage which is stored in the dictionary,
    using the ID of the marriage the person is born from.

    Args:
        row (list): A row of data from the CSV file.
        person (Descendant): The person to append to the marriage.
        marriage_dict (dict): A dictionary of rlationships.
    """
    marriage_dict[row[7]].kids.append(person)
    person.parents = marriage_dict[row[7]]


def read_couple_bio(partner1, partner2, row):
    """
    Returns an instance of the Couple class from information in the CSV.

    Args:
        partner1 (Descendant): The first partner in the couple.
        partner2 (Descendant): The second partner in the couple.
        row (list): A row of data from the CSV file.

    Returns:
        A Couple instance with information assigned from the input row.
    """
    # Create an instance of Couple class.
    couple = Couple(partner1, int(row[3]), row[5], row[0])
    couple.end = int(row[4]) # End year of relationship is row[4]
    couple.label = row[0]
    couple.partner2 = partner2
    # Append this relationship in each their marriages list.
    couple.partner1.marriages.append(couple)
    couple.partner2.marriages.append(couple)
    return couple


def make_csv(filename, fam_dict):
    """
    Write data from a dictionary to a CSV file.

    Args:
        filename (str): The name of the CSV file to write to.
        fam_dict (dict): A dictionary containing the data to write.

    Returns:
        None
    """
    print('\nWRITING CSV:', filename)

    # Open CSV file for writing.
    with open(filename, 'w', newline='', encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)

        # Write the header row to the CSV file.
        header = ['ID', 'name', 'house', 'gender', 'sexuality', 'DOB', 'DOD', 'ParentsID']
        writer.writerow(header)

        # For each person in the dictionary:
        for person in fam_dict.values():

            # Write a row about the person to the CSV file.
            write_bio(person, writer)

            # For each relationship:
            for couple in person.marriages:
                # Write a row about the partner to the CSV file.
                write_bio(couple.partner2, writer)

                # Write a row about the relationship information to the CSV file.
                write_marriage(couple, writer)


def read_csv(filename, fam_dict):
    """
    Takes the data in the CSV and outputs it into a dictionary format.

    Args:
        filename (str): The name of the CSV file.
        fam_dict (dict): The dictionary to store the data in.

    Returns:
        A dictionary of Descendant and Couple instances with their IDs as keys.
    """
    print('\nREADING CSV:', filename)
    marriage_dict = {}
    # Open the CSV file.
    with open(filename, encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            print(row)
            # If it is beyond the header row and before the end row.
            if line_count != 0 and row[0] != '':
                # If it is a partner row.
                if len(row) < 7:
                    # Create an instance of Couple class.
                    couple = read_couple_bio(partner1, partner2, row)
                    # Store info in dictionary.
                    marriage_dict[couple.label] = couple
                else:
                    # If person is descendant, they are counted as partner 1.
                    if row[7] == ('TRUE'):
                        # Create an instance of Descendant class.
                        partner1 = read_bio(row)
                        fam_dict[partner1.label] = partner1
                    # If they are not a descendant of anyone, they are counted as partner 2.
                    elif row[7] == ('FALSE'):
                        partner2 = read_bio(row)
                    # Otherwise, they are an unmarried descendant.
                    else:
                        partner1 = read_bio(row)
                        # Search through the csv for the marriage the person was born from.
                        find_parents(row, partner1, marriage_dict)
                        fam_dict[partner1.label] = partner1 # Store person in dicitonary
            line_count = line_count + 1
