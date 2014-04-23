import ConfigParser, sys, os.path

from tagm import (
    TagmDB, find_db, process_paths, parse_tagpaths
)
from subprocess import call

conf = ConfigParser.ConfigParser()

conf.read( 'tagm-open.conf' )

mimes = []
tagmatch = []

for sect in conf.sections():
    opts = dict( conf.items( sect ) )
    if 'mime' in opts:
        mimes.append( ( opts['mime'], sect ) )
    if 'tags' in opts:
        tags = parse_tagpaths( opts['tags'].split( ',' ) )
        tagmatch.append( ( tags, sect ) )

dbpath = find_db()
print 'using db at', dbpath
db = TagmDB( os.path.join( dbpath, '.tagm.db' ) )

for f in process_paths( dbpath, [ sys.argv[1] ] ):
    print 'opening ', f

    tags = db.get_obj_tags( [ f ] )
    print tags

    for mtags, sect in tagmatch:
        print 'Matching', mtags
        matches = filter( lambda tag: tag in mtags, tags )
        if matches == mtags:
            print 'Matched!'

            opts = dict( conf.items( sect ) )
            command = opts['command'].replace( '%n', f )
            print command
            call( command, shell = True )

            break