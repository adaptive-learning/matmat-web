app.directive("wizard", function($timeout){
    return {
        restrict: "E",
        scope: {
            say: "="
        },
        templateUrl: template_urls["wizard"],
        controller: function($scope, SimulatorGlobal){
            $scope.global = SimulatorGlobal;

            $scope.$watch("say", function(n, o){
                if (n == null || n == ""){
                    $scope.old_say = o;
                }else{
                    $scope.old_say = null;
                }
            });

        }
    }
});