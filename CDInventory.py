#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# joeprado, 2020-Mar-09, Began modifying Script
# joeprado, 2020-Mar-10, Added docstrings.
# joeprado, 2020-Mar-10, Finished script modifications
# joeprado, 2020-Mar-23, Added structured exception handling
# joeprado, 2020-Mar-23, Modified script to use binary files instead of text files
# joeprado, 2020-Mar-24, Edited docstrings to reflect use of binary files 
#------------------------------------------#

import pickle #Import Pickle module 

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    @staticmethod
    def add_cd(cdID, title, artist, table):
        """Adding user data for new CD to a table.
        
        Takes user input fed into the function via parameters,formats it as a set key:value pairs in a
        dictionary, and then appends that dictionary as row nested inside a list. 
        
        Args: 
            cdID (string): ID number of CD as entered by the user
            title (string): Title of CD as entered by the user
            artist (string): Artist name for the CD as entered by the user
            table (list of dict): list of dictionaries that holds our data in volatile memory 
            
        Returns: 
            None.
        """
        try: intID = int(cdID)  #try statement, except clause, and else clause to prevent program from crashing if a numnber isn't entered.
        except ValueError: # Handles Value Error if it is raised. 
            print("\nYou must enter the CD ID as an integer. Adding CD failed.\n" )
        else:    
            row = {'ID': intID, 'Title': title, 'Artist': artist}
            table.append(row)
    
    @staticmethod
    def delete_cd(selectID, table):
        """Delete a CD selected by user based on ID.
        
        Takes user input for the ID number of a CD the user would like to delete, searches for the row (dictionary) the ID is in,
        then deletes that row (dictionary) in the table (list).
        
        Args:
            selectID (integer): user selection for CD ID number the user would like to delete.
            table (list of dict): list of dictionaries that holds our data in volatile memory 
            
        Returns:
            None.
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == selectID:
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
    
       
class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to load binary file to a list of dictionaries.

        Loads data from file identified by file_name into a 2D list
        

        Args:
            file_name (string): name of pickled binary file used to load the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file
        try: 
            objFile = open(file_name, 'rb') #Reads from binary file in. 
            table = pickle.load(objFile) #Loads contents of binary file into list 
            objFile.close()
        except IOError: 
            print("\nNo CD file exists.  Add and save CD info to inventory to create a file.\n")


    @staticmethod
    def write_file(file_name, table):
        """Pickles the contents of CD Inventory into a binary file.
        
        Takes the list of dictionaries identified by table and dumps it into binary file 
        identified by file_name.
        
        
         Args:
            file_name (string): name of file used to save data to. 
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
            
        Returns:
            None
        """
        objFile = open(file_name, 'wb') #Writes to binary file. Creates file if it doesn't exist. 
        pickle.dump(table, objFile) #Dumps content of list containing CD information into binary file. 
        objFile.close()


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('\nMenu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.
        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def input_new_cd():
        """Function that collects user input for a new CD to be added to inventory.
        
        Args: 
            None.
            
        Returns:
            cdID (string): string representing ID number user entered for CD 
            title (string): string representing CD title entered by user
            artist (string): string representing artist name entered by user
        """
        cdID = input('Enter ID: ').strip()
        title = input('What is the CD\'s title? ').strip()
        artist = input('What is the Artist\'s name? ').strip()
        return cdID, title, artist


# 1. When program starts, calls function that reads in the currently saved Inventory
print()
FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(strFileName, lstTbl) #Calls function that loads text file containing CD inventory into runtime. 
            IO.show_inventory(lstTbl) #Calls function that displays inventory to user
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl) #Calls function that displays inventory to user
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Calls function that asks user for new ID, CD Title and Artist
        strID, strTitle, strArtist = IO.input_new_cd()  
        # 3.3.2 Calls the function that adds item to the table
        DataProcessor.add_cd(strID, strTitle, strArtist, lstTbl)
        #Calls function that displays inventory with added CD
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl) # Calls function that displays current inventory
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 Calls function that displays inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        try: intIDDel = int(input('Which ID would you like to delete? ').strip()) # try statement to prevent prgm crash if non-number is entered.
        except ValueError: # handles ValueError exception and notified user that deleting CD failed. 
            print("\nYou must enter ID as a integer. Deleting CD failed.\n")
        # 3.5.2 Calls function that searches thru table and deletes CD
        else:  
            DataProcessor.delete_cd(intIDDel, lstTbl)
            IO.show_inventory(lstTbl) #Calls function that displays inventory to user
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Calls function that displays current inventory. 
        IO.show_inventory(lstTbl) 
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower() #asks user for confirmation to save
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 Calls function that saves data
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




