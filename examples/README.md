# Examples

This directory contains small scripts demonstrating some of DevilutionX's subsystems.

- `tile_renderer_demo.py` – showcases simple isometric tile rendering and a
  movable player using Pygame.

## Requirements

The demo relies on the `pygame` package. Install it with:

```bash
pip install pygame
```

Then run the script:

```bash
python3 examples/tile_renderer_demo.py
```

When testing in a headless environment set `SDL_VIDEODRIVER=dummy`. The demo
detects this and quits automatically after a couple of seconds.


