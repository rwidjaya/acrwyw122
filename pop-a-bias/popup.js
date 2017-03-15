//Getting the url of the current tab
function url_query () {
	chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
    	var newsUrl = tabs[0].url;
    	//console.log(typeof(newsUrl))
    
    var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function() {
  		if (xmlhttp.readyState == 4) {
		// JSON.parse does not evaluate the attacker's scripts.
			if (xmlhttp.responseText){
			    var resp = JSON.parse(xmlhttp.responseText);
			    console.log(resp);
  			}
		}
	}
	xmlhttp.open('POST', 'http://localhost:5001/bias_busted_dataonly', true);
	xmlhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	xmlhttp.send('url=' + encodeURIComponent(newsUrl));
	});}




function totallyAwesome() {
  // do something TOTALLY awesome!
}

function awesomeTask() {
  awesome();
  totallyAwesome();
}

function clickHandler(e) {
  setTimeout(awesomeTask, 1000);
}

function main() {
  // Initialization work goes here.
}

// Add event listeners once the DOM has fully loaded by listening for the
// `DOMContentLoaded` event on the document, and adding your listeners to
// specific elements when it triggers.
document.addEventListener('DOMContentLoaded', function () {
  document.querySelector('.action-button').addEventListener('click', url_query);
  main();
});



/*
var xmlhttp = new XMLHttpRequest();
xmlhttp.onreadystatechange = function() {
  if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
    alert('Finished downloading ' + document.title);
  } else if (xmlhttp.readyState == 4) {
    alert('Something went wrong: ' + xmlhttp.status);
  }
}
xmlhttp.open('POST', 'http://my.server.url:8801/', true);
xmlhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
xmlhttp.send('url=' + encodeURIComponent(youtubeURL));
*/