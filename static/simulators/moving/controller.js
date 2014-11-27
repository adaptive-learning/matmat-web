app.directive("moving", function(){
    return {
        restrict: "E",
        scope: {
            data: "=data",
            interface: "=interface"
        },
        templateUrl: template_urls["moving"],
        controller: function($scope, SimulatorGlobal){
            SimulatorGlobal.keyboard = "empty";

            var ol = $scope.data.tokens;
            $scope.selected = undefined;
            $scope.list = [];

            for (var i=0; i < ol.length; i++) {
                $scope.list.push({'text': ol[i], 'state': 'base'});
            }

            $scope.click = function(event, index) {
                $scope.interface.log("CLICK: " + $scope.list[index]);
                if ($scope.selected == undefined) {
                    $scope.selected = index;
                    $scope.list[$scope.selected].state = 'selected';
                } else {
                    var item = $scope.list[$scope.selected];
                    $scope.list[$scope.selected] = $scope.list[index];
                    $scope.list[index] = item;
                    item.state = 'base';
                    $scope.selected = undefined;
                }

            }

            $scope.submit = function() {
                var correct = true;
                for (var i = 0; i < $scope.list.length; i++) {
                   if ($scope.list[i].text != $scope.data.answer[0][i]) correct = false;
                }
                if (correct){
                    $scope.finished = true;
                    $scope.interface.finish(correct, $scope.list);
                }else{
                    $scope.finished_wrong = true;
                    setTimeout(function() {
                        $scope.finished = true;
                        $scope.$digest();
                    }, 1000);
                    $scope.interface.finish(correct, $scope.list, 2500);
                }
            };

            SimulatorGlobal.description.top = "Seřaď od nejmenšího po největší"
        }
    }
});

