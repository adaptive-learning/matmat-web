app.controller("Loader", function($scope, $cookies, CommonData, $http, $compile){
    $scope.common = CommonData;
    $scope.question = null;

    $scope.get_question = function(){
        $http.get("/q/get_question/")
            .success(function(data){
                $scope.question = data;
                var questionDirective = angular.element(
                    '<{0} next=\'next_question\' data=\'{1}\' />'.format(data.simulator.replace("_",""), data.data));
                $("#playground").append(questionDirective);
                $compile(questionDirective)($scope);
            });
    };

    $scope.next_question = function(){
        $("#playground").empty();
        $scope.question = null;
        $scope.get_question();
    };

    $scope.next_question();

});
