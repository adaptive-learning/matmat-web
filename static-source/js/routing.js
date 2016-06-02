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
        otherwise({
            redirectTo: '/'
        });

    $locationProvider.html5Mode(true);
}]);