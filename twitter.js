var Twitter = require('twitter');

var client = new Twitter({
  consumer_key: process.env.TWITTER_CONSUMER_KEY,
  consumer_secret: process.env.TWITTER_CONSUMER_SECRET,
  access_token_key: process.env.TWITTER_ACCESS_TOKEN_KEY,
  access_token_secret: process.env.TWITTER_ACCESS_TOKEN_SECRET
});

if (process.argv.length != 3) {
  exit(1);
}
var status = process.argv[2];

client.post('statuses/update', {status: status}, function(error, tweet, response) {
  if (error) console.log("[ERROR]: " + error);
  console.log(tweet);
  console.log(response);
});

