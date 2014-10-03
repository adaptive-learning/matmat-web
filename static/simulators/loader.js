var QUESTIONS_IN_SET = 10;
var INITIAL_WAIT_TIME_BEFORE_Q_FINISH = 1000;
var FADEOUT_DURATION = 500;
var QUESTIONS_IN_QUEUE = 1; // 0 - for load Q when needed. 1 - for 1 waiting Q, QUESTIONS_IN_SET - for load all Q on start

app.controller("Loader", function($scope, $cookieStore, SimulatorGlobal, $http, $compile){
    if ($scope.test){
        QUESTIONS_IN_QUEUE = 0;
        QUESTIONS_IN_SET = 1000;
    }
    $scope.common = SimulatorGlobal;
    $scope.skill_id = getURLParameter("skill");
    $scope.question = null;
    $scope.counter = {
        total: QUESTIONS_IN_SET,
        current: 0
    };

    $scope.questions_queue = [];

    $scope.get_questions_from_server = function(){
        var count = Math.min(QUESTIONS_IN_QUEUE - $scope.questions_queue.length,
            QUESTIONS_IN_SET - $scope.counter.current - $scope.questions_queue.length);
        count += $scope.question == null ? 1 : 0;
        if (count > 0){
            var in_queue = [];
            if ($scope.question)
                in_queue.push($scope.question.pk);
            for (var i in $scope.questions_queue){
                in_queue.push($scope.questions_queue[i].pk);
            }
            if (!$scope.test) {
                $http.get("/q/get_question/",
                    {params: {
                        count: count,
                        skill: $scope.skill_id,
                        in_queue: in_queue.join(),
                        simulators: $scope.get_simulator_list()
                    } })
                    .success(function (data) {
                        for (var i in data) {
                            if (data[i].recommendation_log)
                                console.log(data[i]);
                        }
                        $scope.questions_queue = $scope.questions_queue.concat(data);
                        $scope.get_question();
                    });
            }else{
                if ($scope.own_question){
                    q = {};
                    q.data = $scope.own_question;
                    q.simulator = $scope.simulator;
                    $scope.questions_queue.push(q);
                    $scope.get_question();
                }else {
                    $http.get("/q/get_selected_question/" + $scope.question_pk)
                        .success(function (data) {
                            for (var i in data) {
                                if (data[i].recommendation_log)
                                    console.log(data[i]);
                            }
                            $scope.questions_queue = $scope.questions_queue.concat(data);
                            $scope.get_question();
                        });
                }
            }
        }
    };

    $scope.get_question = function(){
        if ($scope.question == null && $scope.questions_queue.length > 0){
            $scope.question = $scope.questions_queue.shift();
            $scope.question.log = [];
            var questionDirective = angular.element(
                '<{0} interface=\'interface\' data=\'{1}\' />'
                    .format($scope.question.simulator.replace("_",""), $scope.question.data));
            $("#playground").append(questionDirective);
            $compile(questionDirective)($scope);
            $scope.question_description = SimulatorGlobal.description;
            $scope.question.start_time = new Date().getTime();
            $scope.loading = false;
            SimulatorGlobal.simulator_active = true;
        }
        $scope.get_questions_from_server();
    };

    $scope.save_answer = function(){
        if ($scope.test){
            console.log($scope.question);
            return;
        }
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
        SimulatorGlobal.simulator_active = false;
        wait_time = typeof wait_time !== 'undefined' ? wait_time : INITIAL_WAIT_TIME_BEFORE_Q_FINISH;

        $scope.log_something("finished");

        $scope.solved= correctly_solved ? "solved_correctly" : "solved_incorrectly";

        setTimeout(function() {
            $scope.question.time =  Math.round((new Date().getTime() - $scope.question.start_time) / 1000);
            $scope.question.correctly_solved =  correctly_solved;
            $scope.save_answer();


            $scope.question.hide = true;
            setTimeout(function() {
                $("#playground").empty();
                $scope.question = null;
                if ($scope.counter.current == $scope.counter.total){
                    window.location.replace("/m/my_skills/"+$scope.skill_id);
                }else{
                    $scope.next_question();
                }
            $scope.solved = ""
            }, FADEOUT_DURATION);
        }, wait_time);
    };

    SimulatorGlobal.skip = $scope.skip = function(){
        $scope.log_something("skipped");
        $scope.finish_question(false, 0);
    };

    $scope.log_something = function(data){
        var log = [(new Date().getTime() - $scope.question.start_time), data];
        $scope.question.log.push(log);
        if ($scope.test) {
            console.log(log);
        }
    };
    SimulatorGlobal.log_something = $scope.log_something;

    $scope.get_simulator_list = function(){
        var pks = [];
        for (var i=0; i < simulators.length; i++){
            var simulator = simulators[i];
            var state = $cookieStore.get("simulator" + simulator.pk);
            if (state || state==null){
                pks.push(simulator.pk);
            }
        }
        return pks.join();
    };

    $scope.clear_queue = function(){
        $scope.questions_queue = [];
    };
    SimulatorGlobal.clear_queue = $scope.clear_queue;

    $scope.interface = {};
    $scope.interface.finish = $scope.finish_question;
    $scope.interface.log = $scope.log_something;

    $scope.next_question();
});
