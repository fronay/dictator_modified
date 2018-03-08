import csv
import os 

BASE_DIR = os.getcwd()
FILE_NAME = BASE_DIR + "/round_data.csv"
# opens PW file
with open(FILE_NAME, 'rU') as f:  
	reader = csv.reader(f)
	# read csv into a list of lists
	data = list(list(rec) for rec in csv.reader(f, delimiter=';')) 
	dictator_sharing_incentive = {}
	receiver_option = {}
	for i, row in enumerate(data):
		# this alone will print all the computer names
		if i > 0:
			roundnumber = int(row[0])
			sharing_incentive = row[1]
			# if sharing incentive is a comma-separated number (in some excel versions), replace with dot before conversion to floating point
			if "," in sharing_incentive:
				sharing_incentive = sharing_incentive.replace(",", ".")
			sharing_incentive = float(sharing_incentive)
			dictator_sharing_incentive[roundnumber] = sharing_incentive
			receiver_option[roundnumber] = str(row[2])
	print dictator_sharing_incentive, "\n"
	print receiver_option
	print "YO, test, in round 3 you should have : {}, {}, {}".format(3, dictator_sharing_incentive[3], receiver_option[3])
