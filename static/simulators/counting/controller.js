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

            $scope.rows = [];
            var ctr = $scope.data.question;
            while (ctr > $scope.data.ncols) {
                ctr = ctr - $scope.data.ncols;
                $scope.rows.push($scope.data.ncols);
            }
            $scope.rows.push(ctr);

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
