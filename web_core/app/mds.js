var mdsApp = angular.module('mdsApp', ['ui.bootstrap', 'ui.router', 'duScroll']);

mdsApp.config(function($stateProvider, $urlRouterProvider) {
    
    $urlRouterProvider.otherwise("/");

    $stateProvider
        .state('list', {
            url: "/",
            templateUrl: "app/templates/default.html",
            controller: 'mainCtrl',
        })
        .state('author', {
            url: "/author/:author",
            templateUrl: "app/templates/default.html",
            controller: 'mainCtrl',
        })
})


.controller('mainCtrl', ['$scope', '$http', '$timeout', '$stateParams', '$document', function ($scope, $http, $timeout, $stateParams, $document) {

    $scope.name = $stateParams.author;

    $http.get('data.json').then(function(resp){
        if ($scope.name){
            var books = [];        
            for (var i=0; i<resp.data.length; i++){
                if (resp.data[i].author == $scope.name)
                    books.push(resp.data[i]);
            }      
            $scope.display_books = books.sort();
        }
        else{
            $scope.pageSize = 25;
            $scope.page = localStorage['page'] ? localStorage['page'] : 1;

            $scope.recentNumber = localStorage['recentNumber'] ? localStorage['recentNumber'] : null;

            $scope.totalItems = resp.data.length;

            var startIndex = $scope.pageSize * ($scope.page-1);
            var endIndex = startIndex + $scope.pageSize;
            $scope.display_books = resp.data.slice(startIndex, endIndex);
        }

        $timeout(function(){
            var currentElement = angular.element(document.getElementsByClassName('current'));
            $document.scrollToElement(currentElement, 50, 50);
        }, 50);
        
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
	var name = book.author+'-'+book.name+'.mp3';
	$scope.downloading = {'id':book.number, 'progress':0};
	var uri = encodeURI(book.link.href);

	fileTransfer.download(
	    uri,
	    'cdvfile://localhost/persistent/Download/'+name,
	    function(entry) {
                $scope.recentNumber = book.number;
                localStorage['recentNumber'] = book.number;	
                navigator.notification.beep(1);
                navigator.notification.alert('Файл загружен в папку Downloads',  function(){}, 'Загрузка завершена!', 'Хорошо');
		$scope.download_in_progress=false;
		$scope.downloading = {'id':-1, 'progress':0};
		$scope.$apply();
	    },
	    function(error) {
		$scope.downloading = {'id':-1, 'progress':0};
		$scope.$apply();
	    }
	);        
    };

}])
