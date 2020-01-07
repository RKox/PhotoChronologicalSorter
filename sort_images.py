import os
import subprocess
import shutil

path = os.getcwd() # or specify specic path
exe = r"D:\Ruben\Desktop\image tester\exiftool.exe"
outPutFolder = "sorted images"

# READ METADATA
def getMetaData(exe, file):
	try:
		process = subprocess.Popen([exe, file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
	except:
		print(f"Could possibly not find the exiftool.exe needed for this script in {exe}! Make sure the path to this executable is correct")
		exit()
	# metaData = []
	metaData = {}
	for output in process.stdout:
		# metaDataDict = {}
		line = output.strip().split(":", 1)
		metaData[line[0].strip()] = line[1].lstrip()
		# metaData.append(metaDataDict)
	return metaData

# COPY AND RENAME FILE
def copyRename(file, metaData, newDir):
	print("Trying to move file...")
	extension = metaData.get("File Type Extension")
	if extension.lower() in ("arw", "jpg"):
		newName = metaData.get("Date/Time Original")+"."+extension # arw/jpg
	elif extension.lower() in ("mp4"):
		newName = metaData.get("Create Date")+"."+extension # mp4
	elif extension.lower() in ("avi"):
		newName = metaData.get("File Modification Date/Time")+"."+extension # avi
	else:
		print(f" Could not find \"{newName}\" in \"{file}\"...")
		answer = None
		while answer not in ("y", "yes", "n", "no"):
			answer = input("Continue? (y/n)")
			if answer.lower() in ("y", "yes"):
				print("Continue with remaining files")
				return
			elif answer.lower() in ("n", "no"):
				print("Exiting script.")
				exit()
			else:
				print("please enter yes/y or no/n")
	
	newName = newName.replace(":","-")
	
	oldDirNewName = os.path.join(os.path.dirname(file), newName)
	newDirNewName = os.path.join(newDir, newName)
	
	os.rename(file, oldDirNewName)
	shutil.move(oldDirNewName, newDirNewName)
	print(f"Moved successfully to: {newDirNewName}")


# Create output folder (if necessary)
outPutFolderPath = os.path.join(path, outPutFolder)
if not os.path.exists(outPutFolderPath):
	print(f"creating output folder: {outPutFolderPath}.")
	os.makedirs(outPutFolderPath)
else:
	print(f"folder already exists: {outPutFolderPath}")
	answer = None
	while answer not in ("y", "yes", "n", "no"):
		answer = input("should the existing output folder be emptied? (y/n)")
		if answer.lower() in ("y", "yes"):
			print("deleting folder contents.")
			shutil.rmtree(outPutFolderPath)
		elif answer.lower() in ("n", "no"):
			print("Exiting script.")
			exit()
		else:
			print("please enter yes/y or no/n")
		
# Search for files in folders
files = []
print(f"Finding media files in {path}.")
for r, d, f in os.walk(path):
	for file in f:
		if file.lower().endswith(('.jpg', '.arw', '.raw', '.mp4', '.avi')):
			files.append(os.path.join(r, file))
mediaFound = len(files)

# If media found, copy and rename...
if mediaFound > 0:
	print(f"Script found {mediaFound} media files in folder structure!")
	numFile = 1
	for file in files:
		file = r"{}".format(file)
		print(f"getting metadata from file {numFile} of {mediaFound}... File name: {file}")
		numFile += 1
		metaData = getMetaData(exe, file)
		copyRename(file, metaData, outPutFolderPath)
		for e in metaData:
			print(e)
		print()
else:
	print('No media found in folder...')
	exit()

print("====================")
print("= Script finished! =")
print("====================")
