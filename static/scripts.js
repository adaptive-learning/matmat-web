generate_cubes = function (count, canvas_id) {
    var canvas = $("#"+canvas_id);
    for (var i=0; i < count; i++){
        var cube = $("<div></div>");
        cube.css("background-color", random_color());
        cube.css("left", Math.random()*100 - 15 + "%");
        cube.css("top", Math.random()*100 - 15 + "%");
        cube.css("transform", "rotate({0}deg)".format(Math.random() * 90));
        canvas.append(cube);
    }
};

random_color = function () {
    return 'rgb({0},{1},{2})'.format(Math.floor(Math.random() * 256), Math.floor(Math.random() * 256), Math.floor(Math.random() * 256))
};


get_color = function(value, used){
    if (typeof value === 'undefined') {
        return {r: 127, g:127, b:0, a: 0};
    }

    value = (1 / (1 + Math.exp(-value)));
    color = HSVtoRGB(1. / 12 + value * 2 / 9., 1, 0.8);
    color.alpha = used ? 1 : 0.2;
    return color
};


function HSVtoRGB(h, s, v) {
    var r, g, b, i, f, p, q, t;
    if (h && s === undefined && v === undefined) {
        s = h.s, v = h.v, h = h.h;
    }
    i = Math.floor(h * 6);
    f = h * 6 - i;
    p = v * (1 - s);
    q = v * (1 - f * s);
    t = v * (1 - (1 - f) * s);
    switch (i % 6) {
        case 0: r = v, g = t, b = p; break;
        case 1: r = q, g = v, b = p; break;
        case 2: r = p, g = v, b = t; break;
        case 3: r = p, g = q, b = v; break;
        case 4: r = t, g = p, b = v; break;
        case 5: r = v, g = p, b = q; break;
    }
    return {
        r: Math.floor(r * 255),
        g: Math.floor(g * 255),
        b: Math.floor(b * 255)
    };
}