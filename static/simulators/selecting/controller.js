app.directive("selecting", function(){
    return {
        restrict: "E",
        scope: {
            data: "=data",
            interface: "=interface"
        },
        templateUrl: template_urls["selecting"],
        controller: function($scope, SimulatorGlobal, $timeout){
            SimulatorGlobal.keyboard = "empty";
            $scope.selected = 0;
            $scope.mover = 0;
//            $scope.simple = $scope.data.answer < 10;
            $scope.simple = false;

            $scope.rows = [];
            var nrows = $scope.data.nrows;
            var ncols = $scope.data.ncols;
            for (var r=0; r<nrows; r++){
                var row = [];
                for (var c=0; c<ncols; c++){
                    row.push(r * ncols + c + 1);
                }
                $scope.rows.push(row);
            }

            $scope.submit = function() {
                var correct = $scope.selected == $scope.data.answer;
                if (correct){
                    $scope.finished = true;
                    $scope.interface.finish(correct, $scope.selected);
                }else{
                    $scope.finished_wrong = true;
                    setTimeout(function() {
                        $scope.finished = true;
                        $scope.$digest();
                    }, 1000);
                    $scope.interface.finish(correct, $scope.selected, 2500);
                }
            };

            $scope.getSrc = function(cell) {
                var ret = "/static/img/cube_grey.png";

                if ($scope.finished){
                    if (cell <= $scope.data.answer){
                        ret = "/static/img/cube_green.png";
                    }
                    return ret;
                }

                if ($scope.finished_wrong){
                    if (cell <= $scope.selected){
                        ret = "/static/img/cube_red.png";
                    }
                    return ret;
                }

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
                $scope.interface.log(cell);
                $scope.selected = cell;
                if ($scope.simple){
                    $scope.submit();
                }
            };

            $scope.over = function(cell) {
                $scope.mover = cell;
            };

            $scope.out = function() {
                $scope.mover = 0;
            };

            SimulatorGlobal.description.top = "Vyber zadaný počet čtverečků.";
            $timeout(function(){SimulatorGlobal.simulator_loaded_callback()}, 0);
        }
    }
});
