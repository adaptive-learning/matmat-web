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
            $scope.showForm = true;
            $scope.show10 = false;
            $scope.show20 = false;
            $scope.prefix = $scope.data.prefix || '';
            if ($scope.prefix != '') $scope.prefix += ' = ';

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
            var prev = "string";
            for (var i=0; i < q.length; i++) {
                if (typeof q[i] == "number") {
                    if (prev == "number") {
                        // add some vertical space
                        var div = document.createElement('div');
                        container.appendChild(div);
                        div.style.height = "20px";
                    }
                    var ctr = q[i];
                    while (ctr > 0) {
                        var num = Math.min(ctr, width);
                        var div = document.createElement('div');
                        container.appendChild(div);
                        div.style.height = "33px";
                        div.style.textAlign = "left";
                        div.style.width = width*33 + 5 +"px";
                        div.style.margin = "auto";
                        for (var j=0; j < num; j++) {
                            var span = document.createElement('span');
                            if ((j + 1) % 5 == 0){
                                span.style.marginRight = "5px";
                            }
                            div.appendChild(span);
                            span.style.padding = "1px";
                            var img = document.createElement('img');
                            span.appendChild(img);
                            img.src = "/static/img/cube_orange.png";
                            alpha = Math.floor(Math.random() * 100 / 0.5) + 50;
                            //img.style.filter       = "alpha(opacity=" + str(alpha) + ");";
                            alpha = alpha / 100;
                            img.style.MozOpacity   = alpha;
                            img.style.opacity      = alpha;
                            img.style.KhtmlOpacity = alpha;
                        }
                        ctr = ctr - width;
                    }
                } else if (typeof q[i] == "string") {
                    var h2 = document.createElement('h2');
                    container.appendChild(h2);
                    h2.textContent = q[i];
                }
                prev = typeof q[i];
            }

            $scope.set_text = function(n){
                $scope.response = n;
                $scope.submit();
            };

            $scope.submit = function() {
                var correct = $scope.response == $scope.data.answer;
                $scope.interface.finish(correct);
            };

//          TODO - logging
        }
    }
});
