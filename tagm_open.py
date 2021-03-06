#!/usr/bin/env python2
import ConfigParser, sys, os.path, argparse, fnmatch
from tagm import (
    TagmDB, find_db, process_paths, parse_tagpaths
)
from subprocess import call, check_output

def call_command( conf, sect, f ):
    opts = dict( conf.items( sect ) )
    command = opts['command'].replace( '%n', f )
    call( command, shell = True )

def main():
    # Setup argparser
    parser = argparse.ArgumentParser()
    parser.add_argument( '--tags', action = 'store_true' )
    parser.add_argument( '--conf', action = 'store', default = '~/.config/tagm-open.conf' )
    parser.add_argument( 'files_or_tags', nargs = '+' )

    args = parser.parse_args()

    # Load config
    conf = ConfigParser.ConfigParser()

    conf.read( os.path.expanduser( args.conf ) )

    mimes = []
    tagmatch = []

    for sect in conf.sections():
        opts = dict( conf.items( sect ) )
        if 'mime' in opts:
            for mmime in opts['mime'].split(','):
                mimes.append( ( mmime, sect ) )
        if 'tags' in opts:
            tags = parse_tagpaths( opts['tags'].split( ',' ) )
            tagmatch.append( ( tags, sect ) )

    dbpath = find_db()
    db = TagmDB( os.path.join( dbpath, '.tagm.db' ) )

    # Get files
    if args.tags:
        tagpaths = []
        for tp in args.files_or_tags:
            tagpaths += tp.split( ',' )
        files = db.get( parse_tagpaths( tagpaths ) )
    else:
        files = process_paths( dbpath, args.files_or_tags )

    # Match file(s)
    for f in files:
        tags = db.get_obj_tags( [ f ] )
        for mtags, sect in tagmatch:
            matches = filter( lambda tag: tag in mtags, tags )
            if matches == mtags:
                call_command( conf, sect, f )
                break
        else:
            f = os.path.join( dbpath, f )

            mime = check_output( [ 'file', '-b', '--mime-type', f ] ).strip()
            for mmime, sect in mimes:
                if fnmatch.fnmatch( mime, mmime ):
                    call_command( conf, sect, f )
                    break


if __name__ == '__main__':
    main()