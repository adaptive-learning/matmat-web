app.directive("dragdrop", function(){
    return {
        restrict: "E",
        scope: {
            data: "=data",
            interface: "=interface"
        },
        templateUrl: template_urls["dragdrop"],
        controller: function($scope, SimulatorGlobal){
            SimulatorGlobal.keyboard = "empty";

            var ol = $scope.data.tokens;
            var list = document.getElementById('drag_drop_list');
            var dragSrc = null;
            $scope.list = [];

            for (var i=0; i < ol.length; i++) {
                $scope.list.push(ol[i]);
                var item = document.createElement('li');
                item.className = "mydrop";
                list.appendChild(item);
                var div = document.createElement('div');
                div.className = "mydrag";
                div.draggable = true;
                div.innerHTML = ol[i];
                div.addEventListener('dragstart', function(e){
                    dragSrc = this;
                    e.dataTransfer.effectAllowed = 'move';
                    e.dataTransfer.setData('text/html', this.innerHTML);
                    this.classList.add('mydragged');  
                }, false);
                div.addEventListener('dragend', function(e){
                    dragSrc = null;
                    this.classList.remove('mydragged');  
                }, false);
                div.addEventListener('dragenter', function(e){
                    this.classList.add('mydragover');  
                }, false);
                div.addEventListener('dragleave', function(e){
                    this.classList.remove('mydragover');  
                }, false);
                div.addEventListener('dragover', function(e){
                    if (e.preventDefault) {
                        e.preventDefault();
                    }
                    e.dataTransfer.dropEffect = 'move'; 
                    return false;
                }, false);
                div.addEventListener('drop', function(e){
                    if (e.stopPropagation) {
                        e.stopPropagation(); 
                    }
                    if (dragSrc != this) {
                        var x = $scope.list.indexOf(dragSrc.innerHTML);
                        var y = $scope.list.indexOf(this.innerHTML);
                        dragSrc.innerHTML = $scope.list[x] =  this.innerHTML;
                        this.innerHTML = $scope.list[y] = e.dataTransfer.getData('text/html');
                    }
                    this.classList.remove('mydragover');  
                    return false;
                }, false);
                item.appendChild(div);
            }

            $scope.onDropComplete = function (index, obj, evt) {
                var otherObj = $scope.draggableObjects[index];
                var otherIndex = $scope.draggableObjects.indexOf(obj);
                $scope.draggableObjects[index] = obj;
                $scope.draggableObjects[otherIndex] = otherObj;
            }

            $scope.submit = function() {
                var correct = true;
                for (var i = 0; i < $scope.list.length; i++) {
                   if ($scope.list[i] != $scope.data.answer[0][i]) correct = false;
                }
                if (correct){
                    $scope.finished = true;
                    $scope.interface.finish(correct, $scope.list);
                }else{
                    $scope.finished_wrong = true;
                    setTimeout(function() {
                        $scope.finished = true;
                        $scope.$digest();
                    }, 1000);
                    $scope.interface.finish(correct, $scope.list, 2500);
                }
            };

            SimulatorGlobal.description.top = "Zorad"
        }
    }
});

