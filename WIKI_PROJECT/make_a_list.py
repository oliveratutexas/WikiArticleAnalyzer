#!/usr/bin/python

import sys

#minimum number of ratings needed in order to qualify as statistically significant
CUTOFF = 30
BUFFER_SIZE = 100
#These are all adjusted by 1 from their original values to account for 0 indexing
TRUST = 0
OBJ = 1
COMP = 2
WELLWRIT = 3


class Article(object):

	def __init__(self,name):
		self.page_title = name
		self.revisions = dict()		
		
if __name__ == '__main__':
	
	print sys.argv[1]
	print sys.argv[2]

	tsv = open(sys.argv[1])	
	
	categories = dict()
	#basically a buffer so I can read things in a bit at a time. 
	#	I'm hoping this reduces IO calls

	# Because the first line is just "blah" data
	tsv.readline()
	A = [tsv.readline() for x in range(0,BUFFER_SIZE)]

	while(len(A[0]) != 0):

		for doc in range(0,len(A)):

			cur_string = A[doc].split()
				
			#uh oh, I'm at empty data, no use continuing
			if(len(A[doc]) == 0):
				break
			
			#Wikipedia, clean your damn data!
			if( not cur_string[0].isdigit() or cur_string[2] == "NULL" or not cur_string[6].isdigit() or not cur_string[7].isdigit() or int(cur_string[6]) > 4 or int(cur_string[7]) > 5):
				continue
			
			page_title = 	str(cur_string[2])
			rating_value = 	float(cur_string[7])
			rating_key = 	int(cur_string[6]) - 1
			rev_id = 	int(cur_string[4])
			page_id = 	int(cur_string[1])
			
			#rating value is adjusted for 0 indexing
			if rating_value == 0:
				#no use adding empty rating values
				continue	

			elif not categories.has_key(page_id):

				categories[page_id] = Article(page_title)
				categories[page_id].revisions[rev_id] = [0,0,0,0,0.0,0.0,0.0,0.0] 
				rev = categories[page_id].revisions[rev_id]

				#Initialize each category and frequency 
				categories[page_id].page_title = page_title
				#initialize frequency and average
				rev[rating_key] += 1
				rev[rating_key + 4] += rating_value
			else:
				if(categories[page_id].revisions.has_key(rev_id) == False):
					categories[page_id].revisions[rev_id] = [0,0,0,0,0.0,0.0,0.0,0.0]

				rev = categories[page_id].revisions[rev_id]

				#add to frequency
				rev[rating_key] += 1

				#compute average
				rev[rating_key + 4] = ((rev[rating_key + 4] * (rev[rating_key] - 1) + rating_value) / float(rev[rating_key]))

				 

		#read in the next round of data	
		A = [tsv.readline() for x in range(0,BUFFER_SIZE)]	
		
	OBJ_file = open(str(sys.argv[2]) + ".analysis.tsv","w")
	OBJ_file.write("Page_title\tpage_id\t%revision\tobjective_frequency\tobj_avg\twell_writ_freq\twell_writ_avg\n")
	
	#Write out the frequency for each document	
	num_OBJ = 0
	num_WELLWRIT = 0

	for category in categories:

		#go to each article
		revs = categories[category].revisions
		page_title = categories[category].page_title

		#go to each revision in an article
		for rev in revs:

			table = revs[rev]	
			
			obj_freq = 0
			obj_avg = 0

			wellwrit_freq = 0
			wellwrit_avg = 0
			
			do_write = False
	
			if(table[OBJ] >= CUTOFF):
				do_write = True
				num_OBJ += 1
				obj_freq = table[OBJ]
				obj_avg = table[OBJ + 4]		
				
			if(table[WELLWRIT] >= CUTOFF):
				do_write = True
				num_WELLWRIT += 1
				wellwrit_freq = table[WELLWRIT]
				wellwrit_avg = table[WELLWRIT + 4]

			if(do_write):	
				OBJ_file.write("%s\t%d\t%d\t%d\t%f\t%d\t%f\n" % (page_title,category,rev,obj_freq,obj_avg,wellwrit_freq,wellwrit_avg))
