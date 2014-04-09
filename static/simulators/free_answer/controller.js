app.directive("freeanswer", function(){
    return {
        restrict: "E",
        scope: {
            data: "=data",
            next: "=next"
        },
        templateUrl: static_url + "simulators/free_answer/simulator.html",
        controller: function($scope){
            $scope.check_answer = function(){
                //TODO - delay after answer with feedback
                if ($scope.answer == $scope.data.answer){
                    console.log("yahooo");
                }else{
                    console.log("nope");
                }

                $scope.next();

            };
//          TODO - logging
        }
    }
});