app.directive("visualizationObjectCounting", function(){
    return {
        restrict: "E",
        scope: {
            data: "=data",
            extra: "=extra",
            setting: "=setting",
            interface: "=interface"
        },
        templateUrl: "visualizations/object-counting.html",
        controller: ["$scope", "practiceGlobal", "$timeout", function($scope, practiceGlobal, $timeout){
            practiceGlobal.keyboard = "full";
            $scope.answer = practiceGlobal.input;
            $scope.answer.value = '';

            $scope.size = $scope.data.operands.length >= 2 && ($scope.data.operands[0] > 7 || $scope.data.operands[1] > 7) ? 10 : 15;
            $scope.block = $scope.data.operation === "x";
            $scope.question = $scope.data.operands.join(" "+$scope.data.operation.replace('x', '×').replace('/', '÷')+" ");


            $scope.setText = function(n){
                $scope.response.value = n;
                $scope.submit();
            };

            $scope.checkAnswer = function() {
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
