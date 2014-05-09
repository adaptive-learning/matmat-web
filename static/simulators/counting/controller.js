app.directive("counting", function(){
    return {
        restrict: "E",
        scope: {
            data: "=data",
            interface: "=interface"
        },
        templateUrl: static_url + "simulators/counting/simulator.html",
        controller: function($scope){
            $scope.response = '';
            $scope.okHidden = true;
            $scope.nokHidden = true;
            $scope.showForm = true;
            $scope.show10 = false;
            $scope.show20 = false;

            var ans = parseInt($scope.data.answer);
            if (ans <= 7) {
                $scope.showForm = false;
                $scope.show10 = true;
            } else if (ans <= 17) {
                $scope.showForm = false;
                $scope.show10 = true;
                $scope.show20 = true;
            } 

            var width = $scope.data.width;
            var container = document.getElementById('count_display');
            var q = $scope.data.question;
            for (var i=0; i < q.length; i++) {
                if (typeof q[i] == "number") {
                    var ctr = q[i];
                    while (ctr > 0) {
                        var num = Math.min(ctr, width);
                        var div = document.createElement('div');
                        container.appendChild(div);
                        div.style.height = "33px";
                        for (var j=0; j < num; j++) {
                            var span = document.createElement('span');
                            div.appendChild(span);
                            span.style.padding = "1px";
                            var img = document.createElement('img');
                            span.appendChild(img);
                            img.src = "/static/img/cube_orange.png";
                        }
                        ctr = ctr - width;
                    }
                } else if (typeof q[i] == "string") {
                    var h2 = document.createElement('h2');
                    container.appendChild(h2);
                    h2.textContent = q[i];
                }
            }

            $scope.set_text = function(n){
                $scope.response = n;
                $scope.submit();
            };

            $scope.add_text = function(n){
                $scope.response = $scope.response + n;
            };

            $scope.backspace = function(n){
                $scope.response = $scope.response.slice(0, - 1);
            };

            $scope.submit = function() {
                var correct = $scope.response == $scope.data.answer;
                $scope.okHidden = !correct;
                $scope.nokHidden = correct;
                $scope.interface.finish(correct);
            };

//          TODO - logging
        }
    }
});
