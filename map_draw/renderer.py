"""ASCII map rendering helpers."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Point:
    label: str
    x: float
    y: float


def load_points_from_csv(path: str | Path) -> list[Point]:
    """Load points from CSV using label,x,y or label,lat,lon columns."""
    csv_path = Path(path)
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    if not rows:
        return []

    first_row = rows[0]
    if {"label", "x", "y"} <= set(first_row):
        return [Point(row["label"], float(row["x"]), float(row["y"])) for row in rows]
    if {"label", "lat", "lon"} <= set(first_row):
        return [Point(row["label"], float(row["lon"]), float(row["lat"])) for row in rows]

    raise ValueError("CSV must contain label,x,y or label,lat,lon columns")


def scale_points(points: list[Point], width: int = 40, height: int = 20) -> list[tuple[Point, int, int]]:
    """Scale points into the inner drawable area of an ASCII grid."""
    if width < 4 or height < 4:
        raise ValueError("width and height must be at least 4")
    if not points:
        return []

    inner_width = width - 2
    inner_height = height - 2
    xs = [point.x for point in points]
    ys = [point.y for point in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    def scale(value: float, low: float, high: float, size: int) -> int:
        if high == low:
            return size // 2
        normalized = (value - low) / (high - low)
        return round(normalized * (size - 1))

    scaled: list[tuple[Point, int, int]] = []
    for point in points:
        col = 1 + scale(point.x, min_x, max_x, inner_width)
        row = 1 + scale(point.y, min_y, max_y, inner_height)
        scaled.append((point, col, row))
    return scaled


def _draw_line(canvas: list[list[str]], start: tuple[int, int], end: tuple[int, int]) -> None:
    x1, y1 = start
    x2, y2 = end
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        if canvas[y1][x1] == " ":
            canvas[y1][x1] = "*"
        if x1 == x2 and y1 == y2:
            break
        twice_err = 2 * err
        if twice_err > -dy:
            err -= dy
            x1 += sx
        if twice_err < dx:
            err += dx
            y1 += sy


def render_ascii_map(
    points: list[Point],
    width: int = 40,
    height: int = 20,
    draw_path: bool = False,
) -> str:
    """Render an ASCII map with border and legend."""
    if width < 4 or height < 4:
        raise ValueError("width and height must be at least 4")

    canvas = [[" " for _ in range(width)] for _ in range(height)]
    for row in range(height):
        for col in range(width):
            if row in {0, height - 1} and col in {0, width - 1}:
                canvas[row][col] = "+"
            elif row in {0, height - 1}:
                canvas[row][col] = "-"
            elif col in {0, width - 1}:
                canvas[row][col] = "|"

    scaled = scale_points(points, width=width, height=height)
    if draw_path and len(scaled) > 1:
        for (_, x1, y1), (_, x2, y2) in zip(scaled, scaled[1:]):
            _draw_line(canvas, (x1, height - 1 - y1), (x2, height - 1 - y2))

    legend_lines: list[str] = []
    for point, col, row in scaled:
        canvas[height - 1 - row][col] = point.label[:1].upper() or "?"
        legend_lines.append(f"{point.label[:1].upper()} = {point.label} ({point.x:.4f}, {point.y:.4f})")

    drawing = "\n".join("".join(row) for row in canvas)
    if legend_lines:
        return drawing + "\nLegend:\n" + "\n".join(legend_lines)
    return drawing + "\nLegend:\n(no points)"
