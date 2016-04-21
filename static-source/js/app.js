angular.module("proso.apps", ["proso.apps.common-config","proso.apps.common-logging","proso.apps.flashcards-practice","proso.apps.flashcards-userStats","proso.apps.user-user", "proso.apps.common-toolbar", "proso.apps.tpls"]);
var app = angular.module('matmat', ["ngCookies", "ngRoute", "mm.foundation", "proso.apps"]);

app.config(["$httpProvider", function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.run(["configService", "userService", function(configService, userService) {
    configService.processConfig(config);
    userService.processUser(user);
}]);

app.controller("panel", ["$scope", "userService", function ($scope, userService) {
    $scope.userService = userService;

    $scope.login = function () {
        userService.login($scope.username, $scope.password)
            .success(function (response) {

            }).error(function(response) {
                $scope.msg = response.error;
        });
    };
}]);

var social_auth_callback = function(){
    var element = angular.element($("body"));
    element.injector().get("userService").loadUserFromJS(element.scope());
};