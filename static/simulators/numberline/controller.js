app.directive("numberline", function(){
    /* name of directive have to be its name without _  (replaced by "") */
    return {
        restrict: "E",
        scope: {
            data: "=data",              // json data from database
            interface: "=interface"     // interface of loader
        },
        templateUrl: static_url + "simulators/numberline/simulator.html",  // html
        controller: function($scope){

            $scope.selected_number = null;

            $scope.settings = {
                width: 600,
                height: 50,
                offset: 50,
                top: 30,
                hover_size: 30
            };

            $scope.points = [];
            $scope.range = [0, 10];


            $scope.populate_points = function(){
                var line_length = $scope.settings.width - 2 * $scope.settings.offset;
                var delta = line_length / ($scope.range[1] - $scope.range[0]);
                for (var i=$scope.range[0]; i<=$scope.range[1]; i++){
                    var point = {};
                    point.number = $scope.range[0] + i;
                    point.x = $scope.settings.offset + i * delta;
                    point.y = $scope.settings.top;
                    point.r = 3;
                    if (point.number % 5 == 0) point.r = 4;
                    if (point.number % 10 == 0) point.r = 5;
                    $scope.points.push(point);
                }
            };

            $scope.select = function(point){
                var number = parseInt(point.id.replace("point", ""));
                point = $(point);
                $("g").attr("class", $("g").attr("class").replace(" selected", ""));
                if (number != $scope.selected_number) {
                    $scope.selected_number = number;
                    point.attr("class", point.attr('class')+" selected");
                }else{
                    $scope.selected_number = null;
                }

                $scope.$apply();


            };

            $scope.populate_points();

        }
    }
});
