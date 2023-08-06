#!python
"""
    @copyright: 2020 Lari Huttunen
    @license: MIT <http://www.opensource.org/licenses/mit-license.php>
"""
import argparse
import argunizer.shaker as shaker


def main():
    parser = argparse.ArgumentParser(description="Clean up the source directory.")
    parser.add_argument("src_dir", help="The source directory to empty of ALL files and directories.")
    parser.add_argument("-v", "--verbose", help="Show INFO level messages.", action="store_true")
    parser.add_argument("-d", "--debug", help="Show DEBUG level messages.", action="store_true")
    parser.add_argument("--execute", help="Actually perform the clean-up.", action="store_true")
    args = parser.parse_args()

    if args.execute:
        dryrun = False
    else:
        dryrun = True
    cleanup_run = shaker.Argunizer(spath=args.src_dir, semantics="move", dryrun=dryrun, verbose=args.verbose, debug=args.debug)
    cleanup_run.clean()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("INFO: Script interrupted via CTRL-C.")
