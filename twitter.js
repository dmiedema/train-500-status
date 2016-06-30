var Twitter = require('twitter');

var client = new Twitter({
  consumer_key: process.env.TWITTER_CONSUMER_KEY,
  consumer_secret: process.env.TWITTER_CONSUMER_SECRET,
  access_token_key: process.env.TWITTER_ACCESS_TOKEN_KEY,
  access_token_secret: process.env.TWITTER_ACCESS_TOKEN_SECRET
});

if (process.argv.length != 3) {
  console.log("[ERROR] Not enough arguments. We need 3, we had " + process.argv.length);
  exit(1);
}
var status = process.argv[2];

console.log("About to tweet:");
console.log(status);

client.post('statuses/update', {status: status}, function(error, tweet, response) {
  if (error) console.log("[ERROR]: " + error);
  console.log(tweet);
  console.log(response);
});

