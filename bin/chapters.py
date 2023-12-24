import argparse
import sys

def main():
    """Main driver."""
    args = parse_args()
    with open(args.filename, "r") as reader:
        in_chapter = False
        title = ""
        count = 0
        total = 0

        for line in reader:
            line = line.strip()
            if not line:
                continue

            if line.startswith("<section"):
                in_chapter = True

            elif line.startswith("##"):
                title = line.strip().split(maxsplit=1)[1]

            elif line.startswith("</section>"):
                in_chapter = False
                if count > 0:
                    if title:
                        title = f": {title}"
                    if args.details:
                        print(f"{count:6d}{title}")
                    total += count
                count = 0

            elif in_chapter:
                count += len(line.split())

            else:
                pass

    base = "" if args.base is None else f" ({total - args.base})"
    print(f"{total:6d}{base}")


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, default=None, help="book file")
    parser.add_argument("base", type=int, nargs="?", default=None, help="base count")
    parser.add_argument("--details", action="store_true", default=False, help="show details")
    return parser.parse_args()


if __name__ == "__main__":
    main()
