angular.module("proso.apps", ["proso.apps.common-config","proso.apps.common-logging","proso.apps.models-practice", "proso.apps.user-user", "proso.apps.concept-concept", "proso.apps.common-toolbar", "proso.apps.tpls"]);
var app = angular.module('matmat', ["ngCookies", "ngRoute", "mm.foundation", "proso.apps"]);

app.config(["$httpProvider", function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.run(["$rootScope", "$location", "userService", function ($rootScope, $location, userService) {
    $rootScope.$on('$routeChangeSuccess', function(){
        ga('send', 'pageview', $location.path());
    });
}]);

app.run(["configService", "userService", function(configService, userService) {
    configService.processConfig(config);
    userService.processUser(user);
}]);

app.controller("panel", ["$scope", "userService", function ($scope, userService) {
    $scope.userService = userService;
    $scope.credentials = {};

    $scope.login = function () {
        userService.login($scope.credentials.username, $scope.credentials.password)
            .success(function (response) {
                $('#login-modal').foundation('reveal', 'close');
            }).error(function(response) {
                $scope.msg = response.error;
        });
    };
    $(document).foundation('reveal');
}]);

app.controller("home", ["$scope", "conceptService", function ($scope, conceptService) {
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
            $scope.concepts = concepts0.concat(concepts);
            console.log($scope.concepts);
        });
    });
    $(document).foundation('dropdown');
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
