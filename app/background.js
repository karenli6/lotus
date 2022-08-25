
// chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
//   console.log("here")
//   console.log(tabs[0].url);
//   // Send a message to the client.
// });

chrome.tabs.onUpdated.addListener( function( tabId,  changeInfo,  tab) {
  // let fs = require('fs');
  // with open("test.txt", "a") as myfile:
  //   myfile.write("appended text")

  console.log("UPDATED")
  console.log(tab.url)

    // import { f1 } from "./test.js";

    // f1();
    // let fs = require('fs');
    // fs.writeFile('urls.txt', data, (err) => {
      
    //   // In case of a error throw err.
    //   if (err) throw err;
    // })
    // fs.appendFileSync('urls.txt', tab.url);
    // fs.appendFileSync('urls.txt', "WRITTINGING ");

});


