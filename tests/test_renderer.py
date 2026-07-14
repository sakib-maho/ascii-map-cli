from pathlib import Path
from subprocess import run

from map_draw.renderer import Point, load_points_from_csv, render_ascii_map, scale_points


FIXTURE = Path("data/sample_points.csv")


def test_load_points_from_lat_lon_csv() -> None:
    points = load_points_from_csv(FIXTURE)
    assert len(points) == 5
    assert points[0].label == "Dhaka"
    assert isinstance(points[0].x, float)


def test_scale_points_stays_inside_border() -> None:
    points = [
        Point("West", -10.0, 0.0),
        Point("Center", 0.0, 10.0),
        Point("East", 10.0, 20.0),
    ]
    scaled = scale_points(points, width=20, height=10)
    for _, col, row in scaled:
        assert 1 <= col <= 18
        assert 1 <= row <= 8


def test_render_contains_border_and_legend() -> None:
    drawing = render_ascii_map([Point("Alpha", 0.0, 0.0), Point("Beta", 10.0, 10.0)], width=16, height=8)
    lines = drawing.splitlines()
    assert lines[0].startswith("+")
    assert "Legend:" in drawing
    assert "A = Alpha" in drawing
    assert "B = Beta" in drawing


def test_render_draws_path() -> None:
    drawing = render_ascii_map(
        [Point("A", 0.0, 0.0), Point("B", 5.0, 5.0), Point("C", 10.0, 0.0)],
        width=18,
        height=8,
        draw_path=True,
    )
    assert "*" in drawing


def test_cli_renders_map() -> None:
    result = run(
        ["python3", "cli.py", "--data", "data/sample_points.csv", "--width", "24", "--height", "10"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "Legend:" in result.stdout
    assert "D = Dhaka" in result.stdout


def test_cli_draw_path_flag() -> None:
    result = run(
        ["python3", "cli.py", "--data", "data/sample_points.csv", "--draw-path"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "*" in result.stdout
