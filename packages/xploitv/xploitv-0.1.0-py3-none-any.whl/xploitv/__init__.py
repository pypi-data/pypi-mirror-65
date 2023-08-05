import os
import sys
import logging
import threading

from xploitv.grabber    import Grabber
from xploitv.arguments  import Arguments

def show_banner():
    print(
"""____  ___      .__         .__  __
\\   \\/  /_____ |  |   ____ |__|/  |____  __
 \\     /\\____ \\|  |  /  _ \\|  \\   __\\  \\/ /
 /     \\|  |_> >  |_(  <_> )  ||  |  \\   /
/___/\\  \\   __/|____/\\____/|__||__|   \\_/
      \\_/__|

   [[ An automated Xploitv grabber ]]
""")

def multithreading(grabber: Grabber, codes: list) -> None:
    threads: list = [ threading.Thread(target=grabber.steal, args=(code,)) for code in codes ]
    for thread in threads: thread.start()
    for thread in threads: thread.join()

def entrypoint() -> None:
    # Parse the arguments
    parser: Arguments = Arguments()
    args = parser.parse()
    # Printing the banner
    show_banner()
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
            multithreading(grabber, lines)
    # Output
    if args.extension: grabber.set_format(args.extension.lower())
    grabber.output()


def cli() -> None:
    try: entrypoint()
    except KeyboardInterrupt: sys.exit(2)

if __name__ == '__main__':
    cli()
