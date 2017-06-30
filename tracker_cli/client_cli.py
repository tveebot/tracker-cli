"""
Episode Tracker

Usage:
  episode-tracker add <id> [ --url=<daemon_url> ]
  episode-tracker rm <id> [ --url=<daemon_url> ]
  episode-tracker list [ --url=<daemon_url> ]
  episode-tracker (-h | --help)

Options:
  --url=<daemon_url>    The URL to reach the daemon [default: http://localhost:30014]
  -h --help             Show this screen.
  --version             Show version.

"""
import logging
from contextlib import contextmanager

from beautifultable import BeautifulTable
from docopt import docopt

from tracker_cli.client import Client, RequestError, ServerError

version = 'Episode Tracker CLI: Version 0.2'

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

daemon_url = None


def main():
    args = docopt(__doc__, version=version)

    global daemon_url
    daemon_url = args['--url']

    # Setup the client
    client = Client(daemon_url)

    if args['add']:
        with display_errors("add"):
            added_tvshow = client.add_tvshow(args['<id>'])
            logger.info("TV Show '%s' is now being tracked" % added_tvshow.name)

    elif args['rm']:
        with display_errors("rm"):
            client.remove_tvshow(args['<id>'])
            logger.info("TV Show with ID '%s' is no longer being tracked" % args['<id>'])

    elif args['list']:
        with display_errors("list"):
            tvshows = client.tvshows()

            if len(tvshows) == 0:
                logger.warning("There is no TV Shows being tracked yet")
                logger.info("Use the 'add' command to start tracking a TV Show")
                logger.info("Use the '-h' option to learn more")

            else:
                table = BeautifulTable()
                table.column_headers = ("ID", "NAME")
                for tvshow in tvshows:
                    table.append_row((tvshow.id, tvshow.name))

                logger.info(table)


@contextmanager
def display_errors(command_name: str):

    try:
        yield

    except RequestError as error:
        logger.error("Command '%s' failed" % command_name)
        logger.error(str(error))

    except ConnectionError as error:
        logger.error("Command '%s' failed due to a connection error" % command_name)
        logger.error("Was unable to connect to daemon at %s: %s" % (daemon_url, str(error)))

    except ServerError as error:
        logger.error("Command '%s' failed due to a SERVER ERROR: %s " % (command_name, str(error)))
