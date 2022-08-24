// background.js

// let color = '#3aa757';
chrome.browserAction.onClicked.addListener(function() {
  chrome.tabs.executeScript( {file: "d3.v4.min.js"});
  chrome.tabs.executeScript( {file: "render.js" });
});
