app.run(["$rootScope", "$location", "userService", function ($rootScope, $location, userService) {
    $rootScope.$on('$routeChangeSuccess', function(){
        ga('send', 'pageview', $location.path());
    });

    $rootScope.$on('$routeChangeStart', function(event, next, current) {
        if (next.originalPath === "/teacher" && !userService.status.logged){
            $location.path("/");
        }
        $("#feedback").css('display', next.templateUrl === 'tournament_match.html' ? "none" : "block");
    });
}]);

app.config(['$routeProvider', '$locationProvider', function ($routeProvider, $locationProvider) {
    $locationProvider.hashPrefix('!');
    $routeProvider.
        when('/', {
            templateUrl: 'home.html',
            controller: "home"
        }).
        when('/about', {
            templateUrl: 'about.html'
        }).
        when('/faq', {
            templateUrl: 'faq.html'
        }).
        when('/practice/:concept', {
            templateUrl: 'practice.html',
            controller: "practice"
        }).
        when('/view/:concept', {
            templateUrl: 'skills.html',
            controller: "skills"
        }).
        when('/view', {
            templateUrl: 'skills.html',
            controller: "skills"
        }).
        when('/teacher', {
            templateUrl: 'teacher.html',
            controller: "teacher"
        }).
        otherwise({
            redirectTo: '/'
        });

    $locationProvider.html5Mode(true);
}]);