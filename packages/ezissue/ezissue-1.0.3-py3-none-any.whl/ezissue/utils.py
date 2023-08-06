from colored import fg
from colored import attr

RESET = attr(0)
NORMAL = fg(7)
DEBUG = fg(239)
NOTIFY = fg(14)
ERROR = fg(196)
SUC = fg(82)


def prompt(text):
    """
    Prints with the normal color.
    """
    print("%s%s %s" % (NORMAL, text, RESET))


def debug(text, show):
    """
    Prints a custom colored debug string.
    """
    if show:
        print("%s%s %s" % (DEBUG, text, RESET))


def notify(text):
    """
    Prints a custom colored notification string.
    """
    print("%s%s %s" % (NOTIFY, text, RESET))


def get_from_user(question):
    """
    Recieves a input with a colored question.
    """
    return input('%s%s %s\n' % (NORMAL, question, RESET))


def error(text):
    """
    Prints a custom colored error string.
    """
    print("%s%s %s" % (ERROR, text, RESET))


def show_resp_req(req_json, res):
    """
    Prints the request status with custom colors.
    """
    prompt('\nRequest\'s json ~> %s' % req_json)
    if res.status_code == 201:
        print('Request\'s response ~> %s%d%s' % (SUC, res.status_code, RESET))
    else:
        print('Request\'s response ~> %s%d%s' %
              (ERROR, res.status_code, RESET))
