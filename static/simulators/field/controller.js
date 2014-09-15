app.directive("field", function(){
    return {
        restrict: "E",
        scope: {
            data: "=data",
            interface: "=interface"
        },
        templateUrl: static_url + "simulators/field/simulator.html",
        controller: function($scope){
            $scope.response = '';

            var container = document.getElementById('count_display');
            var field = $scope.data.field;
            for (var i=0; i < field.length; i++) {
                var line = field[i];
                var div = document.createElement('div');
                container.appendChild(div);
                div.style.height = "33px";
                for (var j=0; j < line.length; j++) {
                    var span = document.createElement('span');
                    div.appendChild(span);
                    span.style.padding = "1px";
                    var img = document.createElement('img');
                    span.appendChild(img);
                    if (line[j] == 1) {
                        img.src = "/static/img/cube_orange.png";
                    } else {
                        img.src = "/static/img/cube_grey.png";
                    }
                }
            }

            $scope.set_text = function(n){
                $scope.response = n;
                $scope.submit();
            };

            $scope.submit = function() {
                var correct = $scope.response == $scope.data.answer;
                $scope.interface.finish(correct);
            };

//          TODO - logging
        }
    }
});
