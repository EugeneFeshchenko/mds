var mdsApp = angular.module('mdsApp', []);

mdsApp.controller('mainCtrl', ['$scope', '$http', function ($scope, $http) {
    $http.get('data.json').then(function(resp){
        $scope.page_size = 25;
        $scope.page = localStorage['page'] ? localStorage['page'] : 0;

        var start_index = $scope.page_size * $scope.page;
        var end_index = $scope.page_size * $scope.page + $scope.page_size;
        $scope.display_books = resp.data.slice(start_index, end_index);
    })

}]);
