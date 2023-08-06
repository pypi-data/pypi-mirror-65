# This file is part of ubuntu-bug-triage. See LICENSE file for license info.
"""Ubuntu Bug Triage module."""

import argparse
import logging
import sys

from . import UBUNTU_PACKAGE_TEAMS
from . import ACTIONABLE_BUG_STATUSES
from .triage import PackageTriage, TeamTriage
from .view import BrowserView, CSVView, JSONView, TerminalView


def parse_args():
    """Set up command-line arguments."""
    parser = argparse.ArgumentParser('ubuntu-bug-triage')
    parser.add_argument(
        'package_or_team', nargs='?', default='ubuntu-server',
        help="""source package name (e.g. cloud-init, lxd) or package team name
        (e.g. ubuntu-openstack, foundations-bugs) to use for search (default:
        ubuntu-server)"""
    )
    parser.add_argument(
        'days', nargs='?', type=int, default=1,
        help="""days of updated bugs to triage"""
    )
    parser.add_argument(
        '--anon', action='store_true',
        help='Anonymous login to Launchpad'
    )
    parser.add_argument(
        '--csv', action='store_true',
        help='output as CSV'
    )
    parser.add_argument(
        '--debug', action='store_true',
        help='additional logging output'
    )
    parser.add_argument(
        '--json', action='store_true',
        help='output as JSON'
    )
    parser.add_argument(
        '--open', action='store_true',
        help='open resulting bugs in web browser'
    )
    parser.add_argument(
        '--include-project', '-p', action='store_true',
        help='include project bugs in output'
    )
    parser.add_argument(
        '--status', '-s', action='append', default=[], metavar='STATUS',
        choices=["any", "New", "Incomplete", "Opinion", "Invalid", "Won't Fix",
                 "Expired", "Confirmed", "Triaged", "In Progress",
                 "Fix Committed", "Fix Released", "Incomplete (with response)",
                 "Incomplete (without response)"],
        help='Restrict the search to bugs with the given status.'
        ' Can be specified multiple times. Defaults: ' + ', '.join(
            ACTIONABLE_BUG_STATUSES) + '.'
    )

    return parser.parse_args()


def setup_logging(debug):
    """Set up logging."""
    logging.basicConfig(
        stream=sys.stdout,
        format='%(message)s',
        level=logging.DEBUG if debug else logging.INFO
    )


def launch():
    """Launch ubuntu-bug-triage."""
    args = parse_args()
    if not args.status:
        args.status = ACTIONABLE_BUG_STATUSES
    elif 'any' in args.status:
        args.status = []
    args.status = list(set(args.status))
    setup_logging(args.debug)

    if args.package_or_team in UBUNTU_PACKAGE_TEAMS:
        if args.include_project:
            logging.getLogger(__name__).warning(
                "N.B. --include-project has no effect when running against a"
                " package team")
        triage = TeamTriage(args.package_or_team, args.days,
                            args.anon, args.status)
    else:
        triage = PackageTriage(args.package_or_team, args.days, args.anon,
                               args.include_project, args.status)

    bugs = triage.updated_bugs()
    if args.csv:
        CSVView(bugs)
    elif args.json:
        JSONView(bugs)
    else:
        TerminalView(bugs)

    if args.open:
        BrowserView(bugs)


if __name__ == '__main__':
    sys.exit(launch())
