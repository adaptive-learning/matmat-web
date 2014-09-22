app.directive("selecting", function(){
    return {
        restrict: "E",
        scope: {
            data: "=data",
            interface: "=interface"
        },
        templateUrl: static_url + "simulators/selecting/simulator.html",
        controller: function($scope){
            $scope.selected = 0;
            $scope.mover = 0;

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
                $scope.interface.finish(correct);
            };

            $scope.getSrc = function(cell) {
                var ret = "/static/img/cube_grey.png";
                if (cell <= $scope.selected) {
                    ret = "/static/img/cube_orange.png";
                } 
                if (cell <= $scope.mover) {
                    ret = "/static/img/cube_violet.png";
                } 
                if (cell <= $scope.selected && cell <= $scope.mover) {
                    ret = "/static/img/cube_pink.png";
                } 
                return ret;
            };

            $scope.have_horizontal_gap = function(cell) {
                return cell  % 5 == 0;
            };

            $scope.have_vertical_gap = function(row) {
                return row[row.length-1] % 50 == 0;
            };

            $scope.click = function(cell) {
                $scope.selected = cell;
            };

            $scope.over = function(cell) {
                $scope.mover = cell;
            };

            $scope.out = function() {
                $scope.mover = 0;
            };

//          TODO - logging
        }
    }
});
