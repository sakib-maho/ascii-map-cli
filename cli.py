"""CLI for rendering ASCII maps from CSV coordinates."""

from __future__ import annotations

import argparse
from pathlib import Path

from map_draw.renderer import load_points_from_csv, render_ascii_map


def main() -> int:
    parser = argparse.ArgumentParser(description="Render an ASCII map from a CSV file.")
    parser.add_argument("--data", type=Path, required=True, help="CSV file with label,x,y or label,lat,lon.")
    parser.add_argument("--width", type=int, default=40, help="Total map width including border.")
    parser.add_argument("--height", type=int, default=16, help="Total map height including border.")
    parser.add_argument("--draw-path", action="store_true", help="Draw a path between points in file order.")
    args = parser.parse_args()

    points = load_points_from_csv(args.data)
    print(render_ascii_map(points, width=args.width, height=args.height, draw_path=args.draw_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
