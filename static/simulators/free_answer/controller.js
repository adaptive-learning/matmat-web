app.directive("freeanswer", function(){
    return {
        restrict: "E",
        scope: {
            data: "=data",
            interface: "=interface"
        },
        templateUrl: static_url + "simulators/free_answer/simulator.html",
        controller: function($scope){
            $scope.okHidden = true;
            $scope.nokHidden = true;
            $("#simulator-input").focus();

            $scope.check_answer = function(){
                var correct = $scope.answer == $scope.data.answer;
                $scope.okHidden = !correct;
                $scope.nokHidden = correct;

                setTimeout(function() {
                    $scope.interface.finish(correct);
                }, 700);

            };

            $scope.change = function(){
                $scope.interface.log($scope.answer);
            };
        }
    }
});
