app.directive("visualizationNumberLine", function(){
    /* name of directive have to be its name without _  (replaced by "") */
    return {
        restrict: "E",
        scope: {
            data: "=data",
            extra: "=extra",
            setting: "=setting",
            interface: "=interface"
        },
        templateUrl: "visualizations/number-line.html",  // html
        controller: ["$scope", "practiceGlobal", "$timeout", function($scope, practiceGlobal, $timeout){
            $scope.url = 'url(/practice#shadow)';

            practiceGlobal.keyboard = "empty";
            $scope.selectedNumber = null;
            $scope.simple = $scope.data.answer <= 10;
            $scope.question = $scope.data.operation ?
                $scope.data.operands.join(" "+$scope.data.operation.replace('x', '×').replace('/', '÷')+" ") :
                $scope.data.operands[0];


            $scope.settings = {
                width: $("#playground").width() ? $("#playground").width() : $("#content").width() - 200,
                height: 50,
                offset: 50,
                top: 30
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
            if (18 > $scope.data.answer > 7) { bound += 10 * (hash % 2); }
            if ($scope.data.answer > 17) { bound += 10 * (hash % 3);
            }

            $scope.points = [];
            $scope.rects = [];
            if ($scope.data.answer <= 10) {
                $scope.range = [0, 10];
            } else {
                $scope.range = [0, bound];
            }


            var populatePoints = function(){
                var line_length = $scope.settings.width - 2 * $scope.settings.offset;
                var delta = line_length / ($scope.range[1] - $scope.range[0]);
                $scope.settings.hover_size = delta;
                var left = 0;
                for (var i=$scope.range[0]; i<=$scope.range[1]; i++){
                    var point = {};
                    point.number = i;
                    point.x = $scope.settings.offset + left;
                    point.y = $scope.settings.top;
                    point.r = 3;
                    if (point.number % 5 === 0){ point.r = 4; }
                    if (point.number % 10 === 0){ point.r = 5; }
                    point.display = "none";
                    if ($scope.data.answer <= 10) {
                        if (i === 1 || i === 5 || i === 10) { point.display = "block"; }
                        if (i === $scope.data.answer) { point.display = "none"; }
                        if (i === 0 ){ point.r = 2; }
                    }else{
                        if (i === $scope.range[0] || i === $scope.range[1]){
                            point.display = "block";
                        }
                    }
                    $scope.points.push(point);

                    if ($scope.simple && i< $scope.range[1]){
                        var rect = {};
                        rect.size = Math.min(delta/2, $scope.settings.top -2);
                        rect.y = $scope.settings.top - rect.size - 2;
                        rect.x = $scope.settings.offset + left + (delta - rect.size) / 2;
                        rect.number = i;

                        $scope.rects.push(rect);
                    }

                    left += delta;
                }
            };

            $scope.select = function(point){
                if ($scope.nokShow || $scope.okShow) { return; }
                var number = parseInt(point.id.replace("point", ""));
                point = $(point);
                $("g").attr("class", $("g").attr("class").replace(" selected", ""));
                if (number !== $scope.selectedNumber) {
                    $scope.selectedNumber = number;
                    point.attr("class", point.attr('class')+" selected");
                    $scope.interface.log(number+" selected");
                }else{
                    $scope.selectedNumber = null;
                    $scope.interface.log("unselected");
                }

                $scope.$apply();
                if ($scope.simple){
                    $scope.hoveredNumber = $scope.data.answer;
                    $timeout($scope.checkAnswer, 0);
                }

            };

            $scope.hover = function(point){
                if ($scope.simple && !$scope.nokShow && !$scope.okShow) {
                    $scope.hoveredNumber = parseInt(point.id.replace("point", ""));
                    $scope.$apply();
                }
            };

            $scope.leave = function(){
                if ($scope.simple && !$scope.nokShow && !$scope.okShow) {
                    $scope.hoveredNumber = null;
                    $scope.$apply();
                }
            };

            $scope.checkAnswer = function() {
                var correct = $scope.selectedNumber === $scope.data.answer;
                $(".numberline-point text").show();
                $("#point" + $scope.data.answer + " text").css("font-weight", "bold");
                $("#point" + $scope.data.answer + " circle.shadow").css("opacity", 1).css("fill", "green");
                $("#point" + $scope.data.answer + " circle.point").css("fill", "green");
                if (!correct) {
                    $("#point" + $scope.selectedNumber + " circle.shadow").css("opacity", 1).css("fill", "red");
                    $("#point" + $scope.selectedNumber + " circle.point").css("fill", "red");
                }
                $scope.okShow = correct;
                $scope.nokShow = !correct;
                $scope.interface.finish(correct, $scope.selectedNumber, 2000);
            };

            populatePoints();

            $timeout(function(){practiceGlobal.simulatorReadyCallback();}, 0);
        }]
    };
});
