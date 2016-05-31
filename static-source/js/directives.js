app.directive('focusMe', ["$timeout", function($timeout) {
    return {
        scope: {
            trigger: '=focusMe'
        },
        priority: -1,
        link: function($scope, element) {
            $scope.$watch('trigger', function(value) {
                if (value === true) {
                    if ($.mobileDevice){
                        element[0].blur();
                    }else{
                        element[0].focus();
                    }
                }
            });
        }
    };
}]);


app.directive('keypressEvents', ["$document", "$rootScope", function ($document, $rootScope) {
    return {
        restrict: 'A',
        link: function () {
            $document.bind('keypress', function (e) {
                $rootScope.$broadcast('keypress', e, String.fromCharCode(e.which));
            });
        }
    };
}]);

app.directive('nextAction', [function() {
    return {
        scope: {
            condition: '=nextAction'
        },
        link: function ($scope, element) {
            $scope.$on('keypress', function (e, a, key) {
                if (a.keyCode === 13 && $scope.condition) {
                    angular.element(element).triggerHandler('click');
                }
            });
        }
    };
}]);
