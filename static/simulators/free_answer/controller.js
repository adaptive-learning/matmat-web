app.directive("freeanswer", function(){
    return {
        restrict: "E",
        scope: {
            data: "=data",
            interface: "=interface"
        },
        templateUrl: template_urls["free_answer"],
        controller: function($scope, SimulatorGlobal){
            $scope.answer = SimulatorGlobal.input;
            $scope.answer.value = '';

            if ($scope.data.kb != "full"){
                SimulatorGlobal.keyboard = "choices";
                SimulatorGlobal.choices = $scope.data.kb;
            }else{
                SimulatorGlobal.keyboard = "full";
            }

            $scope.check_answer = function(){
                $scope.answer.value = $scope.answer.value.replace(/\s*-\s*/g,'-').trim();
                var correct = $scope.answer.value == $scope.data.answer;
                var wait = correct ? 1000 : 3000;
                $scope.solved = true;
                $("#playground").find("input").prop('disabled', true);
                $scope.interface.finish(correct, $scope.answer.value, wait);
            };
            SimulatorGlobal.submit = $scope.check_answer;

            $scope.change = function(){
                $scope.interface.log($scope.answer.value);
            };
        }
    }
});

