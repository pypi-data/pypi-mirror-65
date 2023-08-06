'use strict';

angular.module('ajenti.packages', ['core']);


'use strict';

angular.module('core').config(function ($routeProvider) {
    $routeProvider.when('/view/packages/:managerId', {
        templateUrl: '/packages:resources/partial/index.html',
        controller: 'PackagesIndexController'
    });
});


'use strict';

angular.module('ajenti.packages').controller('PackagesIndexController', function ($scope, $routeParams, $location, notify, pageTitle, urlPrefix, packages, terminals, gettext) {
    pageTitle.set(gettext('Packages'));

    $scope.managerId = $routeParams.managerId;
    $scope.searchQuery = '';
    $scope.results = [];
    $scope.selection = [];
    $scope.selectionVisible = false;

    $scope.$watch('searchQuery', function () {
        if ($scope.searchQuery.length < 3) {
            return;
        }
        $scope.results = null;
        packages.list($scope.managerId, $scope.searchQuery).then(function (data) {
            $scope.results = data;
        }, function (err) {
            notify.error(gettext('Could not find packages'), err.message);
            $scope.results = [];
        });
    });

    $scope.updateLists = function () {
        return packages.updateLists($scope.managerId).then(function (data) {
            notify.info(gettext('Package list update started'));
        }, function (err) {
            notify.error(gettext('Package list update failed'), err.message);
        });
    };

    $scope.mark = function (pkg, op) {
        var _iteratorNormalCompletion = true;
        var _didIteratorError = false;
        var _iteratorError = undefined;

        try {
            for (var _iterator = $scope.selection[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
                var sel = _step.value;

                if (sel.package.id === pkg.id) {
                    $scope.selection.remove(sel);
                }
            }
        } catch (err) {
            _didIteratorError = true;
            _iteratorError = err;
        } finally {
            try {
                if (!_iteratorNormalCompletion && _iterator.return) {
                    _iterator.return();
                }
            } finally {
                if (_didIteratorError) {
                    throw _iteratorError;
                }
            }
        }

        $scope.selection.push({
            package: pkg,
            operation: op
        });
    };

    $scope.markForInstallation = function (pkg) {
        return $scope.mark(pkg, 'install');
    };

    $scope.markForUpgrade = function (pkg) {
        return $scope.mark(pkg, 'upgrade');
    };

    $scope.markForRemoval = function (pkg) {
        return $scope.mark(pkg, 'remove');
    };

    $scope.showSelection = function () {
        return $scope.selectionVisible = true;
    };

    $scope.hideSelection = function () {
        return $scope.selectionVisible = false;
    };

    $scope.doApply = function () {
        return packages.applySelection($scope.managerId, $scope.selection).then(function (data) {
            $scope.selection = [];
            var cmd = data.terminalCommand;
            terminals.create({ command: cmd, autoclose: true, redirect: '/view/packages/' + $scope.managerId }).then(function (id) {
                $location.path(urlPrefix + '/view/terminal/' + id);
            });
        }).catch(function () {
            notify.error(gettext('Could not apply changes'));
        });
    };
});


'use strict';

angular.module('ajenti.packages').service('packages', function ($http, $q, tasks) {
    this.getManagers = function () {
        return $http.get("/api/packages/managers").then(function (response) {
            return response.data;
        });
    };

    this.list = function (managerId, query) {
        return $http.get('/api/packages/list/' + managerId + '?query=' + query).then(function (response) {
            return response.data;
        });
    };

    this.get = function (managerId, packageId) {
        return $http.get('/api/packages/get/' + managerId + '/' + packageId).then(function (response) {
            return response.data;
        }).error(function (err) {
            return q.reject(err);
        });
    };

    this.updateLists = function (managerId) {
        return tasks.start('aj.plugins.packages.tasks.UpdateLists', [], { manager_id: managerId });
    };

    this.applySelection = function (managerId, selection) {
        return $http.post('/api/packages/apply/' + managerId, selection).then(function (response) {
            return response.data;
        });
    };

    return this;
});


