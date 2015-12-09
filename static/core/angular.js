var app = angular.module('matmat', ["ngCookies", "ngAnimate", "mm.foundation"]);

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

app.config(["$httpProvider", function($httpProvider){
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.controller("singin", ["$scope", "$http", function($scope, $http){
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
}]);


app.controller("send_child", ["$scope", function($scope){
    $scope.neco = function(){
        console.log($scope.name);
    }
}]);

app.directive('keypressEvents', ["$document", "$rootScope", function ($document, $rootScope) {
    return {
        restrict: 'A',
        link: function () {
            $document.bind('keypress', function (e) {
                $rootScope.$broadcast('keypress', e, String.fromCharCode(e.which));
            });
        }
    };
}]);

app.directive('nextAction', [function() {
    return {
        scope: {
            condition: '=nextAction'
        },
        link: function ($scope, element) {
            $scope.$on('keypress', function (e, a, key) {
                if (a.keyCode === 13 && $scope.condition) {
                    angular.element(element).triggerHandler('click');
                }
            });
        }
    };
}]);