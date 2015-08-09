var dateHelper = require('../../lib/dateHelper');

describe('dateHelper.getMySQLDateString', function () {
    it(' shall produce a valid MySQL date string given "30 July 2010 15:05 UTC"', function () {
        var now = '30 July 2010 15:05 UTC';
        expect(now).to.not.match(/^\d+-\d+-\d+ \d+:\d+:\d+$/);
        expect(dateHelper.getMySQLDateString(now)).to.match(/^\d+-\d+-\d+ \d+:\d+:\d+$/);
    });
});

describe('getPrettyTimeDiff', function() {
	it('shall print a single second in singular', function() {
		var now = new Date();
		var nowPlusOne = new Date(now);
		nowPlusOne.setSeconds(nowPlusOne.getSeconds() + 1);
		expect(dateHelper.getPrettyTimeDiff(now, nowPlusOne).prettyText).to.match(/second$/);
	});
	it('shall print multiple seconds in plural', function() {
		var now = new Date();
		var nowPlusTwo = new Date(now);
		nowPlusTwo.setSeconds(nowPlusTwo.getSeconds() + 2);
		expect(dateHelper.getPrettyTimeDiff(now, nowPlusTwo).prettyText).to.match(/seconds$/);
	});
	it('shall print a single minute in singular', function() {
		var now = new Date();
		var nowPlusOne = new Date(now);
		nowPlusOne.setMinutes(nowPlusOne.getMinutes() + 1);
		expect(dateHelper.getPrettyTimeDiff(now, nowPlusOne).prettyText).to.match(/minute$/);
	});
	it('shall print multiple minutes in plural', function() {
		var now = new Date();
		var nowPlusTwo = new Date(now);
		nowPlusTwo.setMinutes(nowPlusTwo.getMinutes() + 2);
		expect(dateHelper.getPrettyTimeDiff(now, nowPlusTwo).prettyText).to.match(/minutes$/);
	});
	it('shall print a single hour in singular', function() {
		var now = new Date();
		var nowPlusOne = new Date(now);
		nowPlusOne.setHours(nowPlusOne.getHours() + 1);
		expect(dateHelper.getPrettyTimeDiff(now, nowPlusOne).prettyText).to.match(/hour$/);
	});
	it('shall print multiple hours in plural', function() {
		var now = new Date();
		var nowPlusTwo = new Date(now);
		nowPlusTwo.setHours(nowPlusTwo.getHours() + 2);
		expect(dateHelper.getPrettyTimeDiff(now, nowPlusTwo).prettyText).to.match(/hours$/);
	});
	it('shall print a single day in singular', function() {
		var now = new Date();
		var nowPlusOne = new Date(now);
		nowPlusOne.setHours(nowPlusOne.getHours()+ 24);
		expect(dateHelper.getPrettyTimeDiff(now, nowPlusOne).prettyText).to.match(/day$/);
	});
	it('shall print multiple days in plural', function() {
		var now = new Date();
		var nowPlusTwo = new Date(now);
		nowPlusTwo.setHours(nowPlusTwo.getHours() + 48);
		expect(dateHelper.getPrettyTimeDiff(now, nowPlusTwo).prettyText).to.match(/days$/);
	});
});