app.directive("visualizationDivisionBaskets", function(){
    return {
        restrict: "E",
        scope: {
            data: "=data",
            extra: "=extra",
            setting: "=setting",
            interface: "=interface"
        },
        templateUrl: "visualizations/division-baskets.html",
        controller: ["$scope", "practiceGlobal", "$timeout", function($scope, practiceGlobal, $timeout){
            $scope.answer = practiceGlobal.input;
            $scope.answer.value = '';
            $scope.apples = range($scope.data.operands[0]);
            $scope.baskets = range($scope.data.operands[1]);

            practiceGlobal.keyboard = "full";
            $scope.question = $scope.data.operands.join(" "+$scope.data.operation.replace('x', '×').replace('/', '÷')+" ");

            $scope.checkAnswer = function(){
                $scope.answer.value = $scope.answer.value.replace(/\s*-\s*/g,'-').trim();
                var correct = $scope.answer.value === '' + $scope.data.answer;
                var wait = correct ? 1000 : 3000;

                var posleft = {0: 0, 1: -30, 2: 30, 3: -20, 4: 5, 5: 30};
                var postop = {0: 0, 1: 0, 2: 0, 3: 15, 4: 15, 5: 15};

                var ans = $scope.data.answer;
                for (var ai=0; ai < $scope.apples.length; ai++) {
                    var apple = $('#apple' + ai);
                    var pos = ai % ans;
                    var bi = (ai - pos) / ans;
                    var basket = $('#basket' + bi);
                    apple.animate({
                        'top': basket.position().top - apple.position().top - 5 + postop[pos],
                        'left': basket.position().left - apple.position().left + 60 + posleft[pos]
                    }, 900 ); 
                }

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

