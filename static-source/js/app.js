angular.module("proso.apps", ["proso.apps.common-config","proso.apps.common-logging","proso.apps.models-practice", "proso.apps.user-user", "proso.apps.concept-concept", "proso.apps.common-toolbar", "proso.apps.tpls"]);
var app = angular.module('matmat', ["ngCookies", "ngRoute", "mm.foundation", "proso.apps"]);

app.config(["$httpProvider", function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.run([function () {
    toastr.options = {
        "positionClass": "toast-top-center"
    };
}]);

app.run(["configService", "userService", function(configService, userService) {
    configService.processConfig(config);
    userService.processUser(user);
}]);

app.service("skillsService", ["$q", "conceptService", "$http", function($q, conceptService, $http) {
    var self = this;
    var skills = null;
    var skillsPromise = $q.defer();

    conceptService.getConceptsWithTags('level:0').then(function (concepts0) {
        enrichConcepts(concepts0);
        concept = concepts0[0];
        conceptService.getConceptsWithTags(['level:1']).then(function (subConcepts) {
            enrichConcepts(subConcepts);
            concept.subConcepts = subConcepts;
        });
        conceptService.getConceptsWithTags('level:1').then(function (concepts) {
            enrichConcepts(concepts);
            angular.forEach(concepts, function (concept) {
                conceptService.getConceptsWithTags(['concept:'+concept.rawName, 'level:2']).then(function (subConcepts) {
                    enrichConcepts(subConcepts);
                    concept.subConcepts = subConcepts;
                });
            });
            skills = concepts0.concat(concepts);
            skillsPromise.resolve(skills);
        });
    });

    self.getSkills = function () {
        return skillsPromise.promise;
    };

    self.getTable = function(concept){
        return $http.get('small_concepts/' + concept);
    };

}]);

app.controller("panel", ["$scope", "userService", "$timeout", function ($scope, userService, $timeout) {
    $scope.userService = userService;
    $scope.credentials = {};
    $scope.newUser = {};

    $scope.login = function () {
        userService.login($scope.credentials.username, $scope.credentials.password)
            .success(function (response) {
                $('#login-modal').foundation('reveal', 'close');
            }).error(function(response) {
                $scope.msg = response.error;
        });
    };

    $scope.signup = function () {
        userService.signup($scope.newUser)
            .success(function (response) {
                $('#signup-modal').foundation('reveal', 'close');
            }).error(function(response) {
                $scope.msg = response.error;
        });
    };

    $timeout(function(){
        $(document).foundation();
    });
}]);

app.controller("home", ["$scope", "skillsService", function ($scope, skillsService) {
    skillsService.getSkills().then(function (concepts) {
        $scope.concepts = concepts;
    });
}]);

app.controller("skills", ["$scope", "skillsService", "conceptService", "$routeParams", function ($scope, skillsService, conceptService, $routeParams) {
    var currentConcept = $routeParams.concept;
    conceptService.getUserStats(true).then(function (userStats) {
        enrichUserStats(userStats);
        $scope.userStats = userStats;
        skillsService.getSkills().then(function (concepts) {
            $scope.concepts = concepts.slice(1, concepts.length);
            if (currentConcept) {
                conceptService.getConceptByName(currentConcept).then(function (concept) {
                    enrichConcepts([concept]);
                    $scope.currentConcept = concept;
                    angular.forEach($scope.concepts, function (concept) {
                        if (concept.identifier === $scope.currentConcept.identifier){
                            concept.active = true;
                        }
                        angular.forEach(concept.subConcepts, function (subConcept) {
                            if (subConcept.identifier === $scope.currentConcept.identifier){
                                concept.active = true;
                                subConcept.active = true;
                                getTable(subConcept.rawName);
                            }
                        });
                    });
                });
            }
        });
    });

    $scope.tables = {};

    $scope.activeSubConcept = function (concept) {
        if (!concept.active) {          // activity change after this function
            getTable(concept.rawName);
        }
    };

    var getTable = function (identifier) {
        if ($scope.tables[identifier]){
            return;
        }
        $scope.tables[identifier] = {'loading': true};
        skillsService.getTable(identifier)
            .success(function(response){
                angular.forEach(response.data, function(concept){
                    concept.color = getColor(concept.prediction, concept.answer_count);
                    concept.style = {
                        'background-color': 'rgba({0}, {1}, {2}, {3})'.format(concept.color.r, concept.color.g, concept.color.b, concept.color.alpha)
                    };
                });
                $scope.tables[identifier] = response;
            });
    };
}]);

app.controller("feedback", ["$scope", "$http", "$location", "userService", function ($scope, $http, $location, userService) {
    $scope.feedback = {};
    if (userService.user){
        $scope.feedback.email = userService.user.email;
    }

    $scope.send = function() {
        $scope.feedback.page = $location.absUrl();

        $http.post('/feedback/feedback/', $scope.feedback).success(function(data){
            $scope.sending = false;
            $scope.feedback.text = '';
            $('#feedback-modal').foundation('reveal', 'close');
        }).error(function(){
            $scope.sending = false;

        });
        $scope.sending = true;
    };
}]);

app.controller("teacher", ["$scope", "$location", "userService", function ($scope, $location, userService) {
    $scope.new = {};
    $scope.data = {};
    $scope.newClassName = null;
    $scope.classes = userService.user.profile.owner_of;
    $scope.profile = userService.user.profile;
    $scope.status = userService.status;

    if ($scope.classes.length === 1){
        $scope.classes[0].isOpen = true;
    }

    $scope.createClass = function () {
        userService.createClass($scope.data.newClassName)
            .success(function(response){
                toastr.success('Třída vytvořena');
                $scope.data.newClassName = null;
            }).error(function(response) {
                toastr.error(response.error);
            });
    };

    $scope.joinClass = function () {
        userService.joinClass($scope.data.joinClassCode)
            .success(function(response){
                toastr.success('Přídání se do třídy proběhlo úspěšně');
                $scope.data.joinClassCode = null;
            }).error(function(response) {
            toastr.error(response.error);
        });
    };

    $scope.addChild = function(){
        userService.createStudent($scope.new)
            .success(function(response){
                toastr.success('Přidání dítěte proběhlo úspěšně');
                $scope.new = {};
            }).error(function(response) {
                toastr.error(response.error);
        });
    };

    $scope.logAs = function(id){
        userService.loginStudent(id)
            .success(function(response){
                $location.path('/');
            }).error(function(response) {
                toastr.error(response.error);
        });
    };

}]);

app.directive("childrenComparison", [function(){
    return {
        restrict: "E",
        transclude: true,
        scope: {
            cls: "="
        },
        templateUrl: "children_comparison.html",
        controller: ["$scope", "conceptService", "skillsService", function($scope, conceptService, skillsService){
            $scope.stats = null;
            var loading = false;

            var ids = [];
            angular.forEach($scope.cls.members, function (member) {
                ids.push(member.user.id);
            });

            skillsService.getSkills().then(function (concepts) {
                $scope.concepts = concepts.slice(1, concepts.length);
            });

            var loadStats = function () {
                loading = true;
                conceptService.getUserStatsBulk(ids).success(function (response) {
                    $scope.stats = {};
                    angular.forEach(response.data.users, function (userStats) {
                        enrichUserStats(userStats.concepts);
                        $scope.stats[userStats.user_id] = userStats.concepts;
                    });
                });
            };

            $scope.$watch('cls.isOpen', function(isOpen){
                if (isOpen && !loading){
                    loadStats();
                }
            });
        }]
    };
}]);

var social_auth_callback = function(){
    var element = angular.element($("body"));
    element.injector().get("userService").loadUserFromJS(element.scope());
};

var enrichConcepts = function(concepts){
    angular.forEach(concepts, function (concept) {
        concept.rawName = /"skill\/(.*)"/.exec(concept.query)[1];
        concept.query = JSON.parse(concept.query);
        angular.forEach(concept.actions, function (action) {
            concept[action.identifier] = action;
            action.url = /\/(.*)/.exec(action.url)[1];
        });
    });
};

var enrichUserStats = function (userStats) {
    angular.forEach(userStats, function (userStat, id) {
        userStat.color = getColor(userStat.prediction, userStat.practiced_items_count);
        userStat.style = {
            'background-color': 'rgba({0}, {1}, {2}, {3})'.format(userStat.color.r, userStat.color.g, userStat.color.b, userStat.color.alpha)
        };

        userStat.style2 = {
            'background': 'linear-gradient(to left, white, rgba({0}, {1}, {2}, {3}))'.format(userStat.color.r, userStat.color.g, userStat.color.b, userStat.color.alpha)
        };
        userStat.diamonds = [false, false, false, false, false];
        userStat.fromFive = Math.round(userStat.prediction * 5);
        for (var i = 0; i < userStat.fromFive; i++){
            userStat.diamonds[userStat.diamonds.length - 1 - i] = true;
        }
    });
};
