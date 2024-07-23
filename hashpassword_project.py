import os
import hashlib
from pathlib import Path
    
def read_hashes_from_files(file_paths):
# read hashes from all files in directory

	hashes = set()#set to store unique hashes
		
	for file_path in file_paths: #iterate through the files
			print(f"Reading hash from file: {file_path}")  # Add this line for debugging
			try:
				file_hash = calculate_file_hash(file_path)
				hashes.add(file_hash)
					#add the hash to the set
			except Exception as e:
				print(f"Error reading file{file_path}: {e}")
	return hashes

def find_leaked_passwords(active_files, leaked_files):
	#searches for leaked or reused 
	#this should return a list of all the reused or leaked hashes 

	
	#reading hashes from both directories
	activedir_hashes = read_hashes_from_files(active_files)#might need to change the name of this directory
	pwned_hashes= read_hashes_from_files(leaked_files)

   
   
	print(f"Active Directory Hashes: {activedir_hashes}")
	print(f"Pwned Directory Hashes: {pwned_hashes}")
	
#this should find the common hashes between the two directories
	common_hashes = list(activedir_hashes.intersection(pwned_hashes))
	print(f"Common Hashes Found: {common_hashes}")  # Debug print
	return common_hashes

def main():

	print("running the main function")
	#user input the directory path, incase each user has a different path
	active_files = input("Enter the path to file1:  ").strip() #need to come back and change name
	leaked_files = input("Enter the path to the file2:  ").strip()

	active_directory = os.path.abspath(active_files)
	leaked_directory = os.path.abspath(leaked_files)

	#testing if directory is not found throw an errror
	if not os.path.exists(active_files):
		print(f"Error: '{active_files}' is not a valid directory.")
		return
	if not os.path.exists(leaked_files):
		print(f"Error: '{leaked_files}' is no a valid directory.")
		return

	print("Both directories exist, proceeding to find the leaked hashes")
	
	#should find all the reused and leaked hashes	
	common_hashes = find_leaked_passwords([active_files],[leaked_files])

	print(f"found {len(common_hashes)}reused or leaked hashes:")
	print(common_hashes)
	
	 #Saving common hashes to a text file
	with open("common_hashes.txt", "w") as f:
		for hash_value in common_hashes:
			f.write(hash_value + "\n")
	
	
if __name__ == "__main__":
	main()
