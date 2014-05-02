#!/usr/bin/python

if __name__=='__main__':
	
	print "\n".join(sorted(set([x.split()[0] for x in open('download_list.txt',"r").readlines()])))
	
	
