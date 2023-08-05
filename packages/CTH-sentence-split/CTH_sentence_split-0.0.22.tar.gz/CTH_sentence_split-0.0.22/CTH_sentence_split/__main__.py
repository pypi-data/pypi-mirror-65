import argparse
from pkg import split, run_update


def choose():
    parser = argparse.ArgumentParser(prog="CTH_sentence_split")

    parser.add_argument('-s', '--split')
    # parser.add_argument('sentence', default="sentence")
    parser.add_argument('-u', '--update_dicts',
                        action='store_true', help='Update dictionaries')
    args = parser.parse_args()

    if args.split:
        split(args.split)
    elif args.update_dicts:
        run_update()
    else:
        parser.print_help()


if __name__ == "__main__":
    choose()
