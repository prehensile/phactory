
import re
import getopt
import sys
import plagiarist

from collections import deque
from os import stat

mysql_host = '127.0.0.1'
mysql_user = 'plagiarist'
mysql_pass = 'x3r0x'
mysql_port = 3306

re_nonalpha = re.compile( '\\W' )
re_whitespace = re.compile( '\\s')
re_apostrophe = re.compile('\'');


def train_from_file( filename, connector ):
	
	myPlagiarist = plagiarist.Plagiarist()
	myPlagiarist.connect( connector )
	
	current_word = ""
	current_triplet = deque()
	
	s = stat( filename )
	l = s.st_size
	f = open( filename )
	c = ""
	
	isNotAlphaNumeric = False
	isWhitespace = False
	hasEndedWord = False
	
	for i in range( 1, l ):
		
		c = f.read( 1 );
		
		isNotAlphaNumeric =  re_nonalpha.match( c )
		isWhitespace = re_whitespace.match( c )
		if( re_apostrophe.match( c ) ):
			isNotAlphaNumeric = False
		
		if( isNotAlphaNumeric ):
			hasEndedWord = True
		
		if( hasEndedWord ):
			if( len( current_word ) > 0 ):
				current_triplet.append( current_word )
				if( len( current_triplet ) == 3 ):
					myPlagiarist.add_triplet( current_triplet )
					current_triplet.popleft()
			current_word = ""
			hasEndedWord = False
		
		if( isWhitespace ):
			hasEndedWord = True
		else: 
			current_word += c;
		
def main():
	
	filename = sys.argv[ 1 ]
	dbname = sys.argv[ 2 ]
	
	connector = plagiarist.PlagiaristConnectorMySQL()
	connector.connect( mysql_host, mysql_port, mysql_user, mysql_pass, dbname )
	
	train_from_file( filename, connector )
	
	connector.commit()
	connector.close()
		
main()