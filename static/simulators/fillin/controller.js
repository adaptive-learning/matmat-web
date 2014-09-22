app.directive("fillin", function(){
    return {
        restrict: "E",
        scope: {
            data: "=data",
            interface: "=interface"
        },
        templateUrl: static_url + "simulators/fillin/simulator.html",
        controller: function($scope){
            $scope.fill = '_';
            $scope.answer = '';
            $("#simulator-input").focus();

            $scope.check_answer = function(){
                $scope.answer = $scope.answer.replace(/\s*-\s*/g,'-').trim();  
                var correct = $scope.answer == $scope.data.answer;
                $scope.interface.finish(correct);
            };

            $scope.change = function(){
                $scope.interface.log($scope.answer);
                $scope.fill = ($scope.answer == '') ? '_' : $scope.answer;
            };
        }
    }
});
