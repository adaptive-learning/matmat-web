app.directive('focus', function(){
    return function(scope, element){
        element[0].focus();
    };
});

app.directive("keyboard", function(){
    return {
        restrict: "E",
        submit: "=",
        scope: {
        },
        templateUrl: static_url + "simulators/keyboard.html",
        controller: function($scope, $cookieStore, CommonData){
            $scope.hidden = !$cookieStore.get("keyboard");
            $scope.submit = CommonData.submit;

            $scope.submit = function(){
                CommonData.submit();
            };

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

app.directive("responseinput", function($timeout){
    return {
        restrict: "E",
        scope: {
            ngModel: "=",
            submit: "&",
            ngChange: "&"
        },
        templateUrl: static_url + "simulators/response-input.html",
        controller: function($scope){
            $scope.change = function(){
                $timeout($scope.ngChange, 0);
            }
        }
    }
});


app.directive("responsespan", function($timeout){
    return {
        restrict: "E",
        scope: {
            answer: "=",
            response: "=",
            solved: "=",
            default: "@"
        },
        templateUrl: static_url + "simulators/response-span.html",
        controller: function($scope){
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