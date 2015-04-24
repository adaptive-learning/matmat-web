app.directive("field", function(){
    return {
        restrict: "E",
        scope: {
            data: "=data",
            interface: "=interface"
        },
        templateUrl: template_urls["field"],
        controller: function($scope, SimulatorGlobal, $timeout){
            $scope.response = SimulatorGlobal.input;
            $scope.response.value = '';

            if ($scope.data.kb != "full"){
                SimulatorGlobal.keyboard = "choices";
                SimulatorGlobal.choices = $scope.data.kb;
            }else{
                SimulatorGlobal.keyboard = "full";
            }

            $scope.field = [];
            var previous_blank = true;
            for (var i=0; i < $scope.data.field.length; i++) {
                var line = $scope.data.field[i];
                var sum = 0;
                for (var j=0; j < line.length; j++) {
                    sum += line[j];
                }
                if (sum == 0 && (previous_blank || i + 1 == $scope.data.field.length)){
                    continue;
                }
                previous_blank = sum == 0;
                $scope.field.push($scope.data.field[i]);
            }

            $scope.submit = function() {
                $scope.response.value = $scope.response.value.replace(/\s*-\s*/g,'-').trim();
                var correct = $scope.response.value == $scope.data.answer;
                var wait = correct ? 1000 : 3000;
                $scope.solved = true;
                $scope.interface.finish(correct, $scope.response.value, wait);
            };
            SimulatorGlobal.submit = $scope.submit;

            $scope.change = function(){
                $scope.interface.log($scope.response.value);
            };

            SimulatorGlobal.description.top = "Kolik je to čtverečků?";
            $timeout(function(){SimulatorGlobal.simulator_loaded_callback()}, 0);
        }
    }
});
