app.directive("rollerwizard", ["$timeout", function($timeout){
    return {
        restrict: "E",
        transclude: true,
        scope: {
            closed: "=",
            question: "=",
            control: "="
        },
        templateUrl: "simulators/roller-wizard.html",
        controller: ["$scope", "SimulatorGlobal", "$timeout", function($scope, SimulatorGlobal, $timeout){
            $scope.global = SimulatorGlobal;

            $scope.control.fit_height = $scope.fit_height = function(){
                var roller = $('#roller-wizard');
                roller.find("#roller-playground").css("height", roller.find("#roller-playground > div").height() + 10)
            };

            $scope.$watch("closed", function(o, n){
                $scope.fit_height();
                $timeout($scope.fit_height, 100);
                $timeout($scope.fit_height, 1000);
            });
        }]
    }
}]);