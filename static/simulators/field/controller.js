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
            $("#simulator-input").focus();

            var container = document.getElementById('count_display');
            var field = $scope.data.field;
            for (var i=0; i < field.length; i++) {
                var line = field[i];
                var sum = 0;
                for (var j=0; j < line.length; j++) {
                    sum += line[j];
                }
                if (sum == 0)
                    continue;
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
                        img.src = "/static/img/cube_white.png";
                    }
                }
            }

            $scope.set_text = function(n){
                $scope.response = n;
                $scope.submit();
            };

            $scope.submit = function() {
                $scope.response = $scope.response.replace(/\s*-\s*/g,'-').trim();
                var correct = $scope.response == $scope.data.answer;
                var wait = correct ? 1000 : 3000;
                $scope.solved = true;
                $("#playground").find("input").prop('disabled', true);
                $scope.interface.finish(correct, wait);
            };

            $scope.change = function(){
                $scope.interface.log($scope.response);
            };

//          TODO - show correct answer after incorrect response
        }
    }
});
