#!/usr/bin/python

import xml.etree.ElementTree as ET

#i'm going to be recieving a bunch of file names and I'm also going to get an article and a revision.

import os
import sys

class Article(object):
	def __init__(self,title):
		self.title = title
		self.revs = []
	def __str__(self):
		return "%s : %s\n" % (self.title,str(self.revs))

if __name__=='__main__':

	if(len(sys.argv) < 2):
		print "use ./prgrmn_name information.tsv "	
		exit()

	revision_ratings = [x for x in open(sys.argv[1]).readlines()[1:]]
	articles = []
	
	#initialize the first article	
	cur_article = Article(revision_ratings[0].split()[0])
	last_title = ''

	#CREATE A BUNCH OF ARTICLES
	for rating_datum in [x.split() for x in revision_ratings]:

		if(last_title == rating_datum[0]):
			#add a bunch of ratings to that article
			articles[-1].revs.append(int(rating_datum[2]))
		else:
			#set the title
			last_title = rating_datum[0]
			articles.append(Article(rating_datum[0]))
			articles[-1].revs.append(int(rating_datum[2]))


	#FOR EACH REVISION IN AN ARTICLE, MAKE A FILE THAT YOU CAN ANALYZE
	for article in articles:
		
		#	
		saved_revisions = dict()	
		XML_tree = ET.parse(" " + article.title + " _wiki.txt")
		XML_root = XML_tree.getroot()
		
		for rev in XML_root[1].findall('revision'):
			if int(rev.find('id').text) in article.revs:
				saved_revisions[rev]  = rev.find('text').text
			rev.remove('revision')				
	
			#root.tag
			#root.attrib
			

		for rev_key in saved_revisions:

			#ADD THE REVISION
			XML_root[1].append('revision')
			rev.find('revision').text = saved_revision[rev_key]
			file_title = article.title + "_" + str(rev_key) + ".xml"

			#WRITE OUT THE REVISION
			XML_tree.write( file_title )
			
			#GET THE PLAIN TEXT OUT
			os.system("wikiExtract %s -o %s_%d.txt " % (file_title, article.title,rev) )
			XML_root[1].remove('revision')
		
		

		
