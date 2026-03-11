# Adobe-Script-Toolkit

ExtendScript (JSX) and Python scripts for automating Adobe Illustrator and After Effects — batch operations, export pipelines, layer management, and render automation.

---

## What's in here

| Folder | Contents |
|--------|----------|
| `illustrator/` | JSX scripts + Python pipeline for Illustrator — sticker pack export, batch artboard export, vectorize, layer automation |
| `after-effects/` | JSX scripts for After Effects — render queue automation, layer control, expression helpers |

---

## Illustrator Scripts

### `illustrator/sticker_pack_export_pipeline.py` ★
Full end-to-end sticker pack export pipeline — Python drives Illustrator via COM (win32com), with an embedded JSX script executing inside Illustrator to export each group item. Handles the entire commercial release workflow:

- Exports every sticker group at **1000×1000 PNG**, **600×600 JPEG**, and **SVG vector** formats
- Generates **watermarked preview samples** for each sticker (separate transparent overlay pass)
- **Resizes** all exports down to 300×300 and 600×600 derivatives via Pillow
- **Organises** all outputs into a clean commercial folder structure (`PNGs/300x300/`, `JPEGs/600x600/`, `Vectors/`, `PDFs/`, `SAMPLES/`)
- Generates **printable sticker sheet PDFs** with cut lines and optional registration marks (Cricut + Silhouette versions) via ReportLab
- Creates a **promotional collage video** (MP4) from the 300×300 thumbnails via OpenCV
- **Zips** the final pack ready for marketplace upload
- Optionally chains to a Photoshop script for cover image generation

```
pip install -r requirements.txt
python illustrator/sticker_pack_export_pipeline.py
```

> Requires Illustrator to be running. A Tkinter dialog will prompt for root folder and pack name.

---

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
- **Python + win32com** — drives Illustrator headlessly via COM, with inline JSX injected at runtime for full Illustrator API access
- **Pillow / OpenCV / ReportLab** — image resizing, video generation, and PDF sticker sheet creation in the export pipeline

---

## Author

**Naadir** · [Portfolio](https://naadir-dev-portfolio.github.io) · [GitHub](https://github.com/Naadir-Dev-Portfolio)
