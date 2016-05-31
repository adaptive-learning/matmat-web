app.directive("visualizationSimple", function(){
    return {
        restrict: "E",
        scope: {
            data: "=data",
            extra: "=extra",
            setting: "=setting",
            interface: "=interface"
        },
        templateUrl: "visualizations/simple.html",
        controller: ["$scope", "practiceGlobal", "$timeout", function($scope, practiceGlobal, $timeout){
            practiceGlobal.keyboard = "full";
            $scope.answer = practiceGlobal.input;
            $scope.answer.value = '';

            $scope.question = $scope.data.operands.join(" "+$scope.data.operation.replace('x', '×').replace('/', '÷')+" ");

            $scope.checkAnswer = function(){
                $scope.answer.value = $scope.answer.value.replace(/\s*-\s*/g,'-').trim();
                var correct = $scope.answer.value === '' + $scope.data.answer;
                var wait = correct ? 1000 : 3000;
                $scope.solved = true;
                $scope.interface.finish(correct, $scope.answer.value, wait);
            };
            practiceGlobal.submit = $scope.checkAnswer;

            $scope.change = function(){
                $scope.interface.log($scope.answer.value);
            };

            $timeout(function(){practiceGlobal.simulatorReadyCallback();}, 0);
        }]
    };
});

