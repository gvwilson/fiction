#!/usr/bin/env python

import sys

def main():
    assert len(sys.argv) == 3, "Usage: diffset actual expected"
    actual = read(sys.argv[1])
    expected = read(sys.argv[2])
    report("unknown", actual - expected)
    report("unused", expected - actual)


def read(filename):
    if filename == "-":
        lines = sys.stdin.readlines()
    else:
        with open(filename, "r") as reader:
            lines = reader.readlines()
    lines = [x.strip() for x in lines]
    lines = [x[:-2] if x[-2:] == "'s" else x for x in lines]
    return set([x for x in lines if x])


def report(title, words):
    if not words: return
    print(title)
    for w in sorted(words):
        print(f"- {w}")


if __name__ == "__main__":
    main()
