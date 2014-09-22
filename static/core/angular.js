var app = angular.module('matmat', ["ngCookies", "ngAnimate"]);

app.factory("CommonData", function(){
        return {
            test: "hello world"
        }
    }
);

app.config(function($httpProvider){
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }
);