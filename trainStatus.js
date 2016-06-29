var page = require('webpage').create();
var system = require('system');

// Variable Setup
var now = Date.now();
// Get our arguments.
// 0 is script name
// 1 is our station short code. Default is ALY
// 2 is our train nubmer. Default to 500
// 3 is our date. Default is today
var station     = system.args[1] || 'ALY';
var trainNumber = system.args[2] || 500;
var date        = system.args[3] || currentDateString();

console.log('Station: ' + station);
console.log('Train Number: ' + trainNumber);
console.log('Date: ' + date);

page.onConsoleMessage = function(msg, lineNum, sourceId) {
  console.log('CONSOLE: ' + msg + ' (line: ' + lineNum + ' in: "' + sourceId + '")');
};

page.open('https://tickets.amtrak.com/itd/amtrak', function(status) {
  if (status !== 'success') {
    console.log('[ERROR] Failure to load page');
    phantom.exit();
  }

  console.log("Loaded page in " + (Date.now() - now) + ' msec');
  page.evaluate(function(station, trainNumber, date, page) {
    // Create a fake click event
    var ev = document.createEvent('MouseEvents');
    ev.initEvent('click', true, true);
    // Get our status tab from the tab bar
    var checkStatusTab = document.getElementById('ff_tabbar_status');
    // Get its first child (which is a <span> with all the onclick handling
    checkStatusTab.children[0].dispatchEvent(ev);

    // Setup our request
    var stationInput = document.getElementById('status_to');
    var trainInput   = document.getElementById('status_train_num');
    var dateInput    = document.getElementById('wdfdate10');

    stationInput.value = station;
    trainInput.value   = trainNumber;
    dateInput.value    = date;

    var submitDiv = document.getElementById('ff_status_submit_wrapper');
    // SEND IT!
    var lastItem = submitDiv.children.length - 1;
    submitDiv.children[lastItem].click();

  }, station, trainNumber, date, page); // end page.evaluate

  setTimeout(function() {
    // page.render("submitted.png");
    var output;
    output = page.evaluate(function() {
      // Response?
      var responseDiv = document.getElementById('resp_by_train_num_status_details');
      return responseDiv.innerText;
    });
    console.log(output);
    }, 2000);

  setTimeout(function() {
    phantom.exit();
  }, 3000);
});


function currentDateString() {
  var date = new Date();

  function addPadding(n) { return n < 10 ? "0" + n : n; }

  // MM/DD/YYY
  return addPadding(date.getMonth() + 1) + "/" + addPadding(date.getDate()) + "/" + addPadding(date.getFullYear());

}

