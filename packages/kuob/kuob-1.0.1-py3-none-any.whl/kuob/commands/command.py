import sys

from kuob.api import Api


class Command:

    def __init__(self, args, config, env):
        self.quiet = False
        self.api = Api(config.api_url, env.get("USER"), config.install_id)

    def print(self, text, file=sys.stdout, end="\n", force=False):
        if not self.quiet or force:
            print(text, file=file, end=end)

    def print_info(self, text):
        self.print("\x1b[0;32mkuob: %s\x1b[0m" % text)

    def print_warning(self, text):
        self.print("\x1b[0;33mkuob: %s\x1b[0m" % text)

    def print_error(self, text):
        self.print("\x1b[0;31mkuob: %s\x1b[0m" % text, file=sys.stderr, force=True)
