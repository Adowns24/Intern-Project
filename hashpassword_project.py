import os
from pathlib import Path
def read_hashes_from_dir(directory):
# read hashes from all files in directory

	hashes = set()#set to store unique hashes
	for root, _, files in os.walk(directory):
		for file in files: #iterate through the files
			file_path = os.path.join(root, file)
				#get the full file path  
			try:
				with open(file_path, "r") as f:   
					# open each file in read mode
					for line in f:  
							#read each line in the file
						hashes.add(line.strip()) 
							#add the hash to the set
							#should strip any whitespaces
			except Exception as e:
				print(f"Error reading file{file_path}: {e}")
	return hashes

def find_leaked_passwords(active_directory, leaked_directory):
	#searches for leaked or reused 
	#this should return a list of all the reused or leaked hashes 

	#reading hashes from both directories
	activedir_hashes = read_hashes_from_dir(active_directory)#might need to change the name of this directory
	pwned_hashes= read_hashes_from_dir(leaked_directory)
	
	print(f"Active directory hashes: {activedir_hashes}")
	print(f"Haveibeenpwned directory:{pwned_hashes}")

#this should find the common hashes between the two directories
	common_hashes= list(active_dir.intersection(pwned_dir))
	return common_hashes

def main():

	print("running the main function")
	#user input the directory path, incase each user has a different path
	active_directory = input("Enter the path to ntds.dit:  ").strip() 
	leaked_directory = input("Enter the path to the haveibeenpwned directory:  ").strip()

	active_directory = os.path.abspath(active_directory)
	leaked_directory = os.path.abspath(leaked_directory)

	print(f"active_directory: {active_directory}")


	#testing if directory is not found throw an errror
	if not os.path.isdir(active_directory):
		print(f"Error: '{active_directory}' is not a valid directory.")
		return
	if not os.path.isdir(leaked_directory):
		print(f"Error: '{leaked_directory}' is no a valid directory.")
		return

	print("Both directories exist, proceeding to find the leaked hashes")
	
	#should find all the reused and leaked hashes	
	common_hashes = find_leaked_passwords(active_directory, leaked_directory)

	print(f"Found {len(common_hashes)}reused or leaked hashes:") # should print the results from the list

	print(common_hashes)
if __name__ == "__main__":
	main()
