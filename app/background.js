
function getRecentHistory(){
  
  var date = (new Date).getTime();
  console.log("current time is", date);

  // To look for history items visited in the last day,
  // subtract a day of microseconds from the current time.
  var microsecondsPerDay = 1000 * 60 * 60 * 24;
  var oneDayAgo = (new Date).getTime() - microsecondsPerDay;

  if (date >= 1661441718603){
    console.log("--- UPDATING HISTORY ----");

    chrome.history.search({
      'text': '', 
      'maxResults': 1000,
      'startTime': oneDayAgo 
    },
    function(historyItems) {
      var array = []
      for (var i = 0; i < historyItems.length; ++i) {
        var url = historyItems[i].url;
        array.push(url);

      }

      chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
        console.log("background script: LISTENING")
        if (message === 'get-user-data') {
          sendResponse(array);
        }
      });
    });
  // calculating future time
  // var microsecondsPerMin = 1000 * 60;
  // var oneMinuteLater = (new Date).getTime() + microsecondsPerMin;
  }
}

chrome.tabs.onCreated.addListener(function(tab) {
  getRecentHistory();
})
