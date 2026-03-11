/**
 * Batch Render Queue
 * ------------------
 * Adds all open compositions to the After Effects render queue
 * with a consistent output template, then starts the render.
 *
 * How to run: File > Scripts > Run Script File > select this file
 */

(function () {

    var OUTPUT_TEMPLATE = "Best Settings";    // AE render settings template name
    var OUTPUT_MODULE = "Lossless";           // AE output module template name
    var OUTPUT_FOLDER = "";                   // Leave "" to prompt, or set absolute path

    // -------------------------------------------------------

    var proj = app.project;
    if (!proj) { alert("No project open."); return; }

    // Determine output folder
    var destFolder;
    if (OUTPUT_FOLDER) {
        destFolder = new Folder(OUTPUT_FOLDER);
    } else {
        destFolder = Folder.selectDialog("Select render output folder");
        if (!destFolder) return;
    }

    // Collect all compositions
    var comps = [];
    for (var i = 1; i <= proj.numItems; i++) {
        if (proj.item(i) instanceof CompItem) {
            comps.push(proj.item(i));
        }
    }

    if (comps.length === 0) {
        alert("No compositions found in this project.");
        return;
    }

    var queue = app.project.renderQueue;
    var added = 0;

    for (var j = 0; j < comps.length; j++) {
        var comp = comps[j];
        try {
            var rqi = queue.items.add(comp);

            // Apply render settings template
            try { rqi.applyTemplate(OUTPUT_TEMPLATE); } catch (e) { /* template may not exist */ }

            // Set output path
            var safeName = comp.name.replace(/[\/\\:*?"<>|]/g, "_");
            var outPath = destFolder.fsName + "/" + safeName + ".mov";
            var om = rqi.outputModules[1];

            // Apply output module template
            try { om.applyTemplate(OUTPUT_MODULE); } catch (e) { /* template may not exist */ }

            om.file = new File(outPath);
            added++;

        } catch (e) {
            $.writeln("Could not queue comp [" + comp.name + "]: " + e.message);
        }
    }

    alert("Added " + added + " compositions to render queue.\nStarting render...");

    // Fire the render
    queue.render();

})();
