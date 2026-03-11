/**
 * Batch Export Artboards
 * ----------------------
 * Exports every artboard in the active Illustrator document as a separate file.
 * Supported formats: PNG, SVG, PDF
 *
 * How to run: File > Scripts > Other Script > select this file
 */

(function () {

    var CONFIG = {
        format: "PNG",          // "PNG" | "SVG" | "PDF"
        scale: 2,               // Export scale (2 = @2x / 200%)
        resolution: 150,        // PNG resolution (DPI)
        outputFolder: ""        // Leave empty to prompt user
    };

    // -------------------------------------------------------

    var doc = app.activeDocument;
    if (!doc) { alert("No document open."); return; }

    // Pick output folder
    var destFolder;
    if (CONFIG.outputFolder) {
        destFolder = new Folder(CONFIG.outputFolder);
    } else {
        destFolder = Folder.selectDialog("Choose export destination folder");
        if (!destFolder) return;
    }

    var artboards = doc.artboards;
    var total = artboards.length;
    var exported = 0;

    for (var i = 0; i < total; i++) {
        artboards.setActiveArtboardIndex(i);
        var ab = artboards[i];
        var name = ab.name.replace(/[\/\\:*?"<>|]/g, "_"); // sanitise filename
        var filePath = destFolder.fsName + "/" + name;

        try {
            if (CONFIG.format === "PNG") {
                var pngOpts = new ExportOptionsPNG24();
                pngOpts.artBoardClipping = true;
                pngOpts.antiAliasing = true;
                pngOpts.transparency = true;
                pngOpts.horizontalScale = CONFIG.scale * 100;
                pngOpts.verticalScale = CONFIG.scale * 100;
                doc.exportFile(new File(filePath + ".png"), ExportType.PNG24, pngOpts);

            } else if (CONFIG.format === "SVG") {
                var svgOpts = new ExportOptionsSVG();
                svgOpts.artBoardClipping = true;
                svgOpts.embedRasterImages = false;
                doc.exportFile(new File(filePath + ".svg"), ExportType.SVG, svgOpts);

            } else if (CONFIG.format === "PDF") {
                var pdfOpts = new PDFSaveOptions();
                pdfOpts.artboardRange = String(i + 1);
                doc.saveAs(new File(filePath + ".pdf"), pdfOpts);
            }

            exported++;

        } catch (e) {
            $.writeln("Error exporting artboard [" + name + "]: " + e.message);
        }
    }

    alert("Done. Exported " + exported + " of " + total + " artboards to:\n" + destFolder.fsName);

})();
