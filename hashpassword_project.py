import os
import hashlib
from pathlib import Path

def read_hashes_from_directory(directory):
# read hashes from all files in directory

	hashes = set()#set to store unique hashes
	for root, _, files in os.walk(directory):	
		for file in files:
			 #iterate through the files
			file_path = os.path.join(root, file)
			try:
				with open(file_path, 'r') as f:
					lines = f.readlines()
					print(f"reading{len(lines)}lines from file {file_path}")
					for line in lines:
						#add each line (hashed_password to set
						stripped_line = line.strip()
						if stripped_line:
							hashes.add(stripped_line)
					
			except Exception as e:
				print(f"Error reading file{file_path}: {e}")
	print(f"total hashes read from {directory}:{len(hashes)}")
	return hashes

def find_leaked_passwords(active_directory, leaked_directory):
	#searches for leaked or reused 
	#this should return a list of all the reused or leaked hashes 

	
	#reading hashes from both directories
	activedir_hashes = read_hashes_from_directory(active_directory)#might need to change the name of this directory
	pwned_hashes= read_hashes_from_directory(leaked_directory)

   
   
	print(f"Active Directory Hashes: {activedir_hashes}")
	print(f"Pwned Directory Hashes: {pwned_hashes}")
#this should find the common hashes between the two directories
	common_hashes = list(activedir_hashes.intersection(pwned_hashes))
	return common_hashes

def main():

	print("running the main function")
	#user input the directory path, incase each user has a different path
	active_directory = input("Enter the path to file1:  ").strip() #need to come back and change name
	leaked_directory = input("Enter the path to the file2:  ").strip()

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

	print(f"found {len(common_hashes)}reused or leaked hashes:")
	print(common_hashes)
	
	 #Saving common hashes to a text file
	#with open("common_hashes.txt", "w") as f:
	#	for hash_value in common_hashes:
	#		f.write(hash_value + "\n")
	
	
if __name__ == "__main__":
	main()
