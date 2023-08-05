import argparse
import os
import sys

from . import parsing
from . import CONFIG


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(description="Calculate optical cavity parameters.")
    # add all the available arguments
    parsing.add_parser_arguments(parser)
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    # parse the args provided into a Namespace
    args = parser.parse_args()
    # if any plotting needs doing, then handle style initialisations here
    if args.semilogx or args.semilogy or args.loglog:
        args.plot = True
    if args.loglog:
        args.semilogx = True
        args.semilogy = True
    if args.plot:
        if "plotting" in CONFIG:
            import matplotlib

            plotting_conf = CONFIG["plotting"]

            backend = plotting_conf.get("matplotlib_backend", "")
            if backend:
                matplotlib.use(backend)

            import matplotlib.pyplot as plt

            style = plotting_conf.get("style", "")
            if not style:
                plt.style.use(
                    os.path.join(
                        os.path.split(os.path.realpath(__file__))[0],
                        "_default.mplstyle",
                    )
                )
            else:
                plt.style.use(style)

    # now perform the task the user requires
    parsing.handle_parser_namespace(args)


if __name__ == "__main__":
    main()
