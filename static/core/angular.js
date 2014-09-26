var app = angular.module('matmat', ["ngCookies", "ngAnimate"]);

app.factory("CommonData", function(){
        return {
            test: "hello world",

//            for sumulators
            submit: null,       // function which ends question in simulator
            skip: null,        // skip question in simulator
            input: {"value": ""},        // curent input
            keyboard: 'gone'     // keyboard mode
        }
    }
);

app.config(function($httpProvider){
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }
);