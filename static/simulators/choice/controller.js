app.directive("choice", function(){
    return {
        restrict: "E",
        scope: {
            data: "=data",
            interface: "=interface"
        },
        templateUrl: template_urls["choice"],
        controller: function($scope, SimulatorGlobal){
            SimulatorGlobal.keyboard = "empty";

            var ol = $scope.data.tokens;
            $scope.list = [];
            for (var i=0; i < ol.length; i++) {
                $scope.list.push({'text': ol[i], 'state': 'base'});
            }

            $scope.click = function(event, index) {
                var ans = $scope.list[index];
                var correct = ans.text == $scope.data.answer;
                if (correct){
                    ans.state = 'correct';
                    $scope.finished = true;
                    $scope.interface.finish(correct, ans.text);
                } else {
                    ans.state = 'incorrect';
                    $scope.finished_wrong = true;
                    setTimeout(function() {
                        $scope.finished = true;
                        $scope.$digest();
                    }, 1000);
                    $scope.interface.finish(correct, ans.text, 2500);
                }
            };

            SimulatorGlobal.description.top = $scope.data.text;
        }
    }
});

