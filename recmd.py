import sys, os, re, fnmatch
import color


def main( args ):
	for f in find( args[0] ):
		print f

def find( pattern=False ):
	for root, dirs, files in os.walk('.'):
		if '.svn' in dirs:
			dirs.remove('.svn')

		print dirs

		for filename in files:
			if not pattern or fnmatch.fnmatch( filename, pattern ):
				yield os.path.join( root, filename )

def grep( pattern ):
	pattern = re.compile( pattern )
	for path in find():
		with open( path ) as file_obj:
			for line_num, line in enumerate( file_obj, 1 ):
				if pattern.search( line ):
					yield ( path, line_num, line )

def textmate():
	os.system( 'open "txmt://open/?url=file://{0}&line={1}"'.format( abspath, num ) )

def run( pattern, options={} ):
	try:
		_run( pattern, options )
	except KeyboardInterrupt:
		print('')
		return

def _run( pattern, options={} ):
	opts = {}
	opts.update( options )

	###########################################################################
	# LOCATE MATCHES
	###########################################################################

	r = re.compile( pattern )
	matches = []
	index = 0

	for root, dirs, files in os.walk('.'):
		if '.svn' in dirs:
			dirs.remove('.svn')

		for name in files:
			path = os.path.join( root, name )

			if os.path.isfile( path ):
				with open( path ) as f:
					num = 0
					for line in f:
						num += 1
						if r.search( line ):
							index += 1
							matches.append( ( index, num, path, line ) )


	###########################################################################
	# FORMAT MATCHES
	###########################################################################

	padIndex = len( '{0}'.format( index ) ) + 2
	gutter = ''.rjust( padIndex, ' ' ) + '  '

	if not matches:
		color.write('grey', "{0}No matches found.".format( gutter ))
		return;

	for index, num, path, line in matches:
		# Prepare the strings
		index = '{0}  '.format( str( index ).rjust( padIndex, ' ' ) )
		path  = path.ljust( 40, ' ' ) + " "
		line  = line.strip()
		line  = (line[:75] + '...') if len(line) > 75 else line
		out   = ''

		out += color.wrap( 'green', index )
		out += color.wrap( 'grey', path )

		# highlight the matches
		out += r.sub( color.wrap( 'blue', '\g<0>'), line.strip() )

		print( out )

	###########################################################################
	# OPEN A FILE
	###########################################################################

	openText  = color.wrap('blue', "\n{0}Open a result".format( gutter ))
	openText += color.wrap('grey', ' (optional)')
	print( openText )

	prompt = color.wrap( 'green', '{0}  '.format( '>'.rjust( padIndex, ' ' ) ) )

	try:
		index = int( raw_input( prompt ) ) - 1 # matches begins at '1'
	except ValueError:
		return

	if index not in range( len( matches ) ):
		return

	index, num, path, line = matches[ index ]
	abspath = os.path.abspath( path )

	color.write( 'grey', '{0}{1}:{2}\n'.format( gutter, path, num ) )
	os.system( 'open "txmt://open/?url=file://{0}&line={1}"'.format( abspath, num ) )

if __name__ == '__main__':
	main(sys.argv[1:])