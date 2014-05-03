#!/usr/bin/python

import xml.etree.ElementTree as ET

#i'm going to be recieving a bunch of file names and I'm also going to get an article and a revision.

import os
import sys
import re

class Article(object):
	def __init__(self,title):
		self.title = title
		self.revs = []
	def __str__(self):
		return "%s : %s\n" % (self.title,str(self.revs))

if __name__=='__main__':

	if(len(sys.argv) < 4):
		print "use ./prgrmn_name information.tsv xml_path text_output_path clean_output_path"	
		exit()
	WIKI_EXTRACT_PATH = '/home/oliver/Dropbox/DOCUMENTS/CLASS/4thSemseter/Data\ Mining/PROJECT/WIKI_PROJECT/wikipedia2text/wikiextract.py'
	XML_PATH = sys.argv[2]
	TXT_OUTPUT_PATH = sys.argv[3]
	CLEAN_OUTPUT_PATH = sys.argv[4]
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
		try:	
			#	
			saved_revisions = dict()	
			xml_file_path = XML_PATH + " " + article.title + " _wiki.txt"
			print xml_file_path

			XML_tree = ET.parse(xml_file_path)
			XML_root = XML_tree.getroot()
			revision_tag = "{http://www.mediawiki.org/xml/export-0.8/}revision"
			id_tag = "{http://www.mediawiki.org/xml/export-0.8/}id"
			text_tag =  "{http://www.mediawiki.org/xml/export-0.8/}text"


			for rev in XML_root[1].findall(revision_tag):
				cur_rev = int(rev.find(id_tag).text)
				if cur_rev in article.revs:
					saved_revisions[cur_rev]  = rev.find(text_tag).text
				XML_root[1].remove(rev)


			for rev_key in saved_revisions:
					#ADD THE REVISION
					XML_root[1].append(ET.Element(revision_tag))
					XML_root[1].find(revision_tag).append(ET.Element(text_tag))
					XML_root[1].find(revision_tag).find(text_tag).text = saved_revisions[rev_key]
					XML_file_title = article.title + "_" + str(rev_key) + ".xml"
					TEXT_file_title = article.title + "_" + str(rev_key) + ".txt"

					#WRITE OUT THE XML FILE
					XML_tree.write("%s%s" % (TXT_OUTPUT_PATH,XML_file_title) )
					
					#CLEAN UP THE XML FILE
					dirty_file = open("%s%s"% (TXT_OUTPUT_PATH,XML_file_title),"r+")
					clean_string =    ("\n".join(dirty_file.readlines()))
					clean_string = clean_string.replace("ns0:","")
					if len(clean_string) == 0:
						print "Something's wrong"
						exit()
					dirty_file.write(clean_string)
					dirty_file.close()	

					#GET THE PLAIN TEXT OUT
					os.system("mkdir %s%s_%s" % (CLEAN_OUTPUT_PATH,article.title,str(rev_key)))
					os.system("wp2txt -ildtaersg %s%s -o %s%s_%s" % (TXT_OUTPUT_PATH,XML_file_title,CLEAN_OUTPUT_PATH,article.title,str(rev_key)))
					
					#REMOVE THIS SO THAT WE CAN START WITH THE NEXT TREE
					XML_root[1].remove(XML_root[1].find(revision_tag))
		#END TRY	
		except:
			print XML_PATH + " " + article.title + " _wiki.txt" + " Does not exist apparently\n"	
			raise
