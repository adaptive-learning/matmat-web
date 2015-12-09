app.directive('focus', function(){
    return function(scope, element){
        if ($.mobile_device){
            element[0].blur();
        }else{
            element[0].focus();
        }
    };
});

app.directive('focusMe', ["$timeout", function($timeout) {
    return {
        scope: {
            trigger: '=focusMe'
        },
        priority: -1,
        link: function($scope, element) {
            $scope.$watch('trigger', function(value) {
                if (value === true) {
                    if ($.mobile_device){
                        element[0].blur();
                    }else{
                        element[0].focus();
                    }
                }
            });
        }
    };
}]);

app.directive("keyboard", ["$timeout", function($timeout){
    return {
        restrict: "E",
        scope: {
        },
        templateUrl: "simulators/keyboard.html",
        controller: ["$scope", "$cookieStore", "SimulatorGlobal", function($scope, $cookieStore, SimulatorGlobal){
            //  $scope.hidden = !$cookieStore.get("keyboard");
            $scope.hidden = false;
            $scope.global = SimulatorGlobal;

            $scope.submit = function(){
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
                $scope.global.log_something("soft-keyboard:"+s);
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
        }]
    }
}]);

// input field with submit button
app.directive("responseinput", ["$timeout", function($timeout){
    return {
        restrict: "E",
        scope: {
            ngModel: "=",       // model for input
            submit: "&",        // submit function
            ngChange: "&"       // function to call after input change
        },
        templateUrl: "simulators/response-input.html",

        controller: ["$scope", "SimulatorGlobal", function($scope, SimulatorGlobal){
            $scope.global = SimulatorGlobal;
            $scope.change = function(){
                $timeout($scope.ngChange, 0);
            };

            $scope.local_submit = function(){
                if ($scope.global.input.value)
                    $scope.submit()
            };
        }]
    }
}]);

// show current response, after finish question show correct solution
app.directive("responsespan", function(){
    return {
        restrict: "E",
        scope: {
            answer: "=",        // right answer
            response: "=",      // current response
            solved: "=",        // indicator of question finish
            def: "@"        // default string to show if answer is empty
        },
        templateUrl: "simulators/response-span.html",
        controller: ["$scope", function($scope){
        }]
    }
});


app.directive("simulatorselector", function(){
    return {
        restrict: "E",
        scope: {
        },
        templateUrl: "simulators/simulator_selector.html",
        controller: ["$scope", "$cookieStore", "SimulatorGlobal", function($scope, $cookieStore, SimulatorGlobal){
            $scope.simulators = simulators;

            for (var i=0; i<$scope.simulators.length; i++){
                var simulator = $scope.simulators[i];
                var state = $cookieStore.get("simulator" + simulator.pk);
                if (state == null)
                    state = true;
                simulator.selected = state;
            }

            $scope.change = function(simulator){
                $cookieStore.put("simulator" + simulator.pk, simulator.selected);
                SimulatorGlobal.clear_queue();
            };
        }]
    }
});

app.directive("cubes", function(){
    return {
        restrict: "E",
        scope: {
            count: "=",
            height: "=",
            width: "=",
            size: "=",
            field: "=",
            input: "=",
            correct: "="
        },
        templateUrl: "simulators/cubes.html",
        controller: ["$scope", "$element", "$timeout", function($scope, $element, $timeout){
            if ($scope.size){
                $($element).find(".objects").css("font-size", $scope.size+"px")
            }

            if ($scope.input != null){
                $scope.selectable = true;
                $timeout(function(){$scope.cubes = $($element).find("div > div")});

                $scope.hover = function(n){
                    if ($scope.correct) return;
                    $scope.cubes.removeClass("hovered");
                    $scope.cubes.slice(0, n).addClass("hovered");
                };

                $scope.select = function(n){
                    if ($scope.correct) return;
                    $scope.input  = n;
                    $scope.cubes.removeClass("selected");
                    $scope.cubes.removeClass("hovered");
                    $scope.cubes.slice(0, n).addClass("selected");
                };

                $scope.$watch("correct", function(n, o){
                    if (n){
                        $scope.cubes.removeClass("selected");
                        $scope.cubes.removeClass("hovered");
                        if (n == $scope.input){
                            $scope.cubes.slice(0, n).addClass("correct");
                        }else{
                            $scope.cubes.slice(0, $scope.input).addClass("incorrect");
                            $timeout(function () {
                                $scope.cubes.removeClass("incorrect");
                                $scope.cubes.slice(0, n).addClass("correct");
                            }, 1000);
                        }
                    }

                });
            }

            $scope.repeater = function(n) {
                return new Array(n);
            };
        }]
    }
});