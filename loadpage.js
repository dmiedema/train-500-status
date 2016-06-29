var page = require('webpage').create();
var system = require('system');

var now = Date.now();

page.open('https://tickets.amtrak.com/itd/amtrak', function(status) {
  if (status !== 'success') {
    console.log('[ERROR] Failure to load page');
  } else {
    console.log("Loaded page in " + (Date.now() - now) + ' msec');
  }
  phantom.exit();
});
