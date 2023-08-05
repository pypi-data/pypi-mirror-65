#!/usr/bin/python3

import re
import mkdocs

from mkdocs.config import Config
from mkdocs.plugins import BasePlugin

class GitlabLinksPlugin(BasePlugin):
    '''
    Transform handles such as #1234, %56, !789, &12 or $34 into links to a gitlab repository.
    Before the #/%/!/&/$ is needed either a space or a '(' or '['.
    '''

    config_scheme = (
        ('gitlab_url', mkdocs.config.config_options.Type(mkdocs.utils.string_types, default='http://gitlab.com/XXX')),
        ('verbose', mkdocs.config.config_options.Type(bool, default=False))
    )

    TOKEN_PATHS = {
        '#': 'issues/',
        '!': 'merge_requests/',
        '%': 'milestones/',
        '&': 'epics/',
        '$': 'snippets/',
        }

    BEFORE = r'([\s\(\[])'
    TOKEN = '([' + ''.join(TOKEN_PATHS.keys()) + '])'
    REF = r'(\d+)'

    GITLAB_LINK = re.compile(BEFORE + TOKEN + REF, re.UNICODE)

    def _decorate_link(self, match):
        
        try:
            before, token, ref = match.groups()
            token_path = self.TOKEN_PATHS[token]
        except:
            print("! Error in transforming: ", match.group())

        # Build the link
        link = self.config['gitlab_url'] + '/' + token_path + ref
        linked = before + "[%s](%s)" % (token + ref, link)
        
        if self.config['verbose']:
            print(match.group(), '-->', linked)

        return linked

    def on_page_markdown(self, markdown, page=None, config=None, **kwargs):
        return re.sub(self.GITLAB_LINK, self._decorate_link, markdown)
