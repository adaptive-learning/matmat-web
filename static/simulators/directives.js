app.directive('focus', function(){
    return function(scope, element){
        element[0].focus();
    };
});

app.directive("keyboard", function($timeout){
    return {
        restrict: "E",
        scope: {
        },
        templateUrl: template_urls["keyboard"],
        controller: function($scope, $cookieStore, CommonData){
            $scope.hidden = !$cookieStore.get("keyboard");
            $scope.global = CommonData;

            $scope.submit = function(){
                CommonData.submit();
            };

            $scope.submit_answer = function(answer){
                if (!$scope.global.simulator_active)
                    return;
                $scope.add_text(answer);
                $scope.submit();
            };

            $scope.add_text = function(s){
                if (!$scope.global.simulator_active)
                    return;
                var value = $scope.global.input.value;
                if (s == 'larr'){
                    $scope.global.input.value = value.substring(0, $scope.global.input.value.length - 1);
                }else{
                    $scope.global.input.value = value + s;
                }
                $scope.global.log_something("soft-kyeborad:"+s);
                $scope.global.log_something($scope.global.input.value)
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
        templateUrl: template_urls["response-input"],

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
        templateUrl: template_urls["response-span"],
        controller: function($scope){
        }
    }
});
