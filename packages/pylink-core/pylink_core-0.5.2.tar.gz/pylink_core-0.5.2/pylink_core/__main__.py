_HELP_TEXT = """
klink app-path user-path pio-path
"""

if __name__ == "__main__":
    from .klink import *
    argv = sys.argv[1:]
    parser = argparse.ArgumentParser(description=_HELP_TEXT)
    parser.add_argument('app', nargs='?', default=None)
    parser.add_argument('user', nargs='?', default=None)
    parser.add_argument('pio', nargs='?', default=None)
    args = parser.parse_args(argv)
    def fakeCallback(method, *params):
        if method != 'log':
            print("UI [%s] [%s]" %(method, params))
    klinkServe(args, fakeCallback)