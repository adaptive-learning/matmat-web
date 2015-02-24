app.directive("pairing", function(){
    return {
        restrict: "E",
        scope: {
            data: "=data",
            interface: "=interface"
        },
        templateUrl: template_urls["pairing"],
        controller: function($scope, SimulatorGlobal, $timeout){
            $scope.gameover = false;
            SimulatorGlobal.keyboard = "empty";


            var q = $scope.data.question;
            $scope.todo = q.length * q[0].length / 2;
            $scope.rows = [];
            for (var i=0; i < q.length; i++) {
                var row = [];
                for (var j=0; j < q[i].length; j++) {
                    row.push({'text': q[i][j][0], 'pair': q[i][j][1],
                            'disabled': false, 'state': 'active'});
                }
                $scope.rows.push(row);
            }

            $scope.selected = undefined;
            $scope.click = function(cell) {
                if ($scope.selected == undefined) {
                    // select
                    $scope.interface.log("SELECT: " + cell.text);
                    $scope.selected = cell;
                    $scope.selected.state = 'selected';
                } else if ($scope.selected == cell) {
                    // unselect
                    $scope.interface.log("UNSELECT: " + cell.text);
                    $scope.selected.state = 'active';
                    $scope.selected = undefined;
                } else if ($scope.selected.pair == cell.pair) {
                    // correct
                    $scope.interface.log("CORRECT: " + cell.text);
                    $scope.selected.disabled = true;
                    cell.disabled = true;
                    $scope.selected.state = 'off';
                    cell.state = 'off';
                    $scope.selected = undefined;
                    $scope.todo--;
                    if ($scope.todo == 0) {
                        $scope.submit(true);
                    }
                } else {
                    // wrong
                    $scope.interface.log("WRONG: " + cell.text);
                    $scope.interface.save_partial_answer(false, null);
                    $scope.selected.state = ($scope.selected.state != 'wactive') ? 'wactive' : 'wwactive';
                    cell.state = (cell.state != 'wactive') ? 'wactive' : 'wwactive';
                    $scope.selected = undefined;
                }
            };

            $scope.submit = function(correct) {
                $scope.gameover = true;
                var wait = correct ? 1000 : 3000;
                $scope.solved = correct;
                $scope.interface.finish(correct, null, wait);
            };
            SimulatorGlobal.submit = $scope.submit;

            SimulatorGlobal.description.top = "Vyznač kartičky se stejnou hodnotou.";
            $timeout(function(){SimulatorGlobal.simulator_loaded_callback()}, 0);
        }
    }
});
