// Request promise is powered by Bluebird!
// https://www.npmjs.com/package/request-promise
var Promise = require('bluebird');
var RequestPromise = require('request-promise');
var netHelper = require('netHelper');

// The mendeleyCrawler is responsible for crawling publications by profile
function MendeleyCrawler(appId, clientSecret) {
    this.appId = appId;
    this.clientSecret = clientSecret;
    this.urlBase = 'https://api.mendeley.com:443/';
}

// Return if the mendeley api is reachable at the moment
MendeleyCrawler.prototype.apiIsReachable = function() {
    return netHelper.isReachableAsync(443, "api.mendeley.com");
};

// Get the authentication token from mendeley
MendeleyCrawler.prototype.getToken = function() {
     // Create authorizationHeader
    var encodedData = new Buffer(this.appId+':'+ this.clientSecret).toString('base64');
    this.authorizationHeader = 'Basic ' + encodedData;

    // GET https://api.mendeley.com:443/oauth/token
    var options = {
        method: 'POST',
        uri: this.urlBase + 'oauth/token',
        resolveWithFullResponse: true,
        headers : {
            "Authorization" : this.authorizationHeader
        },
        form : {
            grant_type: 'client_credentials',
            scope: 'all'
        }
    };
    return RequestPromise(options)
            .then(function(response) {
                var jsonToken = JSON.parse(response.body);
                var token = jsonToken.access_token;
                return token;
            });
};

// Given a userId and an access token, get all associated publications
MendeleyCrawler.prototype.getAllPublicationsByUserId = function(token, userId) {
    // GET https://api.mendeley.com:443/documents?profile_id=cooleuserid&authored=true
    var options = {
        method: 'GET',
        uri: this.urlBase + 'documents?profile_id=' + userId +'&authored=true&view=all',
        resolveWithFullResponse: true,
        headers: {
            "Authorization": "bearer " + token
        }
    };
    // Return request promise for the publication retrieval
    return RequestPromise(options)
            .then(function(response) {
                return JSON.parse(response.body);
            });
};

// Given a mendeley token and an profiles list - fetch all publications by profiles
MendeleyCrawler.prototype.getAllPublicationsByProfiles = function(token, profiles) {
  var promises = [];
  var results = [];
  var storePublications = function(publications) {
        results.push(publications);
       };
  for(var i = 0; i < profiles.length; i++) {
    var promise = this.getAllPublicationsByUserId(token, profiles[i].profile_id)
       .then(storePublications);
    promises.push(promise);
  }
  return Promise.all(promises)
    .then(function() {
      // console.log(results);
      return results;
    });
};


// Given an email get all mendeley profiles that are associated with it
MendeleyCrawler.prototype.getProfilesByEmail = function(token, email) {
   var options= {
       method: 'GET',
       uri: this.urlBase + 'profiles?email=' + email,
       resolveWithFullResponse: true,
        headers: {
            "Authorization": "bearer " +  token
        }
   };
   return RequestPromise(options);
};

// Export the mendeley crawler
module.exports = MendeleyCrawler;