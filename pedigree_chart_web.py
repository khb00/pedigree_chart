"""
This file contains the nescessary functions to run a webpage,
displaying a table with the family tree information.
"""

import webbrowser
import pedigree_chart_sql


def generate_people_table_contents(result):
    """
    Generate the contents of the people table in HTML format.

    Args:
    result: A list of tuples representing the result of an SQL query.

    Returns:
    A string containing an HTML table with the information in the result.
    """

    # Define a string called tbl that contains an HTML table header with column names.
    tbl = """<tr><th>Name ID</th><th>First Name</th><th>House</th><th>Gender</th><th>DOB</th><th>DOD</th><th>Parent ID</th></tr>"""

    for row in result:
        part_a = f"<tr><td>{row[0]}</td>"
        part_b = f"<td>{row[1]}</td>"
        part_c = f"<td>{row[2]}</td>"
        part_d = f"<td>{row[3]}</td>"
        part_e = f"<td>{row[5]}</td>"
        part_f = f"<td>{row[6]}</td>"
        part_g = f"<td>{row[7]}</td></tr>"
        # Define a string called i that concatenates all the HTML table cells for a single row.
        i = part_a + part_b + part_c + part_d + part_e + part_f + part_g
        tbl = tbl + i

    contents = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
    <html>
    <head>
    <meta content="text/html; charset=ISO-8859-1"
    http-equiv="content-type">
    <style>
    table, th, td {
      border: 1px solid black;
    }
    </style>
    </head>
    <body>
    <table>
    <caption>House Table</caption>
    %s
    </table>
    </body>
    </html>
    '''%(tbl)

    return contents


def write_contents(contents, filename):

    """
    Write the contents string to a file with the given filename.

    Args:
    contents: A string containing HTML code.
    filename: A string representing the name of the file to write the contents to.
    """

    with open(filename, "w", encoding="utf-8") as output:
        output.write(contents)


def run_web_table():
    """
    Creates webpage of a table of people.
    """
    filename = 'webbrowser.html'
    result = pedigree_chart_sql.read_table('people')
    contents = generate_people_table_contents(result)
    write_contents(contents, filename) # Write the contents to file named with filename.
    webbrowser.open(filename) #Put filename in browser.


def get_path_file():
    """
    Generates an HTML table containing information about people and writes it to a file.
    Returns the name of the file.
    """

    filename = 'DBTable.html'
    result = pedigree_chart_sql.read_table('people')
    contents = generate_people_table_contents(result)
    write_contents(contents, filename)
    return filename
