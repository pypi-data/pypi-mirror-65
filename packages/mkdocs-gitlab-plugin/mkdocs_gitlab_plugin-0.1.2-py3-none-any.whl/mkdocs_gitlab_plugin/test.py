
import sys

from plugin import GitlabLinksPlugin

if __name__ == '__main__':
    plugin = GitlabLinksPlugin()
    plugin.load_config({})
    print(plugin.on_page_markdown(sys.stdin.read()))

