#!/usr/bin/env python3
"""Sample clean SciTeX script — zero lint issues."""

import scitex as stx


@stx.session
def main(data_path="./data.csv", threshold=0.5):
    """Demonstrate a clean SciTeX script pattern."""
    df = stx.io.load(data_path)
    stx.io.save(df, "./processed.csv")
    return 0


if __name__ == "__main__":
    main()
