import argparse
from oom.exit_on_out_of_ram import exit_on_out_of_ram


def parse_args():
    # TODO: fill help
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'script',
        help='path to a script to execute with oom context.'
    )
    parser.add_argument(
        '-t', '--terminate-on',
        help='(megabytes)',
        type=float
    )
    parser.add_argument(
        '-nw', '--need-warning',
        help='',
        action='store_true',
        required=False
    )
    parser.add_argument(
        '-wo', '--warn-on',
        help='',
        type=int,
        required=False
    )
    parser.add_argument(
        '-we', '--warn-each',
        help='',
        type=int,
        required=False
    )
    parser.add_argument(
        '-s', '--sleep-time',
        help='',
        type=float,
        required=False
    )
    parser.add_argument(
        '-nau', '--notify-about-using',
        help='',
        action='store_true'
    )

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    exit_on_out_of_ram(
        terminate_on=int(args.terminate_on * 1024 * 1024),
        need_warning=args.need_warning,
        warn_on=args.warn_on,
        warn_each=args.warn_each if args.warn_each else 20,
        sleep_time=args.sleep_time if args.sleep_time else 0.5,
        notify_about_using=args.notify_about_using
    )
    with open(args.script, 'r') as f:
        script = f.read()
        exec(script, globals())


if __name__ == "__main__":
    main()
