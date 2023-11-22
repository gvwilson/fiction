import sys

USAGE = "Usage: chapters.py [-t] filename"

if len(sys.argv) == 1:
    print(USAGE)
    sys.exit(0)

if len(sys.argv) == 2:
    filename = sys.argv[1]
    details = True
elif (len(sys.argv) == 3) and (sys.argv[1] == "-t"):
    filename = sys.argv[2]
    details = False
else:
    print(USAGE)
    sys.exit(1)

with open(filename, "r") as reader:
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
                if details:
                    print(f"{count:6d}{title}")
                total += count
            count = 0

        elif in_chapter:
            count += len(line.split())

        else:
            pass

print(f"{total:6d}")
