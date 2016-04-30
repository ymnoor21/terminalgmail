# Terminal Gmail
Fetch your gmail email(s) from terminal.

# Installation
1. Use this link to install & setup <a target="_blank"  href='https://developers.google.com/gmail/api/quickstart/python#step_2_install_the_google_client_library'>Gmail API</a>.
2. Edit `mygmail.sh` file to setup the correct location of `mygmail.py` file at the bottom.
3. Now, Run this command in your terminal: `python mygmail.py`. It will pop up a browser window to ask for your permission to access gmail. Allow it to access.
4. Once Step 2 is done, you're ready to run. Run `python mygmail.py` to test again. If it doesn't throw any error (Sometime you need to install additional python libraries depending on your python setup) you're ready to go.
5. Now, symlink this `mygmail.py` file to a shortcut command by running this command: `ln -s /path/to/your/mygmail.py /usr/local/bin/mygmail`.
6. Once done, restart your terminal and run `mygmail`.

# Usage
Run `mygmail --help` or `mygmail -h` to see the command line usage.

1. `-q` parameter takes all kinds of available <a target="_blank" href="https://support.google.com/mail/answer/7190?hl=en">advanced</a> search commands for gmail.
2. `-d` parameter is the directory you want to search. i.e: INBOX, SPAM, also all custom labels you've created in your gmail.

# Sample command(s)
1. `mygmail` (by `-q` defaults to `is:unread` and `-d` defaults to `INBOX`).
2. `mygmail -q "is:unread from:someuser@gmail.com" -d INBOX`.
3. `mygmail -q "from:John Doe" -d "Super Important"` (using custom directory "Super Important").

