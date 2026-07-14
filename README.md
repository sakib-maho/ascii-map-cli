# ASCII Map CLI

`ascii-map-cli` turns simple coordinate CSV files into terminal-friendly maps. It
supports both generic world coordinates and geographic `lat`/`lon` inputs, scales
them into a fixed grid, and prints a compact legend for readability.

## Features

- Load `label,x,y` or `label,lat,lon` CSV files
- Auto-scale real-world coordinates into an ASCII canvas
- Draw a border around the map for clearer framing
- Render point labels using the first character of each label
- Print a legend with the original coordinates
- Optionally draw a route between points in CSV order

## Sample Data

The bundled sample file uses Bangladesh city coordinates:

```csv
label,lat,lon
Dhaka,23.8103,90.4125
Sylhet,24.8949,91.8687
Chattogram,22.3569,91.7832
```

## CLI Usage

```bash
python3 cli.py --data data/sample_points.csv
python3 cli.py --data data/sample_points.csv --width 60 --height 18
python3 cli.py --data data/sample_points.csv --draw-path
```

Example output:

```text
+--------------------------------------+
|            S                         |
|                                      |
| D                                C   |
+--------------------------------------+
Legend:
D = Dhaka (90.4125, 23.8103)
S = Sylhet (91.8687, 24.8949)
C = Chattogram (91.7832, 22.3569)
```

## Python API

```python
from map_draw.renderer import load_points_from_csv, render_ascii_map

points = load_points_from_csv("data/sample_points.csv")
print(render_ascii_map(points, width=40, height=12, draw_path=True))
```

## Run Tests

```bash
python3 -m pytest -q
```

## License

MIT. See `LICENSE`.
