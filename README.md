# uSerFind3r

uSerFind3r.py is used for identifying valid accounts and domains without the risk of account lockouts.  The tool parses responses to identify the "IfExistsResult" flag is null or not, and responds appropriately if the user is valid.  The tool will attempt to identify false positives based on response, and either automatically create a waiting period to allow the throttling value to reset, or warn the user to increase timeouts between attempts.  

uSerFind3r.py can also easily identify if a domain exists in o365 using the -d or --domain flag.  This saves the trouble of copying the url from notes and entering it into the URL bar with the target domain.

## Usage

Change directories to uSerFind3r.py and run:

```pip3 install -r requirements.txt```

This will run the install script to add necessary dependencies to your system.

```python3 uSerFind3r.py -h```

This will output the help menu, which contains the following flags:

```-h, --help - Lists the help options```

```-e, --email - Required for running Oh365UserFinder against a single email account```

```-r, --read - Reads from a text file containing emails (ex. -r emails.txt)```

```-w, --write - Writes valid emails to a text document (ex. -w validemails.txt)```

```-c, --csv - Writes valid emails to a CSV file (ex. -c validemails.csv)```

```-t, --timeout - Sets a pause between attempts in seconds (ex. -t 60)```

```-d, --domain - Checks if the listed domain is valid or not (ex. -d mayorsec.com)```

```--verbose - Outputs test verbosely```

Examples of full commands include:

```python3 uSerFind3r.py -e example@test.com```

```python3 uSerFind3r.py -r emails.txt -w validemails.txt```

```python3 uSerFind3r.py -r emails.txt -w validemails.txt -t 30 -v```
