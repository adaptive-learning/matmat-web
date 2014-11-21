var app = angular.module('matmat', ["ngCookies", "ngAnimate"]);

app.factory("SimulatorGlobal", function(){
        return {
            test: "hello world",
//            for simulators
            submit: null,                   // function which ends question in simulator
            skip: null,                     // function which skip question in simulator
            simulator_active: false,        // indicate if simulator is active - the question is not answered
            input: {"value": ""},           // current input
            keyboard: 'gone',               // keyboard mode
            log_something: null,            // simulator logger function
            get_simulator_list: null,       // list of selected simulator pk
            clear_queue: null,              // function which clear questions from queue
            description: {top: ""}          // description
        }
    }
);

app.config(function($httpProvider){
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }
);

app.controller("singin", function($scope, $http){
    $scope.submit = function(){
        $http.post("/ajaxlogin/",
            {
                password: $scope.password,
                username: $scope.username
            })
            .success(function (data) {
                if (data.success){
                    window.location.replace("/");
                    $scope.msg =  "Přihlášeno";
                    $scope.msg_color =  "green";
                }else{
                    $scope.msg =  data.error_msg;
                    $scope.msg_color =  "red";
                }
            }).error(function (){
                $scope.msg =  "Chyba při komunikaci se serverem.";
                $scope.msg_color =  "red";
        });
    }
});