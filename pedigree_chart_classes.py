"""
Defines classes descendant and couple, and their methods.
"""

from random import randint


class Descendant:
    """
    This class is used to represent an individual.
    Methods are __init__, generate_legit_marriage, generate_illegit_marriage
    """

    def __init__(self, birth, gender, parents, num):
        """
        Initialize a new instance of a Descendant.

        Args:
            birth (int): The birth year of the Descendant.
            gender (int): The gender of the Descendant (0 for male, 1 for female).
            parents (instance of Couple class): The marriage the Descendant was born from.
            num (int): The position in the birth order from relationship.
        """

        self.gender = gender  # Gender is represented as an integer, 0 for male and 1 for female.
        self.name = generate_name(gender)  # Assign the descendant a first name based on their gender.
        self.birth = birth  # Record the year of the descendant's birth.
        self.death = calculate_death(birth)  # Calculate the descendant's death year based on their birth year.
        self.parents = parents  # If the descendant has parents, this should be a Couple. Otherwise, it should be a list of [0, 0, TRUE].
        self.marriages = []  # Initialize an empty list to store the descendant's marriages.

        try:
            # If the descendant has parents, they inherit their surname.
            self.house = parents.house
            # Generate a unique ID for the descendant,
            # based on their name, parents' ID, and position in birth order.
            self.label = self.name + parents.label + str(num)
            # Set the descendant's sexuality to 0, representing heterosexual orientation.
            self.sexuality = 0
            # Assign a 5% chance of bisexuality or homosexuality,
            # otherwise keep the sexuality as heterosexual.
            if randint(0, 99) < 10:
                self.sexuality = randint(1, 2)
        except:
            # If the descendant is the initial node (i.e. has no ancestors),
            # generate a random surname.
            self.house = generate_house(parents[2])
            # Generate a unique ID for the descendant based on their name and a "0" placeholder
            self.label = self.name + str(parents[0])
            # Set the descendant's sexuality based on the parent's value
            # (0 for heterosexual)
            self.sexuality = parents[1]
            self.death = 70

    def generate_legit_marriage(self, marriage_age):
        """
        Generate legitimate marriages for the descendant, if possible

        Args:
            marriageAge (int): The age of Descendant when they can be married.
        """

        legit = True  # Whether the children from this marriage will be legitimate.
        count_begin = marriage_age + self.birth
        i = 0  # Counter for the number of legitimate marriages the descendant has had.
        while count_begin < self.death:
            for year in range(count_begin, self.death):  # Each year the descendant is alive.
                chance = randint(0, 10)
                # If the descendant has never been married before,
                # increase the chance of getting married.
                # Otherwise, there is a 1 in 11 chance of marriage each year.
                if ((self.marriages) == 0 and int(chance/2) == 1) or (chance == 0):
                    # Assign a unique ID to the marriage, indicating it is legitimate.
                    label = str('L') + str(i)
                    # Generate an instance of the Couple class for this marriage.
                    couple = generate_partnership(self, year, legit, label)
                    count_begin = couple.end  # Update the start year for the next marriage.
                    i = i + 1  # Increment the counter for legitimate marriages.


    def generate_illegit_marriage(self, romance_age):
        """
        Generate illegitimate marriages for the descendant, if possible

        Args:
            reomanceAge (int): The age of the Descendant when they can enter a relationship.
        """
        if (randint(0, 4) == 0 and self.gender == 0) or (randint(0, 15) == 0 and self.gender == 1) :
            legit = False # The children born from this relationship are not legitimate
            i = 0 # Counter for the number of illegitimate marriages the descendant has had
            # Calculate the year descendant can begin entering relationships.
            count_begin = romance_age + self.birth
            partner_count = randint(1,6)
            while count_begin < self.death:
                for year in range(count_begin, self.death):
                    # Probility of entering a relationship is a function of
                    # number of previous relationships and partner count.
                    if randint(0,(30 - partner_count + len(self.marriages)))==0 and partner_count>0:
                        # Assign a unique ID to the marriage, indicating it is illegitimate.
                        label = str('I') + str(i)
                        # Generate an instance of the Couple class for this marriage.
                        generate_partnership(self, year, legit, label)
                        i = i + 1# Increment the counter for illegitimate marriages.
                        partner_count = partner_count - 1 # reduce partner_count by 1.
                count_begin = self.death + 1



class Couple:
    """
    This class is used to represent an relationship.
    Methods are __init__, generate_children.
    """

    def __init__(self, partner1, begin, legit, label):
        """
        Creates an instance of the Couple class.

        Args:
            partner1 (Descendant): The first partner in the couple.
            begin (int): The beginning year of the relationship.
            legit (bool): The legitimacy of the relationship.
            label (int): The ID of the relationship.

        Attributes:
            partner1 (Descendant): The first partner in the couple.
            label (str): The ID of the relationship, a set of numbers with 'I' and 'L' throughout.
            partner2 (Descendant): The second partner in the couple.
            house (str): The house of the couple.
            begin (int): The beginning year of the relationship.
            end (int): The end year of the relationship.
            kids (list): A list of children born from the relationship.
            legit (bool): The legitimacy of the relationship.
        """
        # partner1 is the descendant in the family tree.
        self.partner1 = partner1
        # The id of this relationship should be a set of numbers with I and L throughout.
        self.label = partner1.label.split(partner1.name)[1] + str(label)
        # Generate the partner of this relationship.
        self.partner2 = generate_partner(partner1, begin, self.label, legit)
        # If father is a commoner or mother is a commoner, surname is fathers.
        if (partner1.gender == 0 and partner1.house != 'Lowborn') or (self.partner2.house == 'Lowborn'):
            self.house = partner1.house
        else:
            self.house = self.partner2.house
        self.begin = begin # Year of the start of relationship.
        self.end = calculate_end(partner1, self.partner2, begin, legit) # end of relationship
        self.kids = [] # List of kids born from relationship.
        self.legit = legit # Legitamacy of relationship.

    def generate_children(self):
        """
        Generates children for the couple.
        """
        if self.partner1.gender != self.partner2.gender: #if this is a opposite-sex  relationship
            i = 0 # this is how many children have been born from this relationship
            #define which partner is mother and father
            if self.partner1.gender == 0:
                wife = self.partner2
            else:
                wife = self.partner1
            #for every year for which the relationship occurs,
            for year in range(self.begin, self.end):
                #prob represents fertility,
                #which is dependent on legitamcy of relationship and age of mother.
                if self.legit:
                    prob = -3.1943*(year-wife.birth) + 136.97
                else:
                    prob = -3.1943*(year-wife.birth) + 126.97
                # for years in which mother already has a child, her fertility is 0.
                for couple in wife.marriages:
                    for kid in couple.kids:
                        if kid.birth == year:
                            prob = 0
                threshold = randint(0,99)
                if prob > threshold:
                    birth = year
                    # A new instance of descendant is created.
                    # Added to list of kids born from this relationship.
                    self.kids.append( Descendant(birth, randint(0,1), self, i) )
                    i = i + 1 # number of kids increments by 1
                    if randint(0,99) < 4: # 5% probility of having twins
                        self.kids.append( Descendant(birth, randint(0,1), self, i) )
                        i = i + 1
                    elif randint(0,9999) == 0: # 1 in 10000 probility of having triplets
                        self.kids.append( Descendant(birth, randint(0,1), self, i) )
                        i = i + 1
                        self.kids.append( Descendant(birth, randint(0,1), self, i) )
                        i = i + 1


def generate_name(gender):
    '''
    Generates the first name

            Args:
                    gender (int): 0 for male, 1 for female

            Returns:
                    name (str): first name
    '''
    # Pick a name from these csv's depending on gender
    if gender == 0:
        name = read_name('Fantasymalename.txt')
    else:
        name = read_name('Fantasyfemalename.txt')
    return name


def generate_house(legit):
    '''
    Generates surname

            Args:
                    legit (bool): legitamacy of relationship

            Returns:
                    name (str): the surname
    '''
    #if the marriage is legit, or 50%, surname is a noblilty one
    if legit or randint(0,1) == 0:
        name = read_name('Fantasyhousename.txt')
    else:
        #person is a commoner
        name = 'Lowborn'
    return name


def generate_partnership(descendant, begin, legit, label):
    '''
    Collates information to create an instnce of a Couple class with children

            Args:
                    descendant (instance of Descendant class): person in tree
                    begin (int): year relationship begins
                    legit (bool): legitamacy of relationship
                    ID (str): unique ID of relationship
            Returns:
                    couple (instance of Couple class): the relationship descendant belongs to
    '''
    couple = Couple(descendant, begin, legit, label)
    descendant.marriages.append(couple) # Add this relationship to descendants marriages
    couple.partner2.marriages.append(couple) # Add this relationship to partners marriages
    couple.generate_children() # generate children for couple
    return couple


def calculate_death(birth):
    '''
    Calculates the year of death

            Args:
                    birth (int): the year of birth
            Returns:
                    death (int): the year of death
    '''
    #Crisis years are years in which a tradegy occured such as a plauge or civil war
    crisis_years = [30,49,80,119,155,192, 250]
    # This is the percentage of people who die in the crisis years
    death_percent = [20,50,20,50,80,40, 100]
    age = abs(int(-0.01397*(randint(0,10000)) + 113.00)) # This is the age that they live to
    death = birth + age # Year of death is birth year and age
    #if you are alive during one of the crisis years, there is a chance you dire in those years.
    for year, percent in zip(crisis_years, death_percent):
        if birth < year < death :
            if randint(0,99) < percent:
                death = year
    return int(death)


def generate_partner(descendant, begin, label, legit):
    '''
    Generates a partner for descendant

            Args:
                    descendant (Descendant): person in tree
                    begin (int): year relationship begins
                    label (str): unique ID of relationship
                    legit (bool): legitamacy of relationship
            Returns:
                    partner (Descendant): the newly generated partner for the descendant
    '''
    gender = calculate_gender(descendant, legit)
    birth = calculate_birth(begin, descendant)
    # Create an instance of descendant for the partner.
    partner = Descendant(birth, gender, [label, descendant.sexuality, legit], None )
    i = 0 # This is the number of attempts to calculate year of death for the partner.
    # If the calculated death of partner is before the beginning year of the relationship,
    while partner.death < begin:
        # Recalculate the partner death.
        partner.death = calculate_death(partner.birth)
        i = i + 1
        if i == 5: # After 5 unsuccessful attempts,
            partner.death = descendant.death # partners death is the same as the descendants.
    return partner


def calculate_gender(descendant, legit):
    '''
    Generates a gender for partner of descendant
    
            Args:
                    descendant (instance of Descendant class): person in tree
                    legit (bool): legitamacy of relationship
            Returns:
                    gender (int): 0 for male, 1 for female
    '''
    # if it is a legitimate marriage or the descendant is heterosexual, partner is opposite sex.
    if legit or descendant.sexuality == 0:
        if descendant.gender == 0:
            gender = 1
        else:
            gender = 0
    else:
        #if it is a illegit relationship and descendant is gay, gender is same as descendants.
        if descendant.sexuality == 2:
            gender = descendant.gender
        else:
            #if it is a illegit relationship and descendant is bi, gender is randomly generated.
            gender = randint(0,1)
    return gender


def calculate_birth(begin, descendant):
    '''
    Calculates a birth year for partner

            Args:
                    descendant (instance of Descendant class): person in tree
                    begin (int): year relationship begins
            Returns:
                    birth (int): the year of birth
    '''
    descendant_age = begin - descendant.birth # Calculate the age of the descendant
    # 7 years and the older partners age halved is the lowest possible age for the younger partner
    lower_age =  int(abs((descendant_age/2)+7))
    upper_age = int(abs((descendant_age-7)*2))
    #If the range of ages is 0, age is the only possible age
    if lower_age == upper_age :
        age = lower_age
    #If the range of ages exceeds 20 years, the range is shortened to 20 year range
    elif abs(upper_age-lower_age) > 20:
        age = descendant_age + randint(-10,10)
    else:
        age = randint(lower_age,upper_age)
    birth = begin - int(abs(age)) #Calculate year of birth
    return birth


def calculate_end(partner1, partner2, begin, legit):
    '''
    Calculate the year the relationship ends

            Args:
                    partner1 (instance of Descendant class): person in tree
                    partner2 (instance of Descendant class): partner of person in tree
                    begin (int): year relationship begins
                    legit (bool): legitamacy of relationship
            Returns:
                    end (int): the last year of the relationship
    '''
    #if it is a legitimate marriage, the relationship must end due to death, not divorce.
    if legit:
        if partner1.death < partner2.death:
            end = partner1.death
        else:
            end = partner2.death
    #illegit relationships can last up to 20 years or to either partners death
    else:
        end = randint(0,20) + begin
        #if either partner dies before the end, they end is updated to be their death year.
        if partner1.death < end:
            end = partner1.death
        if partner2.death < end:
            end = partner2.death
    return end


def read_name(filename):
    '''
    Picks a random string from a csv
            Args:
                    filename (string): the name of the csv file that will be read
            Returns:
                    name (string): name picked from csv file
    '''

    with open(filename, 'r', encoding="utf-8") as test_file: # Read the csv file
        test_lines = test_file.readlines() # Copy the csv into the list test_lines


    linenum = randint(0,len(test_lines)-1) # Choose a random line to pick name from
    name = test_lines[linenum].rstrip('\n') # Extract chosen name

    return name
