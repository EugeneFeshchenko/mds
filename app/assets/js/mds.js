var mdsApp = angular.module('mdsApp', ['ui.bootstrap']);

mdsApp.controller('mainCtrl', ['$scope', '$http', function ($scope, $http) {
    $http.get('data.json').then(function(resp){
        $scope.pageSize = 25;
        $scope.page = localStorage['page'] ? localStorage['page'] : 1;

        $scope.recentNumber = localStorage['recentNumber'] ? localStorage['recentNumber'] : null;

        $scope.totalItems = resp.data.length;

        var startIndex = $scope.pageSize * ($scope.page-1);
        var endIndex = startIndex + $scope.pageSize;
        $scope.display_books = resp.data.slice(startIndex, endIndex);

        $scope.pageChanged = function(){
            localStorage['page'] = $scope.page;
            var startIndex = $scope.pageSize * ($scope.page-1);
            var endIndex = startIndex + $scope.pageSize;
            $scope.display_books = resp.data.slice(startIndex, endIndex);
        }

        $scope.setActive = function(number){
            $scope.recentNumber = number;
            localStorage['recentNumber'] = number;

        }
    })

}]);
