/**
 * Set Uniform Composition Settings
 * ----------------------------------
 * Applies the same resolution, framerate, and duration to every
 * composition in the project. Useful when importing assets from
 * multiple sources with inconsistent comp settings.
 *
 * How to run: File > Scripts > Run Script File > select this file
 */

(function () {

    var CONFIG = {
        width: 1920,
        height: 1080,
        pixelAspect: 1,           // 1 = square pixels
        frameRate: 25,            // FPS
        durationSeconds: 10,      // Duration in seconds
        bgColor: [0, 0, 0]        // RGB 0-255
    };

    // Set to true to only update comps matching a name pattern
    var FILTER_BY_NAME = false;
    var NAME_FILTER = "";    // e.g. "MASTER_" to only update comps named MASTER_*

    // -------------------------------------------------------

    var proj = app.project;
    if (!proj) { alert("No project open."); return; }

    var updated = 0;

    for (var i = 1; i <= proj.numItems; i++) {
        var item = proj.item(i);
        if (!(item instanceof CompItem)) continue;

        if (FILTER_BY_NAME && item.name.indexOf(NAME_FILTER) === -1) continue;

        try {
            item.width = CONFIG.width;
            item.height = CONFIG.height;
            item.pixelAspect = CONFIG.pixelAspect;
            item.frameRate = CONFIG.frameRate;
            item.duration = CONFIG.durationSeconds;
            item.bgColor = [
                CONFIG.bgColor[0] / 255,
                CONFIG.bgColor[1] / 255,
                CONFIG.bgColor[2] / 255
            ];
            updated++;
        } catch (e) {
            $.writeln("Could not update comp [" + item.name + "]: " + e.message);
        }
    }

    alert("Updated " + updated + " composition(s) to " + CONFIG.width + "x" + CONFIG.height + " @ " + CONFIG.frameRate + "fps");

})();
