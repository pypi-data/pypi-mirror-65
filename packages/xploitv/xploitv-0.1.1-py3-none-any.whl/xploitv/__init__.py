#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Core modules
# --------------
import os
import sys
import logging
import threading

# Xploitv modules
# -----------------
from xploitv.grabber    import Grabber
from xploitv.arguments  import Arguments

# Banner
# -------
def show_banner():
    ''' Print the banner of the program '''
    print(
"""____  ___      .__         .__  __
\\   \\/  /_____ |  |   ____ |__|/  |____  __
 \\     /\\____ \\|  |  /  _ \\|  \\   __\\  \\/ /
 /     \\|  |_> >  |_(  <_> )  ||  |  \\   /
/___/\\  \\   __/|____/\\____/|__||__|   \\_/
      \\_/__|

   [[ An automated Xploitv grabber ]]
""")

# Concurrency
# -------------
def multithreading(grabber: Grabber, codes: list, nthreads: int) -> None:
    ''' Run the program using a concurrency paradigm '''
    logging.debug(f"Running {nthreads} threads...")
    # Set the max number of threads
    for i in range(0,len(codes),nthreads):
        threads: list = [ threading.Thread(target=grabber.steal, args=(code,)) for code in codes[i:i+nthreads] ]
        # Start and wait
        for thread in threads: thread.start()
        for thread in threads: thread.join()

# Entrypoint
# ------------
def entrypoint() -> None:
    ''' Script entrypoint '''
    # Parse the arguments
    parser: Arguments = Arguments()
    args = parser.parse()
    # Print the banner
    if not args.bare: show_banner()
    # Check required arguments
    if not args.id and not args.wordlist: parser.help()
    # Logging basic configuration
    if not args.v: args.v = 2
    elif args.v > 5: args.v = 5
    logging.basicConfig(
        level=(40 - args.v * 10),
        format='[%(asctime)s] %(message)s',
        datefmt='%H:%M:%S')
    # Checking the service status
    logging.critical("Let's hack this world!")
    grabber: Grabber = Grabber()
    if not grabber.check_status():
        logging.critical("Service not accesible")
        sys.exit(1)
    # Grabbing
    if args.id: grabber.steal(args.id)
    else:
        if args.wordlist:
            lines: list = list()
            logging.info(f"Using the wordlist {args.wordlist}")
            with open(args.wordlist) as wordlist:
                lines = [ line[:-1] for line in wordlist.readlines() if len(line) > 0 ]
            multithreading(grabber, lines, args.threads)
    # Output
    if args.extension: grabber.set_format(args.extension.lower())
    grabber.output()

# Cli entrypoint
# ----------------
def cli() -> None:
    ''' Cli entrypoint '''
    try: entrypoint()
    except KeyboardInterrupt: sys.exit(2)

# Main
# ------
if __name__ == '__main__':
    cli()
