from timeit import default_timer
from itertools import chain as itertools_chain, product as itertools_product
from string import digits, ascii_lowercase as lowercase, ascii_uppercase as uppercase
from py7zr import SevenZipFile, exceptions as SevenZipExceptions
from argparse import ArgumentParser
from sys import argv, exit
from os import environ, path

argument_parser = ArgumentParser(prog="Bruteforcer", description="Helps you bruteforce 7zip folders")
argument_parser.add_argument('filename')
argument_parser.add_argument('-u', '--uppercase', help='bruteforce with uppercase letters', action='store_true', required=False)
argument_parser.add_argument('-l', '--lowercase', help='bruteforce with lowercase letters', action='store_true', required=False)
argument_parser.add_argument('-n', '--numbers', help='bruteforce with numbers', action='store_true', required=False)
argument_parser.add_argument('-s', '--special-char', help='bruteforce with special characters', action='store_true', required=False)
argument_parser.add_argument('-a', '--all', help='bruteforce with lowercase and uppercase letters, numbers and special characters', action='store_true', required=False, default=True)
argument_parser.add_argument('-D', '--debug-mode', help='bruteforce with debug on', action='store_true', required=False, default=False)
argument_parser.add_argument('--max-length', help='set the max length of the password to bruteforce', required=True, choices=range(1,11), type=int)
argument_parser.add_argument('--locked-folder-path', help='the locked folder that you want bruteforced', required=True)

special = '&#+=$*%!:;?,'

print_frequency = 10000
passes = open('top10000.txt').read()
top_10000 = passes.split('\n')

def bruteforce():
    n = 0
    for candidate in itertools_chain.from_iterable(itertools_product(charset, repeat=i) for i in range(1, args.max_length + 1)):
        if debug_mode:
            n += 1
            if n % print_frequency == 0:
                print(''.join(candidate))

        try_pass(''.join(candidate))  

def try_pass(pwd: str):
    try: 
        with SevenZipFile(args.locked_folder_path, mode='r', password=pwd) as z: 
            print(f'''PASSWORD FOUND: {pwd}''')

            if input('Do you want to extract the files (y/n): ') == 'y': 
                extracted_path = path.join(path.join(environ['USERPROFILE']), 'Documents') + "\Extracted"

                z.extractall(extracted_path)
                print(f'Your files have been extracted to {extracted_path}')
            
            exit()

    except SevenZipExceptions.Bad7zFile:
        return

if __name__ == '__main__':
    args = argument_parser.parse_args(argv)
    charset = ''
    tries = 0

    if args.uppercase:
        charset += uppercase
    if args.lowercase:
        charset += lowercase
    if args.numbers:
        charset += digits
    if args.all:
        charset += digits + lowercase + uppercase + special
    

    debug_mode = args.debug_mode
    max_length = args.max_length
    
    start_time = default_timer()
    print(f'Starting at {start_time}')

    print('Trying with commonly used passwords')
    for i in top_10000:
        try_pass(i)

    print('Trying with random numbers and letters')
    bruteforce()
