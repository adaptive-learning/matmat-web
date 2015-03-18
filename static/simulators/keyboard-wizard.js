app.directive("keyboardwizard", function($timeout){
    return {
        restrict: "E",
        scope: {
            closed: "="
        },
        templateUrl: template_urls["keyboard-wizard"],
        controller: function($scope, $cookieStore, SimulatorGlobal){
            $scope.choices = ["1","2","3","4","5","6","7","8","9","0"];
            $scope.global = SimulatorGlobal;

            $scope.submit = function(){
                if ($scope.global.input.value)
                    SimulatorGlobal.submit();
            };

            $scope.submit_answer = function(answer){
                if (!$scope.global.simulator_active)
                    return;
                $scope.add_text(answer);
                $scope.submit();
            };

            // change response after click to keyboard
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
                SimulatorGlobal.skip();
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

            var submit_button = $("#keyboard-wizard").find(".key.submit");
            $scope.$watch("global.input.value", function(n, o){
                submit_button.removeClass("blink");
                if (n) {
                    $timeout(function () {
                        if ($scope.global.input.value == n)
                            submit_button.addClass("blink");
                    }, 3000);
                }
            });
        }
    }
});