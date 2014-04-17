app.directive("counting", function(){
    return {
        restrict: "E",
        scope: {
            data: "=data",
            interface: "=interface"
        },
        templateUrl: static_url + "simulators/counting/simulator.html",
        controller: function($scope){
            $scope.okHidden = true;
            $scope.nokHidden = true;

            var width = $scope.data.width;

            $scope.rows = [];
            var q = $scope.data.question;
            for (var i=0; i < q.length; i++) {
                if (typeof q[i] == "number") {
                    var ctr = q[i];
                    while (ctr > width) {
                        ctr = ctr - width;
                        $scope.rows.push(width);
                    }
                    $scope.rows.push(ctr);
                } else {
                    $scope.rows.push(q[i]);
                }
            }

            $scope.type = function(v) {
                return typeof v;
            };

            $scope.getNumber = function(num) {
                return new Array(num);   
            };

            $scope.submit = function() {
                var correct = $scope.response == $scope.data.answer;
                $scope.okHidden = !correct;
                $scope.nokHidden = correct;
                $scope.interface.finish(correct);
            };

//          TODO - logging
        }
    }
});
