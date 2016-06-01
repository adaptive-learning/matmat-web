app.directive("visualizationMultiplicationField", function(){
    return {
        restrict: "E",
        scope: {
            data: "=data",
            extra: "=extra",
            setting: "=setting",
            interface: "=interface"
        },
        templateUrl: "visualizations/multiplication-field.html",
        controller: ["$scope", "practiceGlobal", "$timeout", function($scope, practiceGlobal, $timeout){
            practiceGlobal.keyboard = "full";
            $scope.answer = practiceGlobal.input;
            $scope.answer.value = '';

            $scope.question = $scope.data.operands.join(" "+$scope.data.operation.replace('x', '×').replace('/', '÷')+" ");

            $scope.field = [];
            var previous_blank = true;
            for (var i=0; i < $scope.extra.field.length; i++) {
                var line = $scope.extra.field[i];
                var sum = 0;
                for (var j=0; j < line.length; j++) {
                    sum += line[j];
                }
                if (sum === 0 && (previous_blank || i + 1 === $scope.extra.field.length)){
                    continue;
                }
                previous_blank = sum === 0;
                $scope.field.push($scope.extra.field[i]);
            }

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
