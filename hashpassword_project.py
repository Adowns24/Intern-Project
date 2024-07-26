import os
import hashlib
import sqlite3
from pathlib import Path

def read_hashes_from_file(hashfile):
# read hashes from all files in directory

	hashes = set()#set to store unique hashes
	try:
		with open(hashfile, 'r') as f:
			#open the file for reading
			lines = f.readlines()
			print(f"reading{len(lines)}lines from file {hashfile}")
			for line in lines:
			#add each line (hashed_password to set
				stripped_line = line.strip()
					#stripping any whitespaces
				if stripped_line:
					#if hash not empty, add it to the set
					hashes.add(stripped_line)
					
	except Exception as e:
		print(f"Error reading file{hashfile}: {e}")
	print(f"total hashes read from {hashfile}:{len(hashes)}")
	return hashes

def find_leaked_passwords(active_directory, leaked_directory):
	#searches for leaked or reused 
	#this should return a list of all the reused or leaked hashes 
	common_hashes = set()
	
	#reading hashes from both files
	
	pwned_hashes= read_hashes_from_file(leaked_directory)
	conn = sqlite3.connect("hashes.sqlite3")
	cursor = conn.cursor()
	# parse HaveIBeenP0wned into sqlite
	for eachhash in pwned_hashes:
		#print(f"Looking at: {eachhash}")
		parsed_array = eachhash.split(":")
		if (parsed_array[0] == "des-cbc-md5"):
			cursor.execute('''
			INSERT INTO userhash (hash, algo)
			VALUES ("''' + parsed_array[1] + '''", 1)
			''')
		else:
			cursor.execute('''
			INSERT INTO userhash (hash, algo)
			VALUES ("''' + parsed_array[0] + '''", 2)
			''')
	
	# 10292304b3254f7f		
	# Now look up values from the NTDS.dit file
	# The text file that powers this may have multiple entries per line
	activedir_hashes = read_hashes_from_file(active_directory)
	
	for user_hash in activedir_hashes:
		#print(f"Entry is {user_hash}")
		entries = user_hash.split(":")
		#print("Parsing entry for " + str(entries[1]))
		user_hash_algo = 1 if entries[1] == "des-cbc-md5" else 2
		cursor.execute('select count(id) from userhash where algo=' + str(user_hash_algo) + ' and hash="' + entries[2] + '"')
		row = cursor.fetchone()
		#print("SQL output-> " + str([row[0]]))
		if int(row[0]) > 1:
			print("\n\r!!!Warning!!!\n\rGot a hit for " + entries[0])
			common_hashes.add(entries[0])
		
	conn.commit()
	conn.close()
   
   
	# print(f"Active Directory Hashes: {activedir_hashes}")
	# print(f"Pwned Directory Hashes: {pwned_hashes}")
    #this should find the common hashes between the two directories
	#common_hashes = list(activedir_hashes.intersection(pwned_hashes))
	return common_hashes
	
def create_database(db_name):
    # Check if the database already exists
    if os.path.exists(db_name):
        print(f"Database '{db_name}' already exists. Skipping creation.")
        return
    
    # Connect to the database (will create the database if it does not exist)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Create the cryptalgo table
    cursor.execute('''
    CREATE TABLE cryptalgo (
        id INTEGER PRIMARY KEY,
        algo VARCHAR
    )
    ''')
    
    # Create the userhash table
    cursor.execute('''
    CREATE TABLE userhash (
        id INTEGER PRIMARY KEY,
        username VARCHAR,
        hash VARCHAR,
        algo INT
    )
    ''')
    
    cursor.execute('''
	INSERT INTO cryptalgo (id, algo)
	VALUES (1, "des-cbc-md5")
    ''')
    
    cursor.execute('''
	INSERT INTO cryptalgo (id, algo)
	VALUES (2, "des")
    ''')
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
    print(f"Database '{db_name}' created with tables 'cryptalgo' and 'userhash'.")

def main():
	print("Creating the database")
	create_database("hashes.sqlite3")

	print("running the main function")
	#user input the directory path, incase each user has a different path
	active_directory = "testad.txt" #  input("Enter the path to file1:  ").strip() #need to come back and change name
	leaked_directory = "testpwned.txt" # input("Enter the path to the file2:  ").strip()

	active_directory = os.path.abspath(active_directory)
	leaked_directory = os.path.abspath(leaked_directory)

	print(f"active_directory: {active_directory}")
	print(f"Leaked directory: {leaked_directory}")


	#testing if directory is not found throw an errror
	if not os.path.exists(active_directory):
		print(f"Error: '{active_directory}' is not a valid directory.")
		return
	if not os.path.exists(leaked_directory):
		print(f"Error: '{leaked_directory}' is no a valid directory.")
		return

	print("Both directories exist, proceeding to find the leaked hashes")
	
	#should find all the reused and leaked hashes	
	common_hashes = find_leaked_passwords(active_directory,leaked_directory)

	print(f"found {len(common_hashes)} reused or leaked hashes:")
	print(common_hashes)
	
	 #Saving common hashes to a text file
	#with open("common_hashes.txt", "w") as f:
	#	for hash_value in common_hashes:
	#		f.write(hash_value + "\n")
	
	
if __name__ == "__main__":
	main()
