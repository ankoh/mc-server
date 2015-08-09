var netHelper = require('../../lib/netHelper');

describe('netHelper.isReachableAsync', function () {
    it(' shall reach www.google.de on TCP port 80', function (done) {
        netHelper.isReachableAsync('www.google.de', '80')
			.then(function() { done(); })
			.catch(function(err) { done(err); });
    });
    it(' shall reach www.google.de on TCP port 443', function (done) {
        netHelper.isReachableAsync('www.google.de', '443')
			.then(function() { done(); })
			.catch(function(err) { done(err); });
    });
    it(' shall reach www.heise.de on TCP port 80', function (done) {
        netHelper.isReachableAsync('www.heise.de', '80')
			.then(function() { done(); })
			.catch(function(err) { done(err); });
    });
    it(' shall not crash when trying to reach not-existing-hostname on TCP port 2312', function (done) {
        netHelper.isReachableAsync('not-existing-hostname', '2312')
			.then(function() { done(new Error("Could connect to non-existing-host")); })
			.catch(function(err) {
				expect(err.message).to.match(/Could not connect a TCP socket to not-existing-hostname:2312/);
				done();
			});
    });
});
