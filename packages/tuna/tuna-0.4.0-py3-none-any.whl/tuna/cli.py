import argparse
import os.path
import shutil
import threading
import webbrowser

from .__about__ import __version__
from .main import read, render, start_server


def main(argv=None):
    parser = _get_parser()
    args = parser.parse_args(argv)

    if args.outdir:
        data = read(args.infile)
        if not os.path.exists(args.outdir):
            os.makedirs(args.outdir)
        with open(os.path.join(args.outdir, "index.html"), "wt") as out:
            out.write(render(data, args.infile))
        this_dir = os.path.dirname(__file__)
        static_dir = os.path.join(args.outdir, "static")
        if os.path.exists(static_dir):
            shutil.rmtree(static_dir)
        shutil.copytree(os.path.join(this_dir, "web", "static"), static_dir)
        if args.browser:
            threading.Thread(
                target=lambda: webbrowser.open_new_tab(
                    os.path.join(args.outdir, "index.html")
                )
            ).start()
    else:
        start_server(args.infile, args.browser, args.port)


def _get_parser():
    """Parse input options."""
    parser = argparse.ArgumentParser(description=("Visualize Python profile."))

    parser.add_argument("infile", type=str, help="input runtime or import profile file")
    parser.add_argument(
        "-o",
        "--outdir",
        default=None,
        type=str,
        help="output directory for static files "
        "(no server is started if outdir is specified)",
    )

    parser.add_argument(
        "--no-browser",
        default=True,
        dest="browser",
        action="store_false",
        help="Don't start a web browser (default: do start)",
    )

    parser.add_argument(
        "--port",
        "-p",
        default=None,
        type=int,
        help="Webserver port (default: first free port from 8000)",
    )

    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version="%(prog)s " + (f"(version {__version__})"),
    )
    return parser
