/**
 * Toggle Layer Visibility Across All Comps
 * -----------------------------------------
 * Finds layers matching a name pattern across every composition
 * and toggles their visibility. Useful for batch-hiding watermark
 * or placeholder layers before a final render.
 *
 * How to run: File > Scripts > Run Script File > select this file
 */

(function () {

    var LAYER_NAME_PATTERN = "WATERMARK";   // Exact name or partial match string
    var EXACT_MATCH = false;                // true = exact name, false = contains match
    var SET_VISIBLE = false;                // true = force visible, false = force hidden

    // -------------------------------------------------------

    var proj = app.project;
    if (!proj) { alert("No project open."); return; }

    var modified = 0;
    var compsChecked = 0;

    for (var i = 1; i <= proj.numItems; i++) {
        var item = proj.item(i);
        if (!(item instanceof CompItem)) continue;
        compsChecked++;

        for (var j = 1; j <= item.numLayers; j++) {
            var layer = item.layer(j);
            var match = EXACT_MATCH
                ? (layer.name === LAYER_NAME_PATTERN)
                : (layer.name.toLowerCase().indexOf(LAYER_NAME_PATTERN.toLowerCase()) !== -1);

            if (match) {
                layer.enabled = SET_VISIBLE;
                modified++;
            }
        }
    }

    var action = SET_VISIBLE ? "shown" : "hidden";
    alert("Done.\nChecked " + compsChecked + " compositions.\n" + modified + " layer(s) " + action + " matching: '" + LAYER_NAME_PATTERN + "'");

})();
