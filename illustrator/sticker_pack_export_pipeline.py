import os
import sys
import time
import shutil
import zipfile
import tkinter as tk
from tkinter import filedialog, simpledialog
import subprocess  # For launching the Photoshop script
import win32com.client
import pythoncom

# ------ For PDF generation ------
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

# ---- OpenCV, Numpy, PIL, and other libraries for video generation ----
import cv2
import numpy as np
import random
from math import ceil, sqrt
from PIL import Image, ImageDraw, ImageFont

####################################
# FOLDER STRUCTURE AND EXPORT (Baseline)
####################################
def generate_folder_structure(pack_name: str, root: str) -> dict:
    """
    Creates the folder structure:
    
    <root>/<pack_name>/
      ├─ SAMPLES/
      └─ <pack_name>/
         ├─ PNGs/ 
         │    ├─ 300x300
         │    ├─ 600x600
         │    └─ 1000x1000
         ├─ JPEGs/
         │    ├─ 300x300
         │    └─ 600x600
         ├─ Vectors/
         ├─ PDFs/
         ├─ LICENSE.txt
         └─ README.txt
    """
    outer_folder = os.path.join(root, pack_name)
    samples_folder = os.path.join(outer_folder, "SAMPLES")
    inner_pack_folder = os.path.join(outer_folder, pack_name)

    png_base = os.path.join(inner_pack_folder, "PNGs")
    png300 = os.path.join(png_base, "300x300")
    png600 = os.path.join(png_base, "600x600")
    png1000 = os.path.join(png_base, "1000x1000")

    jpeg_base = os.path.join(inner_pack_folder, "JPEGs")
    jpeg300 = os.path.join(jpeg_base, "300x300")
    jpeg600 = os.path.join(jpeg_base, "600x600")

    vectors_folder = os.path.join(inner_pack_folder, "Vectors")
    pdfs_folder = os.path.join(inner_pack_folder, "PDFs")

    folders = [outer_folder, samples_folder, inner_pack_folder,
               png_base, png300, png600, png1000,
               jpeg_base, jpeg300, jpeg600,
               vectors_folder, pdfs_folder]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

    return {
        "outer": outer_folder,
        "samples": samples_folder,
        "inner_pack": inner_pack_folder,
        "pngs": {"base": png_base, "300": png300, "600": png600, "1000": png1000},
        "jpegs": {"base": jpeg_base, "300": jpeg300, "600": jpeg600},
        "vectors": vectors_folder,
        "pdfs": pdfs_folder,
        "license": os.path.join(inner_pack_folder, "LICENSE.txt"),
        "readme": os.path.join(inner_pack_folder, "README.txt")
    }

def write_license_and_readme(inner_pack_folder: str, pack_name: str):
    license_text = (
        "Commercial Use License\n\n"
        "You MAY:\n"
        "✔ Use these assets in unlimited personal and commercial projects\n"
        "✔ Incorporate the stickers into products for sale\n"
        "✔ Modify, recolor, resize, or edit the icons for your specific needs\n\n"
        "You MAY NOT:\n"
        "✘ Resell, share, or redistribute the original files (even if modified)\n"
        "✘ Upload these assets to stock websites or AI training datasets\n\n"
        "This is a royalty-free, non-exclusive license.\n\n"
        "No attribution is required, but it is always appreciated.\n"
    )
    placeholder_readme = (
        "README for {pack_name} goes here.\n\n"
        "- Describe your pack contents\n"
        "- List file formats and sizes\n"
        "- Provide any usage notes or tips\n"
    ).format(pack_name=pack_name)
    with open(os.path.join(inner_pack_folder, "LICENSE.txt"), "w", encoding="utf-8") as f:
        f.write(license_text)
    with open(os.path.join(inner_pack_folder, "README.txt"), "w", encoding="utf-8") as f:
        f.write(placeholder_readme)

def convert_to_js_path(path: str) -> str:
    return path.replace("\\", "/")

####################################
# EXPORT FROM ILLUSTRATOR VIA JSX
####################################
def export_from_illustrator(outer_folder: str, inner_pack_name: str, prefix: str):
    """
    Exports sticker groups using Illustrator’s JavaScript.
    """
    jsx_script = r'''
    var prefix = "%%PREFIX%%";
    var packName = "%%INNER_PACK_NAME%%";
    
    function exportSectionA(outputFolder) {
        var origDoc = app.activeDocument;
        var groups = origDoc.groupItems;
        if (groups.length === 0) { alert("No groups found."); return; }
        var exportSize = 1000;
        var marginRatio = 0.05;
        var tempDoc = app.documents.add(DocumentColorSpace.RGB, exportSize, exportSize);
    
        for (var i = 0; i < groups.length; i++) {
            var idx = i + 1;
            var pad = (idx < 10 ? "0" : "") + idx;
            var baseName = prefix + "_1000x1000_" + pad;
            
            // Non-watermarked export
            var dupGroup = groups[i].duplicate(tempDoc, ElementPlacement.INSIDE);
            var b = dupGroup.geometricBounds;
            var groupWidth = b[2] - b[0];
            var groupHeight = b[1] - b[3];
            var margin = exportSize * marginRatio;
            var availW = exportSize - 2 * margin;
            var availH = exportSize - 2 * margin;
            var scaleFactor = Math.min(availW / groupWidth, availH / groupHeight) * 100;
            dupGroup.resize(scaleFactor, scaleFactor, true, true, true, true, scaleFactor);
            var nb = dupGroup.geometricBounds;
            var centerX = (nb[0] + nb[2]) / 2;
            var centerY = (nb[1] + nb[3]) / 2;
            dupGroup.translate(exportSize/2 - centerX, exportSize/2 - centerY);

            var pngPath = outputFolder + "/" + baseName + ".png";
            var pngOpts = new ExportOptionsPNG24();
            pngOpts.artBoardClipping = true;
            pngOpts.transparency = true;
            pngOpts.resolution = 300;
            pngOpts.horizontalScale = 100;
            pngOpts.verticalScale = 100;
            pngOpts.antiAliasing = true;
            tempDoc.exportFile(new File(pngPath), ExportType.PNG24, pngOpts);

            var svgName = prefix + "_svg_" + pad + ".svg";
            var svgPath = outputFolder + "/" + svgName;
            var svgOpts = new ExportOptionsSVG();
            svgOpts.embedRasterImages = true;
            tempDoc.exportFile(new File(svgPath), ExportType.SVG, svgOpts);

            dupGroup.remove();

            // Watermarked export
            var dupGroupWM = groups[i].duplicate(tempDoc, ElementPlacement.INSIDE);
            var bWM = dupGroupWM.geometricBounds;
            var groupWidthWM = bWM[2] - bWM[0];
            var groupHeightWM = bWM[1] - bWM[3];
            var marginWM = exportSize * marginRatio;
            var availWWM = exportSize - 2 * marginWM;
            var availHWM = exportSize - 2 * marginWM;
            var scaleFactorWM = Math.min(availWWM / groupWidthWM, availHWM / groupHeightWM) * 100;
            dupGroupWM.resize(scaleFactorWM, scaleFactorWM, true, true, true, true, scaleFactorWM);
            var nbWM = dupGroupWM.geometricBounds;
            var centerXWM = (nbWM[0] + nbWM[2]) / 2;
            var centerYWM = (nbWM[1] + nbWM[3]) / 2;
            dupGroupWM.translate(exportSize/2 - centerXWM, exportSize/2 - centerYWM);

            // Add generic watermark text
            var wm = tempDoc.textFrames.add();
            wm.contents = "YOUR_WATERMARK";
            wm.textRange.size = 100;
            wm.opacity = 20;
            var bwm = wm.geometricBounds;
            var cw = bwm[2] - bwm[0];
            var targetW = exportSize * 0.9;
            var sc = (targetW / cw) * 100;
            wm.resize(sc, sc, true, true, true, true, sc);
            var bb = wm.geometricBounds;
            var wmCenX = (bb[0] + bb[2]) / 2;
            var wmCenY = (bb[1] + bb[3]) / 2;
            wm.translate(exportSize/2 - wmCenX, exportSize/2 - wmCenY);

            var wmName = prefix + "_" + exportSize + "x" + exportSize + "_" + pad + "_watermark.png";
            var wmPath = outputFolder + "/" + wmName;
            var wmOpts = new ExportOptionsPNG24();
            wmOpts.artBoardClipping = true;
            wmOpts.transparency = true;
            wmOpts.resolution = 300;
            wmOpts.horizontalScale = 100;
            wmOpts.verticalScale = 100;
            wmOpts.antiAliasing = true;
            tempDoc.exportFile(new File(wmPath), ExportType.PNG24, wmOpts);

            wm.remove();
            dupGroupWM.remove();
        }
        tempDoc.close(SaveOptions.DONOTSAVECHANGES);
    }

    function exportSectionB(outputFolder) {
        var origDoc = app.activeDocument;
        var groups = origDoc.groupItems;
        if (groups.length === 0) { alert("No groups found."); return; }
        var exportSizeJPEG = 600;
        var marginRatio = 0.05;
        var tempDoc = app.documents.add(DocumentColorSpace.RGB, exportSizeJPEG, exportSizeJPEG);

        for (var i = 0; i < groups.length; i++) {
            var idx = i + 1;
            var pad = (idx < 10 ? "0" : "") + idx;
            var baseName = prefix + "_600x600_" + pad;

            var dupGroup = groups[i].duplicate(tempDoc, ElementPlacement.INSIDE);
            var b = dupGroup.geometricBounds;
            var groupWidth = b[2] - b[0];
            var groupHeight = b[1] - b[3];
            var margin = exportSizeJPEG * marginRatio;
            var availW = exportSizeJPEG - 2 * margin;
            var availH = exportSizeJPEG - 2 * margin;
            var scaleFactor = Math.min(availW / groupWidth, availH / groupHeight) * 100;
            dupGroup.resize(scaleFactor, scaleFactor, true, true, true, true, scaleFactor);
            var nb = dupGroup.geometricBounds;
            var centerX = (nb[0] + nb[2]) / 2;
            var centerY = (nb[1] + nb[3]) / 2;
            dupGroup.translate(exportSizeJPEG/2 - centerX, exportSizeJPEG/2 - centerY);

            var jpgPath = outputFolder + "/" + baseName + ".jpg";
            var jpgOpts = new ExportOptionsJPEG();
            jpgOpts.artBoardClipping = true;
            jpgOpts.qualitySetting = 70;
            jpgOpts.horizontalScale = 100;
            jpgOpts.verticalScale = 100;
            jpgOpts.antiAliasing = true;
            tempDoc.exportFile(new File(jpgPath), ExportType.JPEG, jpgOpts);

            dupGroup.remove();
        }
        tempDoc.close(SaveOptions.DONOTSAVECHANGES);
    }

    exportSectionA("%%OUTPUT_FOLDER%%");
    exportSectionB("%%OUTPUT_FOLDER%%");
    '''
    js_out = convert_to_js_path(outer_folder)
    final_jsx = jsx_script.replace("%%OUTPUT_FOLDER%%", js_out)
    final_jsx = final_jsx.replace("%%PREFIX%%", prefix)
    final_jsx = final_jsx.replace("%%INNER_PACK_NAME%%", inner_pack_name)
    try:
        illustrator = win32com.client.GetActiveObject("Illustrator.Application")
    except Exception:
        print("Illustrator not running. Please open Illustrator and try again.")
        sys.exit(1)
    illustrator.DoJavaScript(final_jsx)
    time.sleep(2)
    pythoncom.CoUninitialize()

####################################
# RESIZE EXPORTS VIA PYTHON
####################################
def resize_exports(export_dir):
    from PIL import Image
    try:
        resample_filter = Image.Resampling.LANCZOS
    except AttributeError:
        resample_filter = Image.ANTIALIAS

    for filename in os.listdir(export_dir):
        lower = filename.lower()
        full_path = os.path.join(export_dir, filename)
        if os.path.isfile(full_path):
            if "1000x1000" in lower and "watermark" not in lower and lower.endswith(".png"):
                try:
                    with Image.open(full_path) as im:
                        im_600 = im.resize((600,600), resample_filter)
                        new_filename_600 = filename.replace("1000x1000", "600x600")
                        im_600.save(os.path.join(export_dir, new_filename_600))
                        im_300 = im.resize((300,300), resample_filter)
                        new_filename_300 = filename.replace("1000x1000", "300x300")
                        im_300.save(os.path.join(export_dir, new_filename_300))
                except Exception as e:
                    print(f"Failed to resize {filename}: {e}")
            if "600x600" in lower and lower.endswith((".jpg", ".jpeg")):
                try:
                    with Image.open(full_path) as im:
                        im_300 = im.resize((300,300), resample_filter)
                        new_filename_300 = filename.replace("600x600", "300x300")
                        im_300.save(os.path.join(export_dir, new_filename_300))
                except Exception as e:
                    print(f"Failed to resize {filename}: {e}")

####################################
# ORGANIZATION STAGE (Python)
####################################
def organize_exports(outer_folder: str, folders: dict):
    for file in os.listdir(outer_folder):
        src = os.path.join(outer_folder, file)
        if not os.path.isfile(src):
            continue
        fname = file.lower()
        if fname.endswith(".svg"):
            dst = os.path.join(folders["vectors"], file)
        elif fname.endswith((".jpg", ".jpeg")):
            if "300x300" in fname:
                dst = os.path.join(folders["jpegs"]["300"], file)
            elif "600x600" in fname:
                dst = os.path.join(folders["jpegs"]["600"], file)
            else:
                dst = os.path.join(folders["jpegs"]["base"], file)
        elif fname.endswith(".png"):
            if "watermark" in fname:
                dst = os.path.join(folders["samples"], file)
            else:
                if "300x300" in fname:
                    dst = os.path.join(folders["pngs"]["300"], file)
                elif "600x600" in fname:
                    dst = os.path.join(folders["pngs"]["600"], file)
                elif "1000x1000" in fname:
                    dst = os.path.join(folders["pngs"]["1000"], file)
                else:
                    dst = os.path.join(folders["pngs"]["base"], file)
        else:
            continue
        try:
            shutil.move(src, dst)
        except Exception as e:
            print("Failed to move", file, e)

####################################
# PDF GENERATION STAGE
####################################
def create_sticker_sheet_pdf(
    image_folder,
    output_pdf_path,
    stickers_per_row=4,
    padding=20,
    include_cut_lines=True,
    cut_line_shape="square",
    include_registration_marks=False,
    bleed_margin=5,
    shop_name="YOUR_SHOP_NAME",
    top_label="YOUR_BRAND",
    sub_label="Sticker Pack",
    theme_color=colors.lavender
):
    page_width, page_height = A4
    image_files = sorted([f for f in os.listdir(image_folder) if f.lower().endswith(".png")])
    c = canvas.Canvas(output_pdf_path, pagesize=A4)
    def draw_header():
        c.setFillColor(theme_color)
        c.rect(0, page_height - 60, page_width, 60, stroke=0, fill=1)
        c.setFillColor(colors.darkslategray)
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(page_width / 2, page_height - 35, top_label)
        c.setFont("Helvetica", 12)
        c.drawCentredString(page_width / 2, page_height - 50, sub_label)
    def draw_footer():
        c.setFillColor(theme_color)
        c.rect(0, 0, page_width, 40, stroke=0, fill=1)
        c.setFont("Helvetica", 9)
        c.setFillColor(colors.darkslategray)
        c.drawCentredString(page_width / 2, 15, f"Find more designs at: YOUR_URL_HERE")
    def draw_registration_marks():
        mark_size = 10
        offset = 15
        c.setStrokeColor(colors.black)
        c.setLineWidth(1)
        # (lines omitted for brevity)

    # (layout and drawing logic continues as before)
    draw_header()
    # ... draw stickers and pages ...
    draw_footer()
    if include_registration_marks:
        draw_registration_marks()
    c.save()

####################################
# ZIP STAGE
####################################
def zip_final(inner_pack_folder: str):
    base_folder = os.path.dirname(inner_pack_folder)
    pack_name = os.path.basename(inner_pack_folder)
    zip_name = f"{pack_name}.zip"
    zip_path = os.path.join(base_folder, zip_name)
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(inner_pack_folder):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, start=inner_pack_folder)
                zipf.write(full_path, arcname=rel_path)
    print(f"✅ Created ZIP: {zip_path}")

####################################
# VIDEO GENERATION STAGE
####################################
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1080
FPS = 24
COLLAGE_DURATION = 10
COLLAGE_FRAMES = FPS * COLLAGE_DURATION
ANIM_DURATION = FPS
FADE_DURATION = FPS
TEXT_SEGMENT_DURATION = 2
TEXT_SEGMENT_FRAMES = FPS * TEXT_SEGMENT_DURATION
IMG_WIDTH, IMG_HEIGHT = 300, 300
FUN_FONT_PATH = r"C:\Windows\Fonts\comic.ttf"

def load_and_resize(image_path, size=(IMG_WIDTH, IMG_HEIGHT)):
    # (same as before)

def overlay_image_alpha(background, overlay, x, y):
    # (same as before)

def draw_text_with_opacity(frame, text, font, opacity):
    # (same as before)

def create_collage_video(image_folder, output_video_path):
    # (same as before, but watermark/logo text removed)

####################################
# MAIN PIPELINE (Combined)
####################################
def main_pipeline():
    pythoncom.CoInitialize()
    root_tk = tk.Tk()
    root_tk.withdraw()
    root_folder = filedialog.askdirectory(title="Select your Root Folder")
    if not root_folder:
        print("No folder selected. Exiting.")
        sys.exit(1)
    pack_name = simpledialog.askstring("Pack Name", "Enter the name of your pack:")
    if not pack_name:
        print("No pack name provided. Exiting.")
        sys.exit(1)
    var_prefix = pack_name.replace(" ", "").lower()[:3]
    folders = generate_folder_structure(pack_name, root_folder)
    write_license_and_readme(folders["inner_pack"], pack_name)
    
    export_from_illustrator(
        outer_folder=folders["outer"],
        inner_pack_name=pack_name,
        prefix=var_prefix
    )
    
    resize_exports(folders["outer"])
    organize_exports(folders["outer"], folders)
    
    png300_folder = folders["pngs"]["300"]
    cricut_pdf = os.path.join(folders["pdfs"], "StickerSheet_Cricut.pdf")
    silhouette_pdf = os.path.join(folders["pdfs"], "StickerSheet_Silhouette.pdf")
    create_sticker_sheet_pdf(
        image_folder=png300_folder,
        output_pdf_path=cricut_pdf,
        include_cut_lines=True,
        cut_line_shape="square",
        include_registration_marks=False
    )
    create_sticker_sheet_pdf(
        image_folder=png300_folder,
        output_pdf_path=silhouette_pdf,
        include_cut_lines=True,
        cut_line_shape="square",
        include_registration_marks=True
    )
    
    zip_final(folders["inner_pack"])
    
    video_output_path = os.path.join(folders["outer"], f"{pack_name}.mp4")
    create_collage_video(folders["pngs"]["300"], video_output_path)
    
    run_photoshop_script = True
    if run_photoshop_script:
        num_items = min(25, len([f for f in os.listdir(folders["pngs"]["300"]) if f.lower().endswith(".png")]))
        photoshop_script_path = os.path.join(os.path.dirname(__file__), "photoshopScript.py")
        psd_save_folder = folders["outer"]
        cmd = [
            sys.executable,
            photoshop_script_path,
            "--png_folder", folders["pngs"]["300"],
            "--pack_name", pack_name,
            "--num_items", str(num_items),
            "--psd_save_path", psd_save_folder
        ]
        print("Running Photoshop script for cover creation...")
        subprocess.run(cmd)
    
    os.startfile(folders["outer"])
    pythoncom.CoUninitialize()

if __name__ == "__main__":
    main_pipeline()
