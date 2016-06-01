app.directive("visualizationObjectSelection", function(){
    return {
        restrict: "E",
        scope: {
            data: "=data",
            extra: "=extra",
            setting: "=setting",
            interface: "=interface"
        },
        templateUrl: "visualizations/object-selection.html",
        controller: ["$scope", "practiceGlobal", "$timeout", function($scope, practiceGlobal, $timeout){
            practiceGlobal.keyboard = "empty";
            $scope.selected = 0;

            $scope.checkAnswer = function() {
                var correct = $scope.selected === $scope.data.answer;
                var wait = correct ? 1000 : 3000;
                $scope.interface.finish(correct, $scope.selected, wait);
            };

            $scope.$watch("selected", function(n, o){
                if (n > 0){
                    $scope.interface.log("selected:" + n);
                }
            });

            $timeout(function(){practiceGlobal.simulatorReadyCallback();}, 0);
        }]
    };
});
