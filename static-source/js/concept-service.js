var m = angular.module('proso.apps.concept-concept', []);
m.service("conceptService", ["$http", "$q", function($http, $q) {
    var self = this;
    var concepts = null;
    var conceptsPromise = null;
    var userStats = null;
    var userStatsPromise = null;

    var _getConcepts = function () {
        if (conceptsPromise){
            return conceptsPromise;
        }
        conceptsPromise = $http.get("/concepts/concepts?all=True")
            .success(function(response){
                concepts = response.data;
                angular.forEach(concepts, function (concept) {
                    concept.tags_raw = [];
                    angular.forEach(concept.tags, function (tag) {
                        concept.tags_raw.push(tag.type + ':' + tag.value);
                    });
                });
            }).error(function(){
                console.error("Error while loading concepts from backend");
            });
        return conceptsPromise;
    };

    var _getUserStats = function () {
        if (userStatsPromise){
            return userStatsPromise;
        }
        userStatsPromise = $http.get("/concepts/user_stats")
            .success(function(response){
                userStats = response.data;
            }).error(function(){
                console.error("Error while loading user stats from backend");
            });
        return userStatsPromise;
    };

    // get all concepts
    self.getConcepts = function () {
        return $q(function(resolve, reject) {
            if (concepts !== null) {
                resolve(angular.copy(concepts));
            } else {
                _getConcepts()
                    .success(function(){
                        resolve(angular.copy(concepts));
                    }).error(function(){
                        reject("Error while loading concepts from backend");
                });
            }
        });
    };

    self.getUserStats = function (getFromServer) {
        return $q(function(resolve, reject) {
            if (userStats !== null && !getFromServer ) {
                resolve(angular.copy(userStats));
            } else {
                _getUserStats()
                    .success(function(){
                        resolve(angular.copy(userStats));
                    }).error(function(){
                    reject("Error while loading userStats from backend");
                });
            }
        });
    };

    // get all concepts containing all provided tags (form 'type:value')
    self.getConceptsWithTags = function (tags) {
        if (typeof tags !== 'object'){
            tags = tags ? [tags] : [];
        }
        return $q(function(resolve, reject) {
            self.getConcepts().then(
                function (concepts) {
                    var filtered_concepts = [];
                    angular.forEach(concepts, function (concept) {
                        var isIn = true;
                        angular.forEach(tags, function (tag) {
                            if (concept.tags_raw.indexOf(tag) === -1){
                                isIn = false;
                            }
                        });
                        if (isIn){
                            filtered_concepts.push(concept);
                        }
                    });
                    resolve(filtered_concepts);
                }, function (msg) {
                    reject(msg);
            });
        });
    };

    var getConceptByParam = function (param, value) {
        return $q(function(resolve, reject) {
            self.getConcepts().then(
                function (concepts) {
                    var found_concept = {};
                    angular.forEach(concepts, function (concept) {
                        if (concept[param] === value){
                            found_concept = concept;
                        }
                    });
                    resolve(found_concept);
                }, function (msg) {
                    reject(msg);
                });
        });
    };

    self.getConceptByName = function (name) {
        return getConceptByParam('name', name);
    };

    self.getConceptByIdentifier = function (identifier) {
        return getConceptByParam('identifier', identifier);
    };

    self.getConceptByQuery = function (query) {
        return getConceptByParam('identifier', query);
    };
}]);