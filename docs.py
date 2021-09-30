"""WolfJobs.

Usage:
  docs.py  [(<name1>|<name2>)] <name3>...
  docs.py  mov <name1> <name2>
  docs.py  (--h|--q) [<name1> -l]
  docs.py  --version

Options:
  -h --help            Show this screen.
  --version            Show version.
"""


from docopt import docopt

if __name__ == '__main__':
    arguments = docopt(__doc__, version='WolfJobs 1.0')
    print(arguments)