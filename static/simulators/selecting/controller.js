app.directive("selecting", function(){
    return {
        restrict: "E",
        scope: {
            data: "=data",
            interface: "=interface"
        },
        templateUrl: template_urls["selecting"],
        controller: function($scope, SimulatorGlobal, $timeout){
            SimulatorGlobal.keyboard = "empty";
            $scope.selected = 0;
//            $scope.simple = $scope.data.answer < 10;

            $scope.submit = function() {
                var correct = $scope.selected == $scope.data.answer;
                $scope.correct = $scope.data.answer;
                if (correct){
                    $scope.interface.finish(correct, $scope.selected);
                }else{
                    $scope.interface.finish(correct, $scope.selected, 2500);
                }
            };

            $scope.$watch("selected", function(n, o){
                if (n > 0){
                    $scope.interface.log("selected:" + n);
                }
            });

            SimulatorGlobal.description.top = "Vyber zadaný počet čtverečků.";
            $timeout(function(){SimulatorGlobal.simulator_loaded_callback()}, 0);
        }
    }
});
