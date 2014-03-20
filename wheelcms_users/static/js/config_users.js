var ModalInstanceCtrl = function($scope, $modalInstance, user) {
    $scope.user = user;

    $scope.ok = function () {
      $modalInstance.close($scope.selected);
    };

    $scope.cancel = function () {
      $modalInstance.dismiss('cancel');
    };
};

app.controller('UserGroupCtrl', function($scope, $modal) {
    $scope.deleted = [];
    $scope.users = [];
    $scope.groups = [];
    $scope.roles = [];

    $scope.init = function(data) {
        $scope.users = data.users;
        $scope.groups = data.groups;
        $scope.roles = data.roles;
        console.log(data);
    };

    $scope.user_roles = function(user) {
        var roles = [];
        angular.forEach(user.roles, function(v, k) {
            if(v) {
              roles.push(k);
            }
        });
        return angular.toJson({id:user.id, roles:roles});
    };

    $scope.AddEditUser = function(id) {
        var i;
        var modaluser = {username:"New user"};
        // id may be not defined, we do handle that!
        for(i=0; i < $scope.users.length; i++) {
            console.log(id);
            console.log($scope.users[i]);
            if($scope.users[i].id == id) {
                modaluser = $scope.users[id];
            }
        }
        var modalInstance = $modal.open({
            templateUrl: 'UserModal.html',
            controller: ModalInstanceCtrl,
            resolve: {
                user: function() { return modaluser; }
            }
        });
        modalInstance.result.then(function (selected) {
            if(selected.device && selected.port) {
                $scope.modified = true;
                p.state = 'modified';
                // mark port as no longer available
                p.device = { title: selected.device.title, url: selected.device.url,
                             portid: selected.port.id };
            }

        }, function () {
            // dismissed
        });

    };
});
