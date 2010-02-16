import sys
import gabble

mysql_host = '127.0.0.1'
mysql_user = 'gabble'
mysql_pass = 'g4bbl3'
mysql_port = 3306

def main():

	dbname = sys.argv[ 1 ]
	source = gabble.GabbleSourceMySQL()
	source.connect( mysql_host, mysql_port, mysql_user, mysql_pass, dbname )
	print gabble.Gabble.gabble_simple( source, 100 )	 
	
main()	

