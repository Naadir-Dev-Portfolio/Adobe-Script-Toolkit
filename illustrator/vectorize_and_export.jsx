/**
 * Vectorize & Export
 * ------------------
 * Applies Image Trace to all raster images in the document,
 * expands them to live vectors, then exports the result as SVG.
 *
 * How to run: File > Scripts > Other Script > select this file
 */

(function () {

    var PRESET = "High Fidelity Photo";   // Image Trace preset name
    var OUTPUT_FORMAT = "SVG";            // "SVG" | "PNG"

    // -------------------------------------------------------

    var doc = app.activeDocument;
    if (!doc) { alert("No document open."); return; }

    var destFolder = Folder.selectDialog("Choose export folder for vectorized output");
    if (!destFolder) return;

    // Select all raster items
    var rasters = doc.rasterItems;
    if (rasters.length === 0) {
        alert("No raster images found in this document.");
        return;
    }

    var count = 0;

    for (var i = rasters.length - 1; i >= 0; i--) {
        var raster = rasters[i];
        try {
            // Select the raster item
            doc.selection = null;
            raster.selected = true;

            // Apply Image Trace
            app.executeMenuCommand("Live Trace");

            // Expand to editable vectors
            app.executeMenuCommand("Expand");

            count++;

        } catch (e) {
            $.writeln("Could not trace item " + i + ": " + e.message);
        }
    }

    // Export the document
    var safeName = doc.name.replace(/\.[^.]+$/, "").replace(/[\/\\:*?"<>|]/g, "_");
    var filePath = destFolder.fsName + "/" + safeName + "_vectorized";

    if (OUTPUT_FORMAT === "SVG") {
        var svgOpts = new ExportOptionsSVG();
        svgOpts.embedRasterImages = false;
        doc.exportFile(new File(filePath + ".svg"), ExportType.SVG, svgOpts);
    } else {
        var pngOpts = new ExportOptionsPNG24();
        pngOpts.transparency = true;
        pngOpts.horizontalScale = 200;
        pngOpts.verticalScale = 200;
        doc.exportFile(new File(filePath + ".png"), ExportType.PNG24, pngOpts);
    }

    alert("Vectorized " + count + " raster items.\nExported to: " + destFolder.fsName);

})();
