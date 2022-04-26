#!/usr/bin/python3

import requests as o365request
import argparse
import time
import re
import textwrap
import sys
from colorama import Fore, Style, init


def definitions():
    global info, close, success, fail
    info, fail, close, success = Fore.YELLOW + Style.BRIGHT, Fore.RED + \
        Style.BRIGHT, Style.RESET_ALL, Fore.GREEN + Style.BRIGHT


def banner():
    print(Fore.YELLOW + Style.BRIGHT + "")
    print("")
    print("")
    print("")                                 
    print("") 
    print("-" * 70)
    print(Fore.YELLOW + Style.BRIGHT + "")                         
    print("                                   Version 2022                                         ")
    print("                                      ＪＡＹ                                    ")
    print("                        uSerFind3r.py -h to get started                            \n" + Style.RESET_ALL)
    print(Fore.YELLOW + Style.BRIGHT + "")
    print("-" * 70)
    print(Fore.RED + Style.BRIGHT + "")


def options():
    opt_parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, epilog=textwrap.dedent(
        '''Example: python3 uSerFind3r.py -e callcentre@kra.go.ke
Example: python3 uSerFind3r.py -r testemails.txt -w valid.txt --verbose
Example: python3 uSerFind3r.py -r emails.txt -w validemails.txt -t 30 --verbose
Example: python3 uSerFind3r.py -r emails.txt -c validemails.csv -t 30
Example: python3 uSerFind3r.py -d kra.go.ke
'''))
    opt_parser.add_argument(
        '-e', '--email', help='(Runs uSerFind3r against a single email)')
    opt_parser.add_argument(
        '-r', '--read', help='Reads email addresses from file')
    opt_parser.add_argument(
        '-t', '--timeout', help='Set timeout between checks to avoid false positives')
    opt_parser.add_argument(
        '-w', '--write', help='Writes valid emails to text file')
    opt_parser.add_argument(
        '-c', '--csv', help='Writes valid emails to a .csv file')
    opt_parser.add_argument(
        '-d', '--domain', help='Validate if a domain exists')
    opt_parser.add_argument(
        '-v', '--verbose', help='Prints output verbosely', action='store_true')
    global args
    args = opt_parser.parse_args()
    if len(sys.argv) == 1:
        opt_parser.print_help()
        opt_parser.exit()
        


ms_url = 'https://login.microsoftonline.com/common/GetCredentialType'


def main():
    if args.timeout is not None:
        print(
            info + f'[info] Timeout set to {args.timeout} seconds between requests.\n' + close)
    counter = 0
    timeout_counter = 0
    print(Fore.YELLOW + Style.BRIGHT +
          f'\n[info] Starting Oh365 User Finder at {time.ctime()}\n' + Style.RESET_ALL)
    if args.email is not None:
        email = args.email
        s = o365request.session()
        body = '{"Username":"%s"}' % email
        request = o365request.post(ms_url, data=body)
        response_dict = request.json()
        response = request.text
        valid_response = re.search('"IfExistsResult":0,', response)
        valid_response5 = re.search('"IfExistsResult":5,', response)
        valid_response6 = re.search('"IfExistsResult":6,', response)
        invalid_response = re.search('"IfExistsResult":1,', response)
        throttling = re.search('"ThrottleStatus":1', response)
        if args.verbose:
            print('\n', email, s, body, request, response_dict, response, valid_response,
                  valid_response5, valid_response6, invalid_response, '\n')
        if invalid_response:
            a = email
            b = " Result - Invalid Email Found! [-]"
            print(fail + f"[-] {a:51} {b}" + close)
        if valid_response or valid_response5 or valid_response6:
            a = email
            b = " Result - Valid Email Found! [+]"
            print(success + f"[+] {a:53} {b} " + close)
        if throttling:
            print(
                fail + "\n[warn] Results suggest O365 is responding with false positives. Retry the scan in 60 seconds." + close)
            sys.exit()
        if args.timeout is not None:
            time.sleep(int(args.timeout))

    elif args.read is not None:
        with open(args.read) as input_emails:
            for line in input_emails:
                s = o365request.session()
                email_line = line.split()
                email = ' '.join(email_line)
                body = '{"Username":"%s"}' % email
                request = o365request.post(ms_url, data=body)
                response = request.text
                valid_response = re.search('"IfExistsResult":0,', response)
                valid_response5 = re.search('"IfExistsResult":5,', response)
                valid_response6 = re.search('"IfExistsResult":6,', response)
                invalid_response = re.search('"IfExistsResult":1,', response)
                throttling = re.search('"ThrottleStatus":1', response)
                if args.verbose:
                    print('\n', s, email_line, email, body, request, response, valid_response,
                          valid_response5, valid_response6, invalid_response, '\n')
                if invalid_response:
                    a = email
                    b = " Result - Invalid Email Found! [-]"
                    print(fail + f"[-] {a:51} {b}\x1b[0m" + close)
                if valid_response or valid_response5 or valid_response6:
                    a = email
                    b = " Result -   Valid Email Found! [+]"
                    print(success + f"[+] {a:51} {b}" + close)
                    counter = counter + 1
                    if args.write is not None:
                        a = email
                        with open(args.write, 'a+') as valid_emails_file:
                            valid_emails_file.write(f"{a}\n")
                    elif args.csv is not None:
                        a = email
                        with open(args.csv, 'a+') as valid_emails_file:
                            valid_emails_file.write(f"{a}\n")
                if throttling:
                    if args.timeout is not None:
                        timeout_counter = timeout_counter + 1
                        if timeout_counter == 5:
                            print(
                                fail + f'\n[warn] Results suggest O365 is responding with false positives.')
                            print(
                                fail + f'\n[warn] O365 has returned five false positives.\n')
                            print(
                                info + f'[info] Oh365UserFinder setting timeout to 10 minutes. You can exit or allow the program to continue running.')
                            time.sleep(int(300))
                            print(info + f'\nScanning will continue in 5 minutes.')
                            time.sleep(int(270))
                            print(info + f'\nContinuing scan in 30 seconds.')
                            time.sleep(int(30))
                            timeout_counter = 0
                            #sys.exit()
                        else:
                            print(
                                fail + f"\n[warn] Results suggest O365 is responding with false positives. Sleeping for {args.timeout} seconds before trying again.\n")
                            time.sleep(int(args.timeout))

                    else:
                        print(
                            fail + "\n[warn] Results suggest O365 is responding with false positives. Restart scan and use the -t flag to slow request times." + close)
                        sys.exit()
                if args.timeout is not None:
                    time.sleep(int(args.timeout))
            if counter == 0:
                print(
                    fail + '\n[-] There were no valid logins found. [-]' + close)
                print(
                    info + f'\n[info] Scan completed at {time.ctime()}' + close)
            elif counter == 1:
                print(
                    info + '\n[info] Oh365 User Finder discovered one valid login account.' + close)
                print(
                    info + f'\n[info] Scan completed at {time.ctime()}' + close)
            else:
                print(
                    info + f'\n[info] Oh365 User Finder discovered {counter} valid login accounts.\n' + close)
                print(
                    info + f'\n[info] Scan completed at {time.ctime()}' + close)

    elif args.domain is not None:
        domain_name = args.domain
        print(
            info + f"[info] Checking if the {domain_name} exists...\n" + close)
        url = (
            f"https://login.microsoftonline.com/getuserrealm.srf?login=user@{domain_name}")
        request = o365request.get(url)
        response = request.text
        valid_response = re.search('"NameSpaceType":"Managed",', response)
        if args.verbose:
            print(domain_name, request, response, valid_response)
        if valid_response:
            print(
                success + f"\n[success] The listed domain {domain_name} exists.\n" + close)
        else:
            print(
                fail + f"[info] The listed domain {domain_name} does not exist.\n" + close)
        print(info + f'[info] Scan completed at {time.ctime()}' + close)
    else:
        sys.exit()


if __name__ == "__main__":
    try:
        init()
        definitions()
        banner()
        options()
        main()

    except KeyboardInterrupt:
        print("\nYou either fat fingered this, or meant to do it. Either way, goodbye!")
        quit()
