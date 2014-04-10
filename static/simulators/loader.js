app.controller("Loader", function($scope, $cookies, CommonData, $http, $compile){
    $scope.common = CommonData;
    $scope.question = null;
    $scope.counter = {
        total: 10,
        current: 0
    };

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
                $scope.loading = false;
            });
    };

    $scope.save_answer = function(){
        $http.post("/q/save_answer/", $scope.question)
            .success(function(data){
                $scope.chat = data;
            });
    };


    $scope.next_question = function(){
        $scope.loading = true;
        $scope.counter.current++;
        $scope.get_question()
    };


    $scope.finish_question = function(correctly_solved, wait_time){
        wait_time = typeof wait_time !== 'undefined' ? wait_time : 1000;

        $scope.log_something("finished");
        setTimeout(function() {
            $scope.question.time =  Math.round((new Date().getTime() - $scope.question.start_time) / 1000);
            $scope.question.correctly_solved =  correctly_solved;
            $scope.save_answer();

            setTimeout(function() {
                $("#playground").empty();
                $scope.question = null;
                if ($scope.counter.current == $scope.counter.total){
                    window.location.replace("/");
                }else{
                    $scope.next_question();
                }
            }, 500);
        }, wait_time);
    };

    $scope.skip = function(){
        $scope.log_something("skipped");
        $scope.finish_question(false, 0);
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
