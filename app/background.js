
// define refresh parameters
var previousDay = (new Date).getDay();
var microsecondsPerDay = 1000 * 60 * 60 * 24;
var microsecondsPerWeek = 1000 * 60 * 60 * 24 * 7;

// get user history data
function getRecentHistory() {
  var weekAgo = (new Date).getTime() - microsecondsPerWeek;

  console.log("---- WE ARE REFRESHING ----");

  // reset nextRefresh to 24 hours later
  nextRefresh = (new Date).getTime() + microsecondsPerDay;

  chrome.history.search({
    'text': '',
    'maxResults': 2000,
    'startTime': weekAgo
  },
    function (historyItems) {
      var array = []
      for (var i = 0; i < historyItems.length; ++i) {
        var url = historyItems[i].url;
        array.push(url);

      }

      chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
        // console.log("background script: LISTENING")
        if (message === 'get-user-data') {
          sendResponse(array);
        }
      });
    });

}

// event listener
chrome.tabs.onCreated.addListener(function (tab) {
  console.log(previousDay)
  var today = (new Date()).getDay();
  if (today !== previousDay) {
    // update previousDay
    previousDay = today;
    // update history and make API call
    getRecentHistory();
  } else {
    console.log("WE ARE HERE------")
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
      // console.log("background script: LISTENING")
      if (message === 'get-user-data') {
        sendResponse([]);
      }
    });
  }
})


// Check whether new version is installed
chrome.runtime.onInstalled.addListener(function (details) {
  if (details.reason == "install") {
    console.log("This is a first install!");

  } else if (details.reason == "update") {
    var thisVersion = chrome.runtime.getManifest().version;
    console.log("Updated from " + details.previousVersion + " to " + thisVersion + "!");
  }
});