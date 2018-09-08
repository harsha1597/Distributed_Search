Setting up:
Install mongodb: 1.MongoDB  https://docs.mongodb.com/v3.2/installation/
                 2. MongoDB Atlas which provides GUI to interact with your DB : https://www.mongodb.com/products/compass
Sample Text files: So for the testing part I've put text files in different Folders , and in the server DB I've used Folder names as 
                  a "Client"
                  The text files are numbered 1-7
Before running the programs, Open command prompt and type "mongod" this will run the mongodb application                 

For the serverside: Run the file "serverbase.py" on Command prompt
PS: If you get an error for duplicate IDs then comment the insert_one() lines which I've mentioned in the program

For the clientside: Make sure that clientpart_main_2.py and clientbase_2.py are in the same folder
                    In the clientpart_main_2.py file add the paths to the different Text files in your client
                    This will perform the different classification operations and then send the classified words to the server
PS: If you get an error for duplicate IDs then comment the insert_one() lines which I've mentioned in the program
                    
The file query_test.py has a list of test queries which are already given in the list "test": 
Change or add to it , to check for new inputs
