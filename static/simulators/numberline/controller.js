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
                width: 800,
                height: 50,
                offset: 50,
                top: 15,
                hover_size: 30
            };

            // pseudo random range
            var str = "salt"+$scope.data.question;
            var hash = 0, chr;
            for (var i = 0; i < str.length; i++ ){
                chr = str.charCodeAt(i);
                hash  = ((hash << 5) - hash) + chr;
                hash |= 0;
            }
            hash = Math.abs(hash);

            var bound = Math.ceil($scope.data.answer/10)*10;
            console.log(hash);
            console.log($scope.data.answer > 7, 10 * (hash % 2));
            if (18 > $scope.data.answer > 7) bound += 10 * (hash % 2);
            if ($scope.data.answer > 17) bound += 10 * (hash % 3);

            $scope.points = [];
            $scope.range = [0, bound];


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
                    point.display = "none";
                    if (i == $scope.range[0] || i == $scope.range[1]) point.display = "block";
                    $scope.points.push(point);
                }
            };

            $scope.select = function(point){
                if ($scope.nokShow || $scope.okShow) return;
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

            $scope.check_answer = function(){
                var correct = $scope.selected_number == $scope.data.answer;
                $(".numberline-point text").show();
                $("#point"+$scope.data.answer+" text").css("font-weight", "bold");
                $("#point"+$scope.data.answer+" circle.shadow").css("opacity", 1).css("fill", "green");
                $("#point"+$scope.data.answer+" circle.point").css("fill", "green");
                $scope.okShow = correct;
                $scope.nokShow = !correct;
                $scope.interface.finish(correct, 3000);
            };

            $scope.populate_points();

        }
    }
});
