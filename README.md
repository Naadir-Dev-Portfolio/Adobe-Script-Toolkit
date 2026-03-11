# Adobe-Script-Toolkit

ExtendScript (JSX) and Python scripts for automating Adobe Illustrator and After Effects — batch operations, export pipelines, layer management, and render automation.

---

## What's in here

| Folder | Contents |
|--------|----------|
| `illustrator/` | JSX scripts for Illustrator — batch export, artboard management, layer automation |
| `after-effects/` | JSX scripts for After Effects — render queue automation, layer control, expression helpers |

---

## Illustrator Scripts

### `illustrator/batch_export_artboards.jsx`
Exports every artboard in the active document as an individual PNG/SVG/PDF — auto-named by artboard name. Configurable output format, scale, and destination folder.

```
Run via: File → Scripts → Other Script → select .jsx
```

### `illustrator/rename_layers_sequential.jsx`
Renames all layers in the active document sequentially (`Layer_01`, `Layer_02`, ...). Useful for batch artwork where consistent layer naming is required downstream.

### `illustrator/vectorize_and_export.jsx`
Applies Image Trace (Live Trace) to all raster objects in the document, expands them to vectors, and exports the result. Automates the manual trace → expand → export workflow.

---

## After Effects Scripts

### `after-effects/batch_render_queue.jsx`
Adds all open compositions to the render queue with a consistent output template and fires the render. Removes the repetitive manual queue-building step when rendering multiple comps.

### `after-effects/toggle_layer_visibility.jsx`
Toggles visibility on a named layer across all compositions in the project — useful when swapping placeholder/watermark layers before final render.

### `after-effects/set_comp_settings.jsx`
Applies uniform settings (resolution, framerate, duration) across all compositions. One script instead of manually editing every comp.

---

## How to run

**Illustrator / After Effects JSX scripts:**
1. Open the target document in Illustrator or After Effects
2. Go to `File → Scripts → Other Script...`
3. Navigate to the `.jsx` file and open it

**Or set up a keyboard shortcut:**
`Edit → Keyboard Shortcuts → Scripts` — assign any `.jsx` to a hotkey for one-press execution.

---

## Tech

- **ExtendScript (JSX)** — Adobe's scripting layer (ES3-based), runs natively in Illustrator and After Effects without any install
- **Python** (where noted) — for file system operations and pipeline glue where ExtendScript can't reach

---

## Author

**Naadir** · [Portfolio](https://naadir-dev-portfolio.github.io) · [GitHub](https://github.com/Naadir-Dev-Portfolio)
