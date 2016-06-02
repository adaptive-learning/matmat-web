function openPopup(url, next) {
    /* Open popup to Google or Facebook auth */

    var w = 700;
    var h = 500;
    var left = 100;
    var top = 100;

    var settings = 'height=' + h + ',width=' + w + ',left=' + left + ',top=' + top + ',resizable=yes,scrollbars=yes,toolbar=no,menubar=no,location=yes,directories=no,status=yes';
    url += "?next=" + next;

    window.open(url, "popup", settings);
}

if (!String.prototype.format) {
    String.prototype.format = function() {
        /* format functionality for strings */
        var args = arguments;
        return this.replace(/{(\d+)}/g, function(match, number) {
            return typeof args[number] !== 'undefined' ? args[number] : match;
        });
    };
}

$.mobileDevice = (/android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini/i.test(navigator.userAgent.toLowerCase()));


var range = function (n) {
    return Array.apply(null, Array(n)).map(function (_, i) {return i;});
};

var getColor = function(value, used){
    if (typeof value === 'undefined') {
        return {r: 127, g:127, b:0, a: 0};
    }

    color = HSVtoRGB(1 / 12 + value * 2 / 9, 1, 0.8);
    color.alpha = used ? 1 : 0.2;
    return color;
};


function HSVtoRGB(h, s, v) {
    var r, g, b, i, f, p, q, t;
    if (h && s === undefined && v === undefined) {
        s = h.s; v = h.v; h = h.h;
    }
    i = Math.floor(h * 6);
    f = h * 6 - i;
    p = v * (1 - s);
    q = v * (1 - f * s);
    t = v * (1 - (1 - f) * s);
    switch (i % 6) {
        case 0: r = v; g = t; b = p; break;
        case 1: r = q; g = v; b = p; break;
        case 2: r = p; g = v; b = t; break;
        case 3: r = p; g = q; b = v; break;
        case 4: r = t; g = p; b = v; break;
        case 5: r = v; g = p; b = q; break;
    }
    return {
        r: Math.floor(r * 255),
        g: Math.floor(g * 255),
        b: Math.floor(b * 255)
    };
}
