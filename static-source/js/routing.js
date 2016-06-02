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
        otherwise({
            redirectTo: '/'
        });

    $locationProvider.html5Mode(true);
}]);