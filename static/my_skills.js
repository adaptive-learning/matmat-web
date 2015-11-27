app.controller("mySkills", function($scope){
    $scope.$watch("skills", function(skills){
        process_skills(skills, $scope.userSkills, $scope.userDiffs, $scope.active);
    });
});


app.controller("childrenComparison", function($scope, $http){

    var get_data = function(){
        $http.get("/m/children_comparison")
            .success(function(data){
                $scope.skills = data.skills;
                $scope.base_skills = data.base_skills;
                $scope.sub_skills = data.sub_skills;
                $scope.userSkills = data.user_skills;
                $scope.userDiffs = data.user_diffs;
                $scope.children = data.children;
                $scope.answer_counts = data.answer_counts;
                $scope.answer_correct_counts = data.answer_correct_counts;
                $scope.children_ids = data.children_ids;

                angular.forEach($scope.children_ids, function(user) {
                    if (!$scope.pure_skills){
                        $scope.pure_skills = $scope.skills[user];
                    }
                    process_skills($scope.skills[user], $scope.userSkills[user], $scope.userDiffs[user], null, $scope.children[user].user_pk);
                });
            })
    };

    get_data()
});


process_skills = function(skills, userSkills, userDiffs, active, user){
    for (var key in skills) {
        if (skills.hasOwnProperty(key)) {
            skill = skills[key];
            if(user){
                skill.user = user;
            }
            skill.value = userSkills[skill.name];
            skill.diff = userDiffs[skill.name];
            skill.color = get_color(skill.value, skill.diff);
            skill.style = {
                'background-color': 'rgba({0}, {1}, {2}, {3})'.format(skill.color.r, skill.color.g, skill.color.b, skill.color.alpha)
            };
            if (skill.image !== null) {
                skill.style['background-image'] = 'url(' + skill.image + ')';
            }
            skill.style2 = {
                'background': 'linear-gradient(to left, white, rgba({0}, {1}, {2}, {3}))'.format(skill.color.r, skill.color.g, skill.color.b, skill.color.alpha)
            };
            if (active) {
                skill.active = active.indexOf(skill.name) !== -1;
            }
            skill.diamonds = [false, false, false, false, false];
            skill.fromFive = Math.round(1 / (1 + Math.exp(-skill.value)) * 5);
            for (var i = 0; i < skill.fromFive; i++){
                skill.diamonds[skill.diamonds.length - 1 - i] = true;
            }
        }
    }
};