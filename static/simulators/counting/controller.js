app.directive("counting", function(){
    return {
        restrict: "E",
        scope: {
            data: "=data",
            interface: "=interface"
        },
        templateUrl: template_urls["counting"],
        controller: function($scope, SimulatorGlobal, $timeout){
            $scope.response = SimulatorGlobal.input;
            $scope.response.value = '';

            if ($scope.data.kb != "full"){
                SimulatorGlobal.keyboard = "choices";
                SimulatorGlobal.choices = $scope.data.kb;
            }else{
                SimulatorGlobal.keyboard = "full";
            }

            $scope.size = $scope.data.question.length >=3 && ($scope.data.question[0] > 7 || $scope.data.question[2] > 7) ? 10 : 15;

            $scope.block = $scope.data.question.length == 3 && $scope.data.question[1]=="×";

            $scope.type = function(part){
                return typeof part;
            };

            $scope.set_text = function(n){
                $scope.response.value = n;
                $scope.submit();
            };

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

            if (!$scope.data.with_text) SimulatorGlobal.description.top = "Kolik je to čtverečků?";
            $timeout(function(){SimulatorGlobal.simulator_loaded_callback()}, 0);
        }
    }
});
