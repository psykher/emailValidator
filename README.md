Email Validator for Python 3.x
==============================
This is a script to verify whether an email address is valid or not.

It checks the syntax and looks up the DNS MX records for the host of the email and will connect to through SMTP to the host on port 25 to try and find out if the email address is valid and exists on that host.

There is a chance for false negatives. This is not always 100% accurate cause signed or restricted mailboxes.

NOTE! Most commercial ISPs will block port 25 so this may not work on your home network.

Requirements:

	Python >= 3.x
	dnspython Libraries (www.dnspython.org)
		'sudo apt-get install python3-dnspython'

Usage:

    python3 emailValidator.py -e <email> -v

Arguments:

	-h or --help                    This help
	-v or --verbose                 Increases verbosity
	-e or --email <email>           Specify one email address to check
	-f or --file <file>             Specify a file of emails delimeted by line

Example:

     python3 emailValidator.py -e admin@example.org -v
     python3 emailValidator.py --file email.txt
     
If my code was useful to you, feel free to [invite me a coffee](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=QDJW7QCGBJL9E&source=url)

Made with ❤ by Carlos Alvarez del Castillo
