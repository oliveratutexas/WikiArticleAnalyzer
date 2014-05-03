#!/usr/bin/python

#i'm going to be recieving a bunch of file names and I'm also going to get an article and a revision.
import re
import sys
import random

def avg_word_length(document):

	ans = 0.0
	count = 0.0
	
	for sen in document:
		for word in sen.split():
			if(word.isalpha()):
				count += 1.0
				ans = (	(ans * count - 1)+ len(word)) / count

	return ans

def sent_length(document):

	avg = 0.0
	count = 1.0
	for sen in document:
		count = 1.0
		sen_count = 0.0
		for word in sen.split():
			if word.isalpha():
				sen_count += 1
		avg = ((avg * (count - 1)) + sen_count) / count 
	return avg

def normalized_unique(document):

	ans = 0.0
	document_size = 0
	all_words = set()
	
	for sen in document:
		for word in sen.split():
			if word.isalpha():
				all_words.add(word)	
				document_size += 1
			

	return float(len(all_words)) / float(document_size)		
	


def prep_commas(document):
	PREPS = set(["aboard","about","above","across","after","against","along","amid","among","anti","around","as","at","before","behind","below","beneath","beside","besides","between","beyond","but","by","concerning","considering","despite","down","during","except","excepting","excluding","following","for","from","in","inside","into","like","minus","near","of","off","on","onto","opposite","outside","over","past","per","plus","regarding","round","save","since","than","through","to","toward","towards","under","underneath","unlike","until","up","upon","versus","via","with","within","without"])
	
	comma_count = 0
	prep_count = 0

	for sen in document:
		for item in sen.split():
			for letter in item:
				if letter == ',':
					comma_count += 1	
			if item.isalpha():
				if item in PREPS:
					prep_count += 1				 

	return comma_count + comma_count
class TrainingDatum(object):
	def __init__(self,title):
		self.title = title
		self.word_length = 0.0
		self.word_unique = 0.0
		self.sent_length = 0.0
		self.prep_commas = 0.0
		self.obj_avg = 0.0
		self.well_writ_avg = 0.0

if __name__=='__main__':

	if(len(sys.argv) < 3):
		print "use ./prgrmn_name information.tsv /path_to_text_files"	
		exit()
	
	obj_file = open("obj_matrix.dat","w")
	obj_sampl = open("max_sampl.dat","w")
	wellwrit_file = open("ww_matrix.dat","w")
	ww_sampl = open("ww_sampl.dat","w")

	PATH_TO_TEXT_FILES = sys.argv[2]
	revision_ratings = [x for x in open(sys.argv[1]).readlines()[1:]]
	training_data = []	

	for rating_datum in [x.split() for x in revision_ratings]:
		try:
			
			text_file = open("%s%s_%s/%s_%s-1.txt"%(PATH_TO_TEXT_FILES,rating_datum[0],rating_datum[2],rating_datum[0],rating_datum[2]),"r").readlines()
			sentences = re.findall("[^.!?\s][^.!?]*(?:[.!?](?!['\"]?\s|$)[^.!?]*)*[.!?]?['\"]?(?=\s|$)",''.join(text_file))

			training_data.append(TrainingDatum(rating_datum[0]))
			training_data[-1].obj_avg = float(rating_datum[4])
			training_data[-1].well_writ_avg = float(rating_datum[6])
			training_data[-1].word_length = avg_word_length(sentences)
			training_data[-1].sent_length = sent_length(sentences)
			training_data[-1].word_unique = normalized_unique(sentences)
			training_data[-1].prep_commas = prep_commas(sentences)
		except:
			print "Empty Record\n"

	#obj_count = 0
	#ww_count = 0
	#num_partitions = 5

	for datum in training_data:
		if(0.0 != datum.obj_avg):
			#obj_avg += 1
			obj_file.write("%f\t%f\t%f\t%f\t%f\n" % (datum.well_writ_avg,datum.word_length,datum.sent_length,datum.word_unique,datum.prep_commas))		
		
	
		if(0.0 != datum.well_writ_avg):
			#ww_matrix += 1
			wellwrit_file.write("%f\t%f\t%f\t%f\t%f\n" % (datum.obj_avg,datum.word_length,datum.sent_length,datum.word_unique,datum.prep_commas))		
	
	#numbas = range(0,obj_count)
	#	for i in range(0,num_partitions):
	#		for x in random.sample(numbas, (obj_avg/num_partitions)):
		
