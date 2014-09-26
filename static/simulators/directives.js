app.directive('focus', function(){
    return function(scope, element){
        element[0].focus();
    };
});

app.directive("keyboard", function($timeout){
    return {
        restrict: "E",
        submit: "=",
        scope: {
        },
        templateUrl: static_url + "simulators/keyboard.html",
        controller: function($scope, $cookieStore, CommonData){
            $scope.hidden = !$cookieStore.get("keyboard");
            $scope.global = CommonData;

            $scope.submit = function(){
                CommonData.submit();
            };

            $scope.submit_answer = function(answer){
                $scope.add_text(answer);
                $scope.submit();
            };

            $scope.add_text = function(s){
                var value = $scope.global.input.value;
                if (s == 'larr'){
                    $scope.global.input.value = value.substring(0, input.val().length - 1);
                }else{
                    $scope.global.input.value = value + s;
                }
            };

            $scope.skip = function(){
                CommonData.skip();
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
        controller: function($scope, CommonData){
            $scope.global = CommonData;
            $scope.change = function(){
                $timeout($scope.ngChange, 0);
            }
        }
    }
});


app.directive("responsespan", function(){
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
