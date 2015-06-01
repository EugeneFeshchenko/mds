var mdsApp = angular.module('mdsApp', ['ui.bootstrap', 'ui.router']);

mdsApp.config(function($stateProvider, $urlRouterProvider) {

    $urlRouterProvider.otherwise("/");

    $stateProvider
        .state('default', {
            url: "/",
            templateUrl: "app/templates/default.html",
            controller: 'mainCtrl',
        })
        .state('author', {
            url: "/author/:name/",
            templateUrl: "app/templates/author.html",
            controller: 'authorCtrl',
        })
})


.controller('mainCtrl', ['$scope', '$http', '$timeout', function ($scope, $http, $timeout) {
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
    })

    	
    document.addEventListener("deviceready", onDeviceReady, false);
    function onDeviceReady() {
	fileTransfer = new FileTransfer();
	fileTransfer.onprogress = function(result){	 
	    if (result.lengthComputable){
		var percent = result.loaded / result.total * 100;
		percent = Math.round(percent);	
		
		if(percent > $scope.downloading.progress){
		    if (!$scope.to){ 
			$scope.to = $timeout(function(){$scope.downloading.progress = percent;}, 40);
			$scope.to.then(function(){$scope.to=null;});
		    }
		}
	    };	
	}; 
    }
    
    
    $scope.download = function(book){
	$scope.download_in_progress=true;
	var name = book.link.href.split('/').pop();
	$scope.downloading = {'id':book.number, 'progress':0};
	var uri = encodeURI(book.link.href);
	
	fileTransfer.download(
	    uri,
	    'cdvfile://localhost/persistent/Download/'+name,
	    function(entry) {
                $scope.recentNumber = book.number;
                localStorage['recentNumber'] = book.number;	
		alert('Загрузка завершена');
		$scope.download_in_progress=false;
		$scope.downloading = {'id':-1, 'progress':0};
		$scope.$apply();
	    },
	    function(error) {
		$scope.downloading = {'id':-1, 'progress':0};
		$scope.$apply();
	    }
	);
    }
}])

.controller('authorCtrl', ['$scope', '$http', '$stateParams',function($scope, $http, $stateParams){

    $scope.name = $stateParams.name;
    
    $http.get('data.json').then(function(resp){
        var books = [];
        
        for (var i=0; i<resp.data.length; i++){
            if (resp.data[i].author == $scope.name)
            books.push(resp.data[i]);
        }
        $scope.books = books.sort();
    })
}]);
