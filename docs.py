"""WolfJobs.

Usage:
  application.py: Contains all the routes within the application
  apps.py: Initializes the application and mongo instance
  forms.py: Contains the model for all the forms used in the application
  utilities.py: Conatins a helper function to send a mail to the user's registered email address incase of password being forgotton
  
Options:
  -h --help            Show this screen.
  --version            Show version.
"""


from docopt import docopt

if __name__ == '__main__':
    arguments = docopt(__doc__, version='WolfJobs 1.0')
    print(arguments)