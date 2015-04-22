app.directive("rollerwizard", function($timeout){
    return {
        restrict: "E",
        transclude: true,
        scope: {
            closed: "=",
            question: "="
        },
        templateUrl: template_urls["roller-wizard"],
        controller: function($scope, SimulatorGlobal, $timeout){
            $scope.global = SimulatorGlobal;

            $scope.fit_height = function(){
                var roller = $('#roller-wizard');
                roller.find("#roller-playground").css("height", roller.find("#roller-playground > div").height() + 10)
            };

            $scope.$watch("closed", function(o, n){
                $scope.fit_height();
                $timeout($scope.fit_height, 100);
                $timeout($scope.fit_height, 1000);
            });
        }
    }
});