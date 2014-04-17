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


    $scope.ModalHeader = function() {
        if(user) {
            return "Edit " + user.username;
        }
        else {
            return "Add a new user";
        }
    };
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

usergroup.directive("validUsername", function($rootScope, $http) {
  /*
   * Validate a username against a remote validator. A username may be
   * invalid because it's already used or because it contains invalid
   * characters.
   *
   * An existing username can be changed, but if the user brings it back to
   * its original it must still be accepted (eventhough the remote validator
   * would claim it is used). This directive implements some countermeasures
   * to make sure this works, but currently it won't work between modal saves.
   *
   * E.g. a user edits user 'ivo', changes it to 'ivo2', closes the dialog (but
   * no save!). The user edits this user (ivo2) again and restores it to 'ivo',
   * which in this case won't be accepted anymore.
   */
  var toId;

  return {
    restrict: 'A',
    require: '?ngModel',
    link: function(scope, elem, attr, ngModel) {
      //when the scope changes, check the email.
      var original = scope.$eval(attr.ngModel);
      scope.$watch(attr.ngModel, function(value) {
        // if there was a previous attempt, stop it.
        if(toId) {
            clearTimeout(toId);
            toId = null;
        }

        // if the name is unchanged, it's okay
        if(value == original) {
            ngModel.$setValidity('validUsername', true);
            return;
        }

        // delay to avoid chattyness
        toId = setTimeout(function(){
            $http.get($rootScope.urlbase + '?config=users_groups&action=validate_username&username=' + value).success(function(data) {
              ngModel.$setValidity('validUsername', data.isValid);
            });
            toId = null;

        }, 200);
      });
    }
  };
});
