#!/usr/bin/env python3
import os
import argparse
import gettext
import logging
import pkg_resources
import re
import readline
import shutil
import sys
import textwrap
import traceback

import lib50
import requests
import termcolor

from . import __version__, CONFIG_LOADER

# Internationalization
gettext.install("cevsubmit", pkg_resources.resource_filename("cevsubmit", "locale"))

SUBMIT_URL = "https://submit.cs50.io"


class Error(Exception):
    pass

def cprint(text="", color=None, on_color=None, attrs=None, **kwargs):
    """Colorizes text (and wraps to terminal's width)."""
    # Assume 80 in case not running in a terminal
    columns, lines = shutil.get_terminal_size()
    if columns == 0:
        columns = 80  # Because get_terminal_size's default fallback doesn't work in pipes

    # Print text
    termcolor.cprint(textwrap.fill(text, columns, drop_whitespace=False),
                     color=color, on_color=on_color, attrs=attrs, **kwargs)


def prompt(included, excluded):
    if included:
        cprint(_("Files that will be submitted:"), "green")
        for file in included:
            cprint("./{}".format(file), "green")
    else:
        raise Error(_("No files in this directory are expected for submission."))

    # Files that won't be submitted
    if excluded:
        cprint(_("Files that won't be submitted:"), "yellow")
        for other in excluded:
            cprint("./{}".format(other), "yellow")

    # Prompt for honesty
    readline.clear_history()
    try:
        answer = input(_("Are you sure you want to submit these files (yes/no)? "))
    except EOFError:
        answer = None
        print()
    if not answer or not re.match(f"^\s*(?:{_('y|yes')})\s*$", answer, re.I):
        return False

    return True


def excepthook(type, value, tb):
    """Report an exception."""
    if (issubclass(type, Error) or issubclass(type, lib50.Error)) and str(value):
        for line in str(value).split("\n"):
            cprint(str(line), "yellow")
    elif not isinstance(value, KeyboardInterrupt):
        cprint(_("Sorry, something's wrong! Let contact@cevgroup.org know!"), "yellow")

    if excepthook.verbose:
        traceback.print_exception(type, value, tb)

    cprint(_("Submission cancelled."), "red")


excepthook.verbose = True

class LogoutAction(argparse.Action):
    def __init__(self, option_strings, dest=argparse.SUPPRESS, default=argparse.SUPPRESS, help=_("logout of cevsubmit")):
        super().__init__(option_strings, dest=dest, nargs=0, default=default, help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        try:
            lib50.logout()
        except lib50.Error:
            raise Error(_("failed to logout"))
        else:
            cprint(_("logged out successfully"), "green")
        parser.exit()


def main():
    sys.excepthook = excepthook

    parser = argparse.ArgumentParser(prog="cevsubmit")
    parser.add_argument("--logout", action=LogoutAction)
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        help=_("show commands being executed"))
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("slug", help=_(
        "prescribed identifier of work to submit"))

    args = parser.parse_args()

    excepthook.verbose = args.verbose
    if args.verbose:
        logging.basicConfig(level=os.environ.get("CEVSUBMIT_LOGLEVEL", "INFO"))
        # Disable progress bar so it doesn't interfere with log
        lib50.ProgressBar.DISABLED = True

    check_announcements()
    check_version()

    user_name, commit_hash, message = lib50.push("cevsubmit", args.slug, CONFIG_LOADER, prompt=prompt)
    print(message)

if __name__ == "__main__":
    main()
