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
            $scope.okHidden = true;
            $scope.nokHidden = true;
            $("#simulator-input").focus();

            $scope.check_answer = function(){
                var correct = $scope.answer == $scope.data.answer;
                $scope.okHidden = !correct;
                $scope.nokHidden = correct;
                $scope.interface.finish(correct);
            };

            $scope.change = function(){
                $scope.interface.log($scope.answer);
            };
        }
    }
});
