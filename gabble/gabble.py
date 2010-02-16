import re
from random import choice
import MySQLdb

class Gabble:
	@classmethod
	def gabble_simple( cls, source, target_word_count ):
		
		re_sentence_end = re.compile( '[\\.\\?!]' )			
		re_alphanumeric = re.compile( '\\w' )
		
		# get a sentence start word (one following a full stop)
		word = source.get_following_word( ".", 10 )
		gabbled_text = ""
		done = False
		isAlpha = True;
		
		while( done is False ):
			word = source.get_following_word( word, 10 )
			if( word is not None ):
				isAlpha = re_alphanumeric.match( word, len(word) - 1 )
				if( isAlpha ):
					gabbled_text += " "
				gabbled_text += word
				target_word_count-=1
				if( target_word_count < 0 ):
					if( source.has_following_link( word, "." ) ):
						gabbled_text += "."
						done = True
			else:
				done = True
		
		return gabbled_text
				

class GabbleSourceSQL:
	
	def __init__( self ):
		self.word_ids = {}
	
	def connect( self, cursor ):
		self.curs = cursor
	
	def id_for_word( self, word ):
		lcword = word.lower()
		if( lcword not in self.word_ids ):
			self.curs.execute( "SELECT id FROM words WHERE word=%s", (word,) )
			row = self.curs.fetchone()
			self.word_ids[ lcword ] = row[ 0 ]
		return( self.word_ids[ lcword ] )
		
	def get_following_word( self, word, search_range ):
		word_id = self.id_for_word( word )
		self.curs.execute( "SELECT following_word_id FROM following_words WHERE root_word_id=%s ORDER BY frequency DESC LIMIT %s", (word_id, search_range) )
		word = None
		rows = self.curs.fetchall()
		if( len( rows ) > 0 ):
			row = choice( rows )
			word_id = row[ 0 ]
			self.curs.execute( "SELECT word FROM words WHERE id=%s", word_id )
			row = self.curs.fetchone()
			word = row[ 0 ]
		return( word )
	
	def has_following_link( self, root_word, following_word ):
		root_word_id = self.id_for_word( root_word )
		following_word_id = self.id_for_word( following_word )
		self.curs.execute( "SELECT id FROM following_words WHERE root_word_id=%s AND following_word_id=%s", (root_word_id, following_word_id) )
		row = self.curs.fetchone()
		return( row is not None )
		

class GabbleSourceMySQL( GabbleSourceSQL ):
	
	def connect( self, host, port, user, passwd, db ):
		self.db = MySQLdb.connect( host=host, port=port, user=user, passwd=passwd, db=db )
		GabbleSourceSQL.connect( self, self.db.cursor() )
	
	def close():
		self.curs.close()
		self.db.close()