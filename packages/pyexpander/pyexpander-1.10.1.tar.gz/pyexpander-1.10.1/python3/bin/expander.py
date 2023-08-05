#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
"""expander.py: this is the pyexpander application.
"""

# pylint: disable=C0322,C0103,R0903

from optparse import OptionParser
#import string
import os.path
import sys

import pyexpander.lib as pyexpander

# version of the program:
__version__= "1.10.1" #VERSION#

assert __version__==pyexpander.__version__

def check_encoding(encoding):
    """check if the encoding name is valid."""
    try:
        pyexpander.test_encoding(encoding)
        return
    except LookupError:
        pass
    url="https://docs.python.org/3/library/codecs.html#standard-encodings"
    sys.exit(("unknown encoding name: %s, see %s for a "
              "list of known encodings") % (repr(encoding), repr(url)))

def process_files(options,args):
    """process all the command line options."""
    my_globals={}
    if options.eval is not None:
        for expr in options.eval:
            # pylint: disable=W0122
            exec(expr, my_globals)
            # pylint: enable=W0122
    filelist= []
    if options.file is not None:
        filelist= options.file
    if len(args)>0: # extra arguments
        filelist.extend(args)
    encoding= pyexpander.INPUT_DEFAULT_ENCODING
    if options.encoding:
        check_encoding(options.encoding) # may exit the program
        encoding= options.encoding
        pyexpander.INPUT_DEFAULT_ENCODING= options.encoding
    output_encoding= pyexpander.SYS_DEFAULT_ENCODING
    if options.output_encoding:
        check_encoding(options.output_encoding) # may exit the program
        output_encoding= options.output_encoding
    if len(filelist)<=0:
        pyexpander.expandFile(None,
                              encoding,
                              my_globals,
                              options.simple_vars,
                              options.auto_continuation,
                              options.auto_indent,
                              options.include,
                              options.no_stdin_msg,
                              output_encoding)
    else:
        for f in filelist:
            # all files are expanded in a single scope:
            my_globals= \
                pyexpander.expandFile(f,
                                      encoding,
                                      my_globals,
                                      options.simple_vars,
                                      options.auto_continuation,
                                      options.auto_indent,
                                      options.include,
                                      False,
                                      output_encoding)

def script_shortname():
    """return the name of this script without a path component."""
    return os.path.basename(sys.argv[0])

def print_summary():
    """print a short summary of the scripts function."""
    print(("%-20s: a powerful macro expension language "+\
           "based on python ...\n") % script_shortname())

def main():
    """The main function.

    parse the command-line options and perform the command
    """
    # command-line options and command-line help:
    usage = "usage: %prog [options] {files}"

    parser = OptionParser(usage=usage,
                          version="%%prog %s" % __version__,
                          description="expands macros in a file "+\
                                      "with pyexpander.")

    parser.add_option("--summary",
                      action="store_true",
                      help="Print a summary of the function of the program.",
                     )
    parser.add_option("-f", "--file",
                      action="append",
                      type="string",
                      help="Specify a FILE to process. This "
                           "option may be used more than once "
                           "to process more than one file but note "
                           "than this option is not really needed. "
                           "Files can also be specified directly after "
                           "the other command line options. If not given, "
                           "the program gets it's input from stdin.",
                      metavar="FILE"
                     )
    parser.add_option("--encoding",
                      action="store",
                      type="string",
                      help="Specify the ENCODING for the file(s) "
                           "that are read.",
                      metavar="ENCODING"
                     )
    parser.add_option("--output-encoding",
                      action="store",
                      type="string",
                      help="Specify the OUTPUTENCODING for the "
                           "created output.",
                      metavar="OUTPUTENCODING"
                     )

    parser.add_option("--eval",
                      action="append",
                      type="string",
                      help="Evaluate PYTHONEXPRESSION in global context.",
                      metavar="PYTHONEXPRESSION"
                     )
    parser.add_option("-I", "--include",
                      action="append",
                      type="string",
                      help="Add PATH to the list of include paths.",
                      metavar="PATH"
                     )
    parser.add_option("-s", "--simple-vars",
                      action="store_true",
                      help="Allow variables without brackets.",
                     )
    parser.add_option("-a", "--auto-continuation",
                      action="store_true",
                      help="Assume '\' at the end of lines with commands",
                     )
    parser.add_option("-i", "--auto-indent",
                      action="store_true",
                      help="Automatically indent macros.",
                     )
    parser.add_option("--no-stdin-msg",
                      action="store_true",
                      help= "Do not print a message on stderr when the "
                            "program is reading it's input from stdin."
                     )

    # x= sys.argv
    (options, args) = parser.parse_args()
    # options: the options-object
    # args: list of left-over args

    if options.summary:
        print_summary()
        sys.exit(0)

    process_files(options,args)
    sys.exit(0)

if __name__ == "__main__":
    main()
