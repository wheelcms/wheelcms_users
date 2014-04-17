usergroup = angular.module('usergroup', ["basemodel"]);

usergroup.factory('UserModel', ["BaseModel", "$rootScope",
                                function(BaseModel, $rootScope) {

    var service = Object.create(BaseModel);
    var _roles = [];

    return angular.extend(service, {
        construct_method: function(data) {
            return $rootScope.urlbase + '?config=users_groups&action=user_data';
        },
        handle_data: function(data) {
            _roles = data.roles || [];
            return data;
        },

        users: function() {
            return this.data().existing;
        },

        update_user: function(id, user) {
            var u = this.update(id, user);
            u.roles = {};
            angular.copy(user.roles||{}, u.roles);
        },

        add_user: function(user) {
            id = this.add(user);
            var u = this.find(id);
            u.roles = {};
            angular.copy(user.roles||{}, u.roles);

        },

        roles: function() {
            return _roles;
        }

    });
}]);

usergroup.controller('AddEditModalCtrl', function($scope, $modalInstance, user,
                                                  UserModel) {
    $scope.user = angular.copy(user) || {};
    $scope.model = UserModel;


    $scope.ok = function () {
      $modalInstance.close($scope.user);
    };

    $scope.remove = function () {
      $modalInstance.close("delete");
    };

    $scope.cancel = function () {
      $modalInstance.dismiss('cancel');
    };

    $scope.canDelete = function() {
        return !!user;
    };
});


usergroup.controller('UserGroupCtrl', ["$scope", "$modal", "UserModel",
                                      function($scope, $modal, UserModel) {
    $scope.model = {};

    $scope.changed = false;

    UserModel.async().then(function(data) {
        $scope.model = UserModel;
    });


    $scope.newEditUser = function(userid) {
        var user = UserModel.find(userid);
        var modalInstance = $modal.open({
            templateUrl: "UserModal.html",
            controller: "AddEditModalCtrl",
            resolve: {
                user: function() { return user; }
            }
        });
        modalInstance.result.then(function(userdata) {
            $scope.changed = true;
            if(userdata == "delete") {
                UserModel.remove(userid);
                return;
            }
            if(userid) {
                UserModel.update_user(userid, userdata);
            }
            else {
                UserModel.add_user(userdata);
            }
        });

    };

    $scope.save = function() {
        UserModel.save();
        $scope.changed = false;
    };
}]);
