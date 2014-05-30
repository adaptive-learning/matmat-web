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


app.directive('focus', function(){
    return function(scope, element){
        element[0].focus();
    };
});

app.directive("keyboard", function(){
    return {
        restrict: "E",
        scope: {
        },
        templateUrl: static_url + "core/keyboard.html",
        controller: function($scope, $cookieStore){
            $scope.hidden = !$cookieStore.get("keyboard");

            $scope.switch_visibility = function(){
                $("#keyboard-buttons").addClass("animate-show-drop");
                if ($scope.hidden) {
                    $scope.hidden = false;
                    $cookieStore.put("keyboard", true);
                }else{
                    $scope.hidden = true;
                    $cookieStore.put("keyboard", false);
                }
            };
        }
    }
});

add_text = function(s){
    var input = $("#playground input.active");
    if (s == 'larr'){
        input.val(input.val().substring(0, input.val().length - 1));
    }else{
        input.val(input.val() + s);
    }
    input.focus();
    angular.element(input).triggerHandler('input');
};