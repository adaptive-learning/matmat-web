var app = angular.module('matmat', ["ngCookies"]);

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


app.directive('focus', function(){
    return function(scope, element){
        element[0].focus();
    };
});
