app.controller("Loader", function($scope, $cookies, CommonData, $http, $compile){
    $scope.common = CommonData;
    $scope.question = null;

    $scope.get_question = function(){
        $http.get("/q/get_question/")
            .success(function(data){
                $scope.question = data;
                $scope.question.log = [];
                var questionDirective = angular.element(
                    '<{0} interface=\'interface\' data=\'{1}\' />'.format(data.simulator.replace("_",""), data.data));
                $("#playground").append(questionDirective);
                $compile(questionDirective)($scope);
                $scope.question.start_time = new Date().getTime();
            });
    };

    $scope.save_answer = function(){
        $http.post("/q/save_answer/", $scope.question)
            .success(function(data){
                $scope.chat = data;
            });
    };


    $scope.next_question = function(){
        $scope.get_question()
    };


    $scope.finish_question = function(result){
        $scope.question.time =  Math.round((new Date().getTime() - $scope.question.start_time) /  1000);
        $scope.save_answer();

        $("#playground").empty();
        $scope.question = null;

        $scope.next_question();
    };

    $scope.log_something = function(data){
        $scope.question.log.push([(new Date().getTime() - $scope.question.start_time), data]);
//        console.log($scope.question.log);
    };


    $scope.interface = {};
    $scope.interface.finish = $scope.finish_question;
    $scope.interface.log = $scope.log_something;

    $scope.next_question();


});