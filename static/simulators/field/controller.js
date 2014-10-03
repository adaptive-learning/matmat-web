app.directive("field", function(){
    return {
        restrict: "E",
        scope: {
            data: "=data",
            interface: "=interface"
        },
        templateUrl: template_urls["field"],
        controller: function($scope, SimulatorGlobal){
            $scope.response = SimulatorGlobal.input;
            $scope.response.value = '';
            $("#simulator-input").focus();

            if ($scope.data.answer <= 10){
                SimulatorGlobal.keyboard = "choices";
                SimulatorGlobal.choices = _.range(1, 10);
            }else{
                SimulatorGlobal.keyboard = "full";
            }

            var container = document.getElementById('count_display');
            var field = $scope.data.field;
            var previous_blank = true;
            for (var i=0; i < field.length; i++) {
                var line = field[i];
                var sum = 0;
                for (var j=0; j < line.length; j++) {
                    sum += line[j];
                }
                if (sum == 0 && (previous_blank || i + 1 == field.length))
                    continue;
                previous_blank = sum == 0;
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

            $scope.submit = function() {
                $scope.response.value = $scope.response.value.replace(/\s*-\s*/g,'-').trim();
                var correct = $scope.response.value == $scope.data.answer;
                var wait = correct ? 1000 : 3000;
                $scope.solved = true;
                $("#playground").find("input").prop('disabled', true);
                $scope.interface.finish(correct, wait);
            };
            SimulatorGlobal.submit = $scope.submit;

            $scope.change = function(){
                $scope.interface.log($scope.response.value);
            };

            SimulatorGlobal.description.top = "Kolik je to čtverečků?"
        }
    }
});
