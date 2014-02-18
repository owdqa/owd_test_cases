
var results_partial_weekly = (function Results() {
	var ROWS_TO_JUMP = 1;
	
	var FAILURES_COLUMN = 3;
	var KNOWN_BUGS_COLUMN = 4;
	var DATE_COLUMN = 0;
	var LINK_COLUMN = 9;
	var PERCENT_COLUMN = 5;


	function handleError() {
		alert("No results found for your selection!!")
		//Going back
		location.href = location.href.split("/").slice(0,-2).join("/");
	};

	function processData(data) {
		// console.log("Data:", data)
		var arrays = $.csv.toArrays(data);

		prev_info_arrays = arrays.slice(0, ROWS_TO_JUMP);
		table_arrays = arrays.slice(ROWS_TO_JUMP);

		/** PREV INFO **/
		var i = 0;
		for (i; i < prev_info_arrays.length; i++) {
			_appendPrevInfo(prev_info_arrays[i]);
		}

		var tokens = location.href.split("/");
		_appendPrevInfo("Device: " + tokens[tokens.length - 3])
		_appendPrevInfo("Version: " + tokens[tokens.length - 2])

		function _appendPrevInfo(what) {
			$("#prev-info .info-wrapper").append($(document.createElement("div"))
										.attr("class", "info-elem"))
										.append(what);
		}
		

		/** FILL THE TABLE ITSELF **/
		// console.log("Arrays:", arrays)
		var table = generateTable(table_arrays);

		$("body").append($(document.createElement("table"))
									.append(table)
									.attr("id", "results")
						);
		postprocessTable();
		$("#results").tablesorter({
			sortList: [[DATE_COLUMN, 0]]
		}); // {sortList: [[0,0], [1,0]]} 
	}

	function postprocessTable() {
		$.each($("#results tbody tr"), function(item, elem) {
			$.each($(elem).find("td"), function (item, elem) {
				if ((item == FAILURES_COLUMN) && 
							(parseInt($(elem).html()) > 0)){

					$(elem).closest("tr").addClass("error");
				} else if ((item == PERCENT_COLUMN) &&
					(_inRange(elem))) {
					if (($(elem).closest("tr").hasClass("error"))){
						$(elem).closest("tr").addClass("warning")
					}
				}
			})
		});

		_addLegend();
		function _addLegend() {
			var text_failures = "Possible regression failures - please investigate.";
			var text_bugs = "If our Jira user story contains test cases that are blocked	and 'Run blocked tests: YES' is set, then the blocked test cases will run. If they fail they go in the 'expected failures' category.";

			$.each($("#results thead th"), function (item, elem) {
				if (item == KNOWN_BUGS_COLUMN) {
					$(elem).attr({"title": text_bugs});
				} else if (item == FAILURES_COLUMN) {
					$(elem).attr({"title": text_failures});
				}
			});
		};

		function _inRange(elem) {
			var percent = parseInt($(elem).html().split("%")[0]);
			return (percent > 0 && percent <= 20)
		}
	};

	// build HTML table data from an array (one or two dimensional)
	function generateTable(data) {
		var html = '';
		var FAILURES_COLUMN = 2

		if (typeof(data[0]) === 'undefined') {
			return null;
		}

		if (data[0].constructor === String) {
			html += '<tr>\r\n';
			for (var item in data) {
				html += '<td>' + data[item] + '</td>\r\n';
			}
			html += '</tr>\r\n';
		}

		if (data[0].constructor === Array) {
			/*
			Do something to prevent unnecessary td fields
			*/
			for (var row in data) {

				if (data[row].length == 1) { //prevent from empty lines
					if (data[row][0] == "") {
						continue;
					}
				}

				if (row == 0) {
					var max = data[row].length; // This is gonna be my MAX
					html += '<thead>\r\n';
				} else if (row == 1) {
					html += '<tbody>\r\n';
				}
				html += '<tr>\r\n';

				for (var item in data[row]) {
					if (row > 0) { // not first row
						if (item < max) {

							if (item == LINK_COLUMN) {
								html += '<td><a href="' + _getPrefix() + data[row][item] +
								 '" target="_blank">' + 'Click here</a>'
							} else {
		  						html += '<td>' + data[row][item] + '</td>\r\n';
		  					}
						}
					} else {
		  				html += '<th>' + data[row][item] + '</th>\r\n';
					}
				}

				html += '</tr>\r\n';

				if (row == 0) {
					html += '</thead>\r\n';
				}
			}
			html += '</tbody>\r\n';
		}

		if(data[0].constructor === Object) {
			for(var row in data) {
		    	html += '<tr>\r\n';
		    	for(var item in data[row]) {
		      		html += '<td><a href="' + _getPrefix() + data[row][item] +
								 '" target="_blank">' + 'Click here</a>'
		    	}
		    	html += '</tr>\r\n';
		  	}
		}

		return html;
	}

	function _getPrefix() {
		var PUBLIC_ADDRESS =  "owd.tid.es";
		var PRIVATE_ADDRESS = "owd-qa-server";
		
		if (location.hostname == PUBLIC_ADDRESS) {
			return "http://" + location.hostname + "/qaReports/owd_tests";
		} else if (location.hostname == PRIVATE_ADDRESS) {
			return "http://" + location.hostname +"/owd_tests";
		} else {
			return ""
		}
	};

	return {
		processData : processData,
		handleError : handleError
	}

})();
