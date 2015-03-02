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