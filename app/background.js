
// get user history data
function getRecentHistory() {
  var date = (new Date).getTime();
  console.log("current time is", date);

  // To look for history items visited in the last day,
  var microsecondsPerDay = 1000 * 60 * 60 * 24 * 4;
  var FourDaysAgo = (new Date).getTime() - microsecondsPerDay;

  if (date >= 1661441718603) {
    console.log("--- UPDATING HISTORY ----");

    chrome.history.search({
      'text': '',
      'maxResults': 1500,
      'startTime': FourDaysAgo
    },
      function (historyItems) {
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
    // [WIP] calculating future time cycle

  }
}

// event listener
chrome.tabs.onCreated.addListener(function (tab) {
  getRecentHistory();
})
