app.directive("wizard", ["$timeout", function($timeout){
    return {
        restrict: "E",
        scope: {
            say: "="
        },
        templateUrl: "graphics/wizard/wizard.html",
        controller: ["$scope", "SimulatorGlobal", function($scope, SimulatorGlobal){
            $scope.global = SimulatorGlobal;

            $scope.$watch("say", function(n, o){
                if (n == null || n == ""){
                    $scope.old_say = o;
                }else{
                    $scope.old_say = null;
                }
            });

        }]
    }
}]);