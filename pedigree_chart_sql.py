"""
# make a database using mysql
# put all info in database
# Much of the code was taken from https://www.w3schools.com/python/python_mysql_getstarted.asp
"""

import mysql.connector
from pedigree_chart_classes import Couple


def create_person_val(fam_dict):
    """
    Format data from fam_dict so that it can be placed into person table.

    Return:
     val (list) : All the necessary data from Dict arranged into items and rows.
    """
    val = []

    # For every person in the dictionary:
    for person in fam_dict.values():
        # If person is a descendant of someone else,
        # the data in the parents ID column is their parentID.
        if isinstance(person.parents, Couple):
            parents_label = person.parents.label
            val = add_bio(val, person, parents_label)
        # If person is a the initial node, the data in the parents ID column is set as True.
        elif person.label.split(person.name)[1] == ('0'):
            parents_label = True
            val = add_bio(val, person, parents_label)
        # For all the partners, the data in the parents ID column is set as False.
        for couple in person.marriages:
            person = couple.partner2
            parents_label = False
            val = add_bio(val, person, parents_label)
    return val


def add_bio(val, person, parent_label):
    """
    Add a person's biographical information to a list.

    Args:
    val (list): The list to append the person's biographical information to.
    person (Descendant): The person whose biographical information should be added.
    parent_label (str): The label of the person's parent.

    Returns:
    list: The updated list of biographical information, with the new information appended.
    """

    bio = (person.label,
            person.name,
            person.house,
            person.gender,
            person.sexuality,
            person.birth,
            person.death,
            parent_label)
    val.append(bio)
    return val


def create_marriage_val(fam_dict):
    """
    Format data from fam_dict so that it can be placed into person table.

    Return:
     val (list) : All the necessary data from Dict arranged into items and rows.

    """
    val = []

    # For every person in the dictionary,
    for person in fam_dict.values():
        # For evry relationship the person has had, arrange its data into a list.
        for couple in person.marriages:
            data = (couple.label,
                    couple.partner1.label,
                    couple.partner2.label,
                    couple.begin,
                    couple.end,
                    couple.legit)
            val.append(data)
    return val


def establish_connection():
    """
    Create connection with SQL database.

    Return mydb, the connected database
    """
    mydb = mysql.connector.connect(
      host= "",
      user= "",
      password= "",
      database = "pedigree_chart_db"
    )
    return mydb


def write_person_table(fam_dict):
    """
    Create table about individuals in Dict and insert into database.
    """
    mydb = establish_connection()
    mycursor = mydb.cursor()

    # Define command to make the table, and its arguments.
    sql = "INSERT INTO people ( name_label, first_name, house, gender, sexuality, dob, dod, parents_label)VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    val = create_person_val(fam_dict) # Define arguments in command.

    mycursor.executemany(sql, val) # Execute command.

    mydb.commit() # Commit changes to database.

    print(mycursor.rowcount, "people record(s) inserted.")


def write_marriage_table(fam_dict):
    """
    Create table about relationships In Dict and insert into database.
    """
    mydb = establish_connection()

    mycursor = mydb.cursor()

    sql = "INSERT INTO marriages (marriage_label, partner1_label, partner2_label, start_year, end_year, legit) VALUES (%s, %s, %s, %s, %s, %s)" # Define command to make the table, and its arguments.

    val = create_marriage_val(fam_dict) # Define arguments in command.

    mycursor.executemany(sql, val)  # Execute command.

    mydb.commit() # Commit changes to database.

    print(mycursor.rowcount, "marriage record(s) inserted.")


def delete_table(table_name):
    """
    Delete table in database.

      Arg:
       table_name (string): Name of table to be deleted.
    """
    mydb = establish_connection()
    mycursor = mydb.cursor()

    sql = "DELETE FROM " + table_name # Define command to delete the table.

    mycursor.execute(sql) # Execute command.

    mydb.commit() # Commit changes to database

    print(mycursor.rowcount, "record(s) deleted")


def read_table(table_name):

    """
    Read table in database.

    Return the selected table.
    """
    mydb = establish_connection()
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM " + table_name) # Select which table to read.

    myresult = mycursor.fetchall()

    return myresult


def request_person_record(name_label):
    """
    Find individual in the database.
    """

    mydb = establish_connection()
    mycursor = mydb.cursor()

    # Define command, and insert the individuals ID.
    sql = "SELECT * FROM people WHERE name_label ='" + name_label + "'"
    mycursor.execute(sql)

    myresult = mycursor.fetchall()

    # Print the individuals data.
    for data in myresult:
        print(data)


def make_database(fam_dict):
    """
    Reset the database with the new dictionaries.
    """
    delete_table("people")
    delete_table("marriages")
    write_marriage_table(fam_dict)
    write_person_table(fam_dict)
