app.directive("freeanswer", function(){
    return {
        restrict: "E",
        scope: {
            data: "=data",
            interface: "=interface"
        },
        templateUrl: static_url + "simulators/free_answer/simulator.html",
        controller: function($scope){
            $scope.answer = '';
            $("#simulator-input").focus();

            $scope.check_answer = function(){
                $scope.answer = $scope.answer.replace(/\s*-\s*/g,'-').trim();  
                var correct = $scope.answer == $scope.data.answer;
                var wait = 1000;
                if (!correct) {
                    $scope.incorrect_answer = $scope.answer;
                    wait = 3000;
                }
                $scope.correct_answer = $scope.data.answer;
                $scope.solved = true;
                $("#playground").find("input").prop('disabled', true);
                $scope.interface.finish(correct, wait);
            };

            $scope.change = function(){
                $scope.interface.log($scope.answer);
            };
        }
    }
});
