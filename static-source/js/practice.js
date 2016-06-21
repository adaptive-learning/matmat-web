var FADEIN_DURATION = 1000;
var FADEOUT_DURATION = 1000;
var DEFAULT_WAIT_TIME_BEFORE_Q_FINISH = 1000;

app.factory("practiceGlobal", function(){
        return {
            submit: null,                   // function which ends question in simulator
            skip: null,                     // function which skip question in simulator
            directiveActive: false,        // indicate if simulator is active - the question is not answered
            input: {"value": ""},           // current input
            keyboard: 'gone'               // keyboard mode
            //get_simulator_list: null,       // list of selected simulator pk
            //clear_queue: null,              // function which clear questions from queue
            //description: {top: ""}          // description
        };
    }
);


app.controller("practice", ["$scope", "$location", "practiceService", "$routeParams", "$compile", "practiceGlobal", "$timeout", "$cookieStore", "conceptService", function ($scope, $location, practiceService, $routeParams, $compile, practiceGlobal, $timeout, $cookieStore, conceptService) {
    var concept = $routeParams.concept;

    var loadQuestions = function(){
        practiceService.initSet("common");
        var setLength = practiceService.getConfig().set_length;
        $scope.counter = {
            total: setLength,
            current: 0,
            progress: Array.apply(null, new Array(setLength)).map(Number.prototype.valueOf,0)
        };
        conceptService.getConceptByName(concept).then(function (c) {
            concept = c;
            enrichConcepts([concept]);
            practiceService.setFilter({filter: concept.query});

            nextQuestion();
        });
    };

    var saveAnswer = function(answer){
        practiceService.saveAnswerToCurrentQuestion(
            answer.correctlySolved ? $scope.question.payload.id : null,
            answer.responseTime,
            $scope.question.log,
            {answer: answer.answer, question: answer.question}
        );
    };

    var nextQuestion = function(){
        practiceService.getQuestion()
        .then(
            function(question){
                $scope.counter.current++;
                $scope.question = question;
                $scope.question.log = [];

                var questionDirective = angular.element(
                    '<{0} interface=\'interface\' extra=\'{1}\' data=\'{2}\' setting=\'{3}\' />'.format(
                        'visualization-'+question.payload.context.content.directive,
                        JSON.stringify(question.payload.description),
                        JSON.stringify(question.payload.task.content),
                        JSON.stringify(question.payload.context.content)
                    ));
                $compile(questionDirective)($scope);
                var playground =  $("#playground");
                if (playground.length > 0){
                    playground.append(questionDirective);
                }else{
                    $timeout(function() {
                        playground =  $("#playground");
                        playground.append(questionDirective);
                    }, 100);
                }

            }, function(msg){
                $location.path(concept.view.url);
                $scope.loading = true;
                ga("send", "event", "set", "finished", concept.name);
        });
    };

    var skipQuestion = function(){
        logSomething("skipped");
        if ($cookieStore.get('asked_to_skip', 0) > 0 || window.confirm("Opravdu chcete přeskočit tuto otázku?")) {
            $cookieStore.put('asked_to_skip', $cookieStore.get('asked_to_skip', 0) + 1);
            finishQuestion(false, null, 0);
        }
    };

    practiceGlobal.simulatorReadyCallback = function(){
        if (practiceGlobal.keyboard === "full") {
            $("responseInput").addClass("phantom");
        }
        $scope.loading = false;
        $timeout(function(){
            $scope.question.startTime = new Date().getTime();
            practiceGlobal.directiveActive = true;
        }, FADEIN_DURATION);
    };

    var logSomething = function(data){
        var log = [(new Date().getTime() - $scope.question.startTime), data];
        $scope.question.log.push(log);
    };

    var finishQuestion = function(correctlySolved, providedAnswer, waitTime){
        if (!practiceGlobal.directiveActive){
            return;
        }
        practiceGlobal.directiveActive = false;
        waitTime = typeof waitTime !== 'undefined' ? waitTime : DEFAULT_WAIT_TIME_BEFORE_Q_FINISH;

        logSomething("finished");
        var responseTime =  (new Date().getTime() - $scope.question.startTime);

        $scope.solved = correctlySolved ? "solved_correctly" : "solved_incorrectly";
        var fastSolution = responseTime <= $scope.question.payload.mean_time * 2;
        var extraFastSolution = responseTime <= $scope.question.payload.mean_time;

        $scope.say = correctlySolved ? "Správně" : "Špatně";
        if ($scope.extraFastSolution && correctlySolved){
            $scope.say += " a rychle";
        }
        $scope.counter.progress[$scope.counter.current - 1] = correctlySolved ? fastSolution ? extraFastSolution ? 3 : 2 : 1 : -1;
        $timeout($scope.roller.fitHeight, 0);

        var answer = {
            correctlySolved: correctlySolved,
            answer: providedAnswer,
            question: $scope.question.payload.task.identifier,
            responseTime: responseTime
        };
        saveAnswer(answer);

        if (correctlySolved || providedAnswer === null) {
            $timeout(closeQuestion, waitTime);
        }else{
            practiceGlobal.closeQuestion = closeQuestion;
        }
    };

    var closeQuestion = function () {
        practiceGlobal.closeQuestion = null;
        $scope.question.closed = true;
        $scope.say = "";
        // wait to finish fade-out animation
        $timeout(function() {
            $("#playground").empty();
            $scope.question = null;
            nextQuestion();
            $scope.solved = "";
        }, FADEOUT_DURATION);
    };

    $scope.interface = {};
    $scope.interface.finish = finishQuestion;
    $scope.interface.skip = skipQuestion;
    $scope.interface.log = logSomething;

    $scope.roller = {};

    loadQuestions();
}]);

app.directive("roller", ["$timeout", function($timeout){
    return {
        restrict: "E",
        transclude: true,
        scope: {
            closed: "=",
            question: "=",
            control: "="
        },
        templateUrl: "directives/roller.html",
        controller: ["$scope", "$timeout", function($scope, $timeout){

            $scope.control.fitHeight = $scope.fitHeight = function(){
                var roller = $('roller');
                roller.find("#roller-playground").css("height", roller.find("#roller-playground > div").height());
            };

            $scope.$watch("closed", function(o, n){
                $timeout($scope.fitHeight, 50);
                $timeout($scope.fitHeight, 1000);
            });
        }]
    };
}]);

app.directive("responseInput", ["$timeout", function($timeout){
    return {
        restrict: "E",
        scope: {
            ngModel: "=",       // model for input
            submit: "&",        // submit function
            ngChange: "&"       // function to call after input change
        },
        templateUrl: "directives/response-input.html",

        controller: ["$scope", "practiceGlobal", function($scope, practiceGlobal){
            $scope.global = practiceGlobal;
            $scope.change = function(){
                $timeout($scope.ngChange, 0);
            };

            $scope.localSubmit = function(){
                if ($scope.global.input.value) {
                    $scope.submit();
                }
            };
        }]
    };
}]);

app.directive("responseSpan", function(){
    return {
        restrict: "E",
        scope: {
            answer: "=",        // correct answer
            response: "=",      // current response
            solved: "=",        // indicator of question finish
            def: "@"           // default string to show if answer is empty
        },
        templateUrl: "directives/response-span.html",
        controller: ["$scope", function($scope){
        }]
    };
});

app.directive("keyboard", ["$timeout", function($timeout){
    return {
        restrict: "E",
        scope: {
            closed: "=",
            interface: "="
        },
        templateUrl: "directives/keyboard.html",
        controller: ["$scope", "$cookieStore", "practiceGlobal", function($scope, $cookieStore, practiceGlobal){
            $scope.choices = ["1","2","3","4","5","6","7","8","9","0"];
            $scope.global = practiceGlobal;

            $scope.submit = function(){
                submitButton.removeClass("blink");
                if ($scope.global.input.value) {
                    practiceGlobal.submit();
                }
            };

            $scope.submitAnswer = function(answer){
                if (!$scope.global.directiveActive) {
                    return;
                }
                $scope.addText(answer);
                $scope.submit();
            };

            $scope.chooseAnswer = function(answer){
                $scope.interface.logSomething("choose: " + answer);
                $scope.global.input.value = "" + answer;
            };

            // change response after click to keyboard
            $scope.addText = function(s){
                if (!$scope.global.directiveActive) {
                    return;
                }
                var value = $scope.global.input.value;
                if (s === 'larr'){
                    $scope.global.input.value = value.substring(0, $scope.global.input.value.length - 1);
                }else{
                    $scope.global.input.value = value + s;
                }
                $scope.interface.log("soft-keyboard:" + s);
                $scope.interface.log($scope.global.input.value);
            };

            $scope.skip = function(){
                $scope.interface.skip();
            };

            $scope.switchVisibility = function(){
                $("#keyboard-buttons").addClass("animate-show-drop");
                if ($scope.hidden) {
                    $scope.hidden = false;
                    $cookieStore.put("keyboard", true);
                }else{
                    $scope.hidden = true;
                    $cookieStore.put("keyboard", false);
                }
            };

            var submitButton = $("#keyboard").find(".key.submit");
            $scope.$watch("global.input.value", function(n, o){
                submitButton.removeClass("blink");
                if (n) {
                    $timeout(function () {
                        if ($scope.global.input.value === n && $scope.global.directiveActive) {
                            submitButton.addClass("blink");
                        }
                    }, $scope.global.keyboard === 'choices' ? 500: 3000);
                }
            });
        }]
    };
}]);

app.directive("wizard", [function(){
    return {
        restrict: "E",
        scope: {
            say: "="
        },
        templateUrl: "directives/wizard.html",
        controller: ["$scope", function($scope){
            $scope.$watch("say", function(n, o){
                if (n === null || n === ""){
                    $scope.oldSay = o;
                }else{
                    $scope.oldSay = null;
                }
            });

        }]
    };
}]);

app.directive("practiceProgress", ["$timeout", function($timeout){
    return {
        restrict: "E",
        scope: {
            current: "="
        },
        templateUrl: "directives/practice-progress.html",
        controller: ["$scope", function($scope){
            var counter = $("#counter");
            var removeClass = function(){ div.removeClass("animated"); };
            $scope.$watch("current", function(n, o){
                for (var i=0; i < n.length; i++){
                    if (n[i] !== o[i]){
                        counter.find("div:nth-child("+(i+1)+") div").css("z-index", 1000+i);
                        div = counter.find("div:nth-child("+(i+1)+")");
                        div.addClass("animated");
                        $timeout(removeClass, 500);
                    }
                }
            }, true);
        }]
    };
}]);

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
        templateUrl: "directives/cubes.html",
        controller: ["$scope", "$element", "$timeout", function($scope, $element, $timeout){
            if ($scope.size){
                $($element).find(".objects").css("font-size", $scope.size+"px");
            }
            if ($scope.input || $scope.input === 0){
                $scope.selectable = true;
                $timeout(function(){$scope.cubes = $($element).find("div > div");});

                $scope.hover = function(n){
                    if ($scope.correct) {
                        return;
                    }
                    $scope.cubes.removeClass("hovered");
                    $scope.cubes.slice(0, n).addClass("hovered");
                };

                $scope.select = function(n){
                    if ($scope.correct) {
                        return;
                    }
                    $scope.input = n;
                    $scope.cubes.removeClass("selected");
                    $scope.cubes.removeClass("hovered");
                    $scope.cubes.slice(0, n).addClass("selected");
                };

                $scope.$watch("correct", function(n, o){
                    if (n){
                        $scope.cubes.removeClass("selected");
                        $scope.cubes.removeClass("hovered");
                        if (n === $scope.input){
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
    };
});
