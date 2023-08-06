#!python
"""
    @copyright: 2020 Lari Huttunen
    @license: MIT <http://www.opensource.org/licenses/mit-license.php>
"""
import argparse
import argunizer.shaker as shaker


def main():
    parser = argparse.ArgumentParser(description="Create and maintain a hierarchical timeline through moving the source files in place.")
    parser.add_argument("src_dir", help="The source directory to walk through.")
    parser.add_argument("dst_dir", help="The destination directory for the timeline and moved files.")
    parser.add_argument("-v", "--verbose", help="Show INFO level messages.", action="store_true")
    parser.add_argument("-d", "--debug", help="Show DEBUG level messages.", action="store_true")
    parser.add_argument("--dryrun", help="Don't actually perform the timeline creation.", action="store_true")
    args = parser.parse_args()

    move_run = shaker.Argunizer(spath=args.src_dir, dpath=args.dst_dir, semantics="move", dryrun=args.dryrun, verbose=args.verbose, debug=args.debug)
    move_run.walk()
    move_run.execute()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("INFO: Script interrupted via CTRL-C.")
