app.controller("Feedback", function($scope, $http, $location){
    $scope.feedback = {};

    $scope.submit = function(){
        $scope.feedback.url = $location.absUrl();
        $http.post('/feedback', $scope.feedback)
            .success(function(data){
                $scope.msg_tag = "success";
                $scope.msg = data.msg;
                $scope.sending = false;
                $scope.feedback.text = ""
            }).error(function(){
                $scope.msg = "V aplikaci bohužel nastala chyba.";
                $scope.msg_tag = "alert";
                $scope.sending = false;
            });
        $scope.sending = true;
    };

    $(document).on('closed.fndtn.reveal', '[data-reveal]', function () {
        var modal = $(this);
        $scope.msg = "";
    });
});