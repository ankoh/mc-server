var Promise = require("bluebird");
var net = require('net');

// Asynchronously test to open a tcp socket to a given host:port
exports.isReachableAsync = function (port, host) {
	return new Promise(function(resolve, reject){
		var conn = net.createConnection(port, host);
        conn.on('error', function(err) {
//            console.log("Error handler fired in isReachableAsync for " + host + ":" + port)
            conn.destroy();
            reject(new Error("Could not connect a TCP socket to " + host + ":" + port));
        }).on('connect', function(connect) {
            conn.destroy();
            resolve("Success");
        });
	});
};