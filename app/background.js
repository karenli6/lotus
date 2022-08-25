
// chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
//   console.log("here")
//   console.log(tabs[0].url);
//   // Send a message to the client.
// });
// var microsecondsPerWeek = 1000 * 60 * 60 * 24 * 7;
// var oneWeekAgo = (new Date).getTime() - microsecondsPerWeek;

// chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
//   console.log("all tabs: ", tabs)

//   chrome.tabs.sendMessage(tabs[0].id, {greeting: "hello"}, function(response) {
//     console.log(response.farewell);
//   });
// });
// Example of a simple user data object
const user = {
  username: 'demo-user'
};



function myAlert(){
  console.log("inside alert");

  // chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
  //   console.log("all tabs: ", tabs)
  //   chrome.tabs.sendMessage(tabs[0].id, {greeting: "hello"}, function(response) {
  //     console.log(response);
  //   });
  // });
  
  
  var date = (new Date).getTime();
  console.log("current time is", date);

  // To look for history items visited in the last day,
  // subtract a day of microseconds from the current time.
  var microsecondsPerDay = 1000 * 60 * 60 * 24;
  var oneDayAgo = (new Date).getTime() - microsecondsPerDay;

  if (date >= 1661441718603){
    console.log("--- UPDATING HISTORY ----");

    chrome.history.search({
      'text': '',              // Return every history item....
      'startTime': oneDayAgo  // that was accessed less than one week ago.
    },
    function(historyItems) {
      var array = []
      for (var i = 0; i < historyItems.length; ++i) {
        var url = historyItems[i].url;
        array.push(url);

      }

      chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
        // 2. A page requested user data, respond with a copy of `user`
        if (message === 'get-user-data') {
          sendResponse(array);
        }
      });



    });
  var microsecondsPerMin = 1000 * 60;
  var oneMinuteLater = (new Date).getTime() + microsecondsPerMin;
  console.log("ONE MINUTE LATER: ", oneMinuteLater );
  // console.log(date == oneMinuteLater);
}
}

chrome.runtime.onInstalled.addListener(() => {
  // var microsecondsPerMin = 1000 * 60;
  // var oneMinuteLater = (new Date).getTime() - microsecondsPerWeek;
  
  myAlert();
});


