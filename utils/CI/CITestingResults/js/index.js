var main = (function () {
	function filterResults() {
		if (CITestingResults.hversion.value != "") {

			url = location.href.match( /^(http.+\/)[^\/]+$/ )[1] + 
				CITestingResults.hdevice.value + '/' + CITestingResults.hversion.value + 
				"/results_partial_daily.html";
			openBackWindow(url);
		} else {
			url = location.href.match( /^(http.+\/)[^\/]+$/ )[1] + 
				CITestingResults.hdevice.value + "/results.html";
			openBackWindow(url);
		}
	};

	function openBackWindow(url){
		var popupWindow = window.open(url);
	    if ($.browser.msie) {
	        popupWindow.blur();
	        window.focus();
	    } else {
	       blurPopunder();
	    }
	};

	function blurPopunder() {
	    var winBlankPopup = window.open("about:blank");
	    if (winBlankPopup) {
	        winBlankPopup.focus();
	        winBlankPopup.close()
	    }
	};

	return {
		filterResults  : filterResults,
		openBackWindow : openBackWindow
	}
})();
