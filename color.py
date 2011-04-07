import os

colors = [ 'grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white' ]
colors = dict( zip( colors, [ '\033[{0}m'.format( i ) for i in range(30, 38) ] ) )
colors['default'] = '\033[0m'
disabled = os.getenv('ANSI_COLORS_DISABLED') is not None

def get( color='default' ):
	if color in colors:
		return colors[ color ]
	return colors['default']

def start( color ):
	print( get( color ) )

def end():
	print( get() )

def wrap( color, text ):
	return '{0}{1}{2}'.format( get( color ), text, get() )

def write( color, text ):
	print( wrap( color, text ) )