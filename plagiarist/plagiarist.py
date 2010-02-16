import MySQLdb

class Plagiarist:
	
	def connect( self, connector ):
		self.connector = connector
	
	def add_preceding_word_link( self, word, preceding_word ):
		word_id = self.connector.id_for_word( word )
		preceding_word_id = self.connector.id_for_word( preceding_word )
		self.connector.add_frequency_counted_link( "preceding_words", "root_word_id", word_id, "preceding_word_id", preceding_word_id )
	
	def add_following_word_link( self, word, following_word ):
		word_id = self.connector.id_for_word( word )
		following_word_id = self.connector.id_for_word( following_word )
		self.connector.add_frequency_counted_link( "following_words", "root_word_id", word_id, "following_word_id", following_word_id )
	
	def add_triplet( self, triplet ):
		self.add_preceding_word_link( triplet[ 1 ], triplet[ 0 ] )
		self.add_following_word_link( triplet[ 1 ], triplet[ 2 ] )
		self.connector.increment_frequency_for_word( triplet[ 1 ] )
		
		
class PlagiaristConnectorSQL:
	
	def __init__( self ):
		self.word_ids = {}
	
	def connect( self, cursor ):
		self.curs = cursor
	
	def increment_frequency_for_word( self, word ):
		word_id = self.id_for_word( word )
		self.curs.execute( "UPDATE words SET frequency=frequency+1 WHERE id=%s", ( word_id, ) )
	
	def id_for_word( self, word ):
		lcword = word.lower()
		if( lcword not in self.word_ids ):
			self.curs.execute( "INSERT INTO words ( word ) VALUES ( %s )", (word,) )	
			id = self.curs.lastrowid
			self.word_ids[ lcword ] = id
		return( self.word_ids[ lcword ] )
	
	def add_frequency_counted_link( self, table_name, column_name_1, id_1, column_name_2, id_2 ):
		# using % instead of allowing execute() to format is insecure, but the only way to get correct formatting
		self.curs.execute( "SELECT id FROM %s WHERE %s=%s AND %s=%s" % ( table_name, column_name_1, id_1, column_name_2, id_2 ) )
		row = self.curs.fetchone()
		link_id = 0
		if( row is None ):
			self.curs.execute( "INSERT INTO %s (%s, %s) VALUES (%s, %s)" % ( table_name, column_name_1, column_name_2, id_1, id_2 ) )
			link_id = self.curs.lastrowid
		else :
			link_id = row[ 0 ]
		self.curs.execute( "UPDATE %s SET frequency=frequency+1 WHERE id=%s" % ( table_name, link_id ) )

		
class PlagiaristConnectorMySQL( PlagiaristConnectorSQL ):
	
	def connect( self, host, port, user, passwd, db ):
		self.db = MySQLdb.connect( host=host, port=port, user=user, passwd=passwd, db=db )
		PlagiaristConnectorSQL.connect( self, self.db.cursor() )
	
	def commit( self ):
		self.db.commit()	
	
	def close( self ):
		self.curs.close()
		self.db.close()