/**
 * Rename Layers Sequentially
 * --------------------------
 * Renames all top-level layers in the active document:
 * Layer_01, Layer_02, Layer_03 ...
 *
 * Configurable: prefix and zero-padding width.
 * How to run: File > Scripts > Other Script > select this file
 */

(function () {

    var PREFIX = "Layer_";       // Prefix for each layer name
    var PAD = 2;                 // Zero-pad width (2 → "01", 3 → "001")

    // -------------------------------------------------------

    var doc = app.activeDocument;
    if (!doc) { alert("No document open."); return; }

    var layers = doc.layers;

    function pad(n, width) {
        var s = String(n);
        while (s.length < width) s = "0" + s;
        return s;
    }

    for (var i = 0; i < layers.length; i++) {
        layers[i].name = PREFIX + pad(i + 1, PAD);
    }

    alert("Renamed " + layers.length + " layers.");

})();
