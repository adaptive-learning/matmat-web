app.directive("rollerwizard", function($timeout){
    return {
        restrict: "E",
        transclude: true,
        scope: {
            closed: "="
        },
        templateUrl: template_urls["roller-wizard"],
        controller: function($scope, SimulatorGlobal, $timeout){
            $scope.global = SimulatorGlobal;

            $scope.prepare_height = function(){
                console.log($("#roller-wizard").find("#roller-playground > div").height());
                $timeout( function() {
                    $('#roller-wizard').find("#roller-playground").css("height", $("#roller-wizard").find("#roller-playground > div").height())
                }, 100);
            };

            $scope.$watch("closed", function(o, n){
                $scope.prepare_height();
            });
        }
    }
});