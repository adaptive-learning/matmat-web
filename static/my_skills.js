app.controller("mySkills", function($scope){
    console.log("controller", new Date());
    $scope.$watch("skills", function(skills){
        console.log("start", new Date());
        for (var key in skills) {
            if (skills.hasOwnProperty(key)) {
                skill = skills[key];
                skill.value = $scope.userSkills[skill.name];
                skill.diff = $scope.userDiffs[skill.name];
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
                skill.active = $scope.active.indexOf(skill.name) !== -1;
                skill.diamonds = [false, false, false, false, false];
                for (var i = 0; i < Math.round(1 / (1 + Math.exp(-skill.value)) * 5); i++){
                    skill.diamonds[skill.diamonds.length - 1 - i] = true;
                }
            }
        }
        console.log("end", new Date(), (new Date).getMilliseconds());
    });
});
