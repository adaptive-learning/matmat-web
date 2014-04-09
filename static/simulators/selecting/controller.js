app.directive("selecting", function(){
    return {
        restrict: "E",
        scope: {
            data: "=data",
            interface: "=interface"
        },
        templateUrl: static_url + "simulators/selecting/simulator.html",
        controller: function($scope){
            $scope.okHidden = true;
            $scope.nokHidden = true;
            $scope.selected = 0;

            $scope.rows = [];
            var nrows = $scope.data.nrows;
            var ncols = $scope.data.ncols;
            for (var r=0; r<nrows; r++){
                var row = [];
                for (var c=0; c<ncols; c++){
                    row.push(r * ncols + c + 1);
                }
                $scope.rows.push(row);
            };

            $scope.submit = function() {
                var correct = $scope.selected == $scope.data.answer;
                $scope.okHidden = !correct;
                $scope.nokHidden = correct;

                setTimeout(function() {
                    $scope.interface.finish(correct);
                }, 700);

            };

            $scope.getSrc = function(cell) {
                if (cell <= $scope.selected) {
                    return "/static/img/cube_orange.png";
                } else {
                    return "/static/img/cube_grey.png";
                }
            }

            $scope.click = function(cell) {
                $scope.selected = cell;
            };

//          TODO - logging
        }
    }
});
