"""StartinBlox commit style parser"""

import re
import ndebug
from typing import Tuple
from semantic_release.errors import UnknownCommitMessageStyleError
from semantic_release.history.parser_helpers import ParsedCommit, parse_text_block

debug = ndebug.create(__name__)

re_parser = re.compile(
    r'(?P<type>\w+)'
    r'(?:\((?P<scope>[\w _\-]+)\))?: '
    r'(?P<subject>[^\n]+)'
    r'(:?\n\n(?P<text>.+))?',
    re.DOTALL
)

MAJOR_TYPES = [
    'major',
]

MINOR_TYPES = [
    'minor',
]

NOTHING_TYPES = [
    'cicd',
    'doc'
]

def parse_commit_message(message: str) -> Tuple[int, str, str, Tuple[str, str, str]]:
    """
    Parses a commit message according to the StartinBlox release rules
    :param message: A string of the commit message
    :return: A tuple of (level to bump, type of change, scope of change, a tuple with descriptions)
    """

    try:
        # default to patch
        level_bump = 1
        _type = 'other'

        # parse message
        parsed = re_parser.match(message)

        # get the type of commit
        _type = parsed.group('type')

        # calculate release level
        if _type in NOTHING_TYPES:
            level_bump = 0

        if _type in MINOR_TYPES:
            level_bump = 2

        if _type in MAJOR_TYPES:
            level_bump = 3

        # get other elements of commit
        subject = parsed.group('subject')
        body, footer = parse_text_block(parsed.group('text'))

    except AttributeError:
        # if regex doesn't match make a patch with raw commit message
        subject = message.split("\n", 1)[0]
        try:
            body, footer = parse_text_block(message.split("\n", 1)[1])
        except IndexError:
            body = ''
            footer = ''

    if debug.enabled:
        debug('parse_commit_message -> ({}, {}, {})'.format(
            level_bump,
            _type,
            (subject, body, footer)
        ))

    return ParsedCommit(
        level_bump,
        _type,
        '',
        (subject, body, footer)
    )
