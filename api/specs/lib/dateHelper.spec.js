var dateHelper = require('../../lib/dateHelper');

describe('When converting a date into a MySQL date string', function () {
    it('the result should match the format regex', function () {
        var now = '30 July 2010 15:05 UTC';
        expect(now).to.not.match(/^\d+-\d+-\d+ \d+:\d+:\d+$/);
        expect(dateHelper.getMySQLDateString(now)).to.match(/^\d+-\d+-\d+ \d+:\d+:\d+$/);
    });
});

describe('When pretty printing a time difference', function() {
	it('a single second shall be printed in singular', function() {
		var now = new Date();
		var nowPlusOne = new Date(now);
		nowPlusOne.setSeconds(nowPlusOne.getSeconds() + 1);
		expect(dateHelper.getPrettyTimeDiff(now, nowPlusOne).prettyText).to.match(/second$/);
	});
	it('multiple seconds shall be printed in plural', function() {
		var now = new Date();
		var nowPlusTwo = new Date(now);
		nowPlusTwo.setSeconds(nowPlusTwo.getSeconds() + 2);
		expect(dateHelper.getPrettyTimeDiff(now, nowPlusTwo).prettyText).to.match(/seconds$/);
	});
	it('a single minute shall be printed in singular', function() {
		var now = new Date();
		var nowPlusOne = new Date(now);
		nowPlusOne.setMinutes(nowPlusOne.getMinutes() + 1);
		expect(dateHelper.getPrettyTimeDiff(now, nowPlusOne).prettyText).to.match(/minute$/);
	});
	it('multiple minutes shall be printed in plural', function() {
		var now = new Date();
		var nowPlusTwo = new Date(now);
		nowPlusTwo.setMinutes(nowPlusTwo.getMinutes() + 2);
		expect(dateHelper.getPrettyTimeDiff(now, nowPlusTwo).prettyText).to.match(/minutes$/);
	});
	it('a single hour shall be printed in singular', function() {
		var now = new Date();
		var nowPlusOne = new Date(now);
		nowPlusOne.setHours(nowPlusOne.getHours() + 1);
		expect(dateHelper.getPrettyTimeDiff(now, nowPlusOne).prettyText).to.match(/hour$/);
	});
	it('multiple hours shall be printed in plural', function() {
		var now = new Date();
		var nowPlusTwo = new Date(now);
		nowPlusTwo.setHours(nowPlusTwo.getHours() + 2);
		expect(dateHelper.getPrettyTimeDiff(now, nowPlusTwo).prettyText).to.match(/hours$/);
	});
	it('a single day shall be printed in singular', function() {
		var now = new Date();
		var nowPlusOne = new Date(now);
		nowPlusOne.setHours(nowPlusOne.getHours()+ 24);
		expect(dateHelper.getPrettyTimeDiff(now, nowPlusOne).prettyText).to.match(/day$/);
	});
	it('multiple days shall be printed in plural', function() {
		var now = new Date();
		var nowPlusTwo = new Date(now);
		nowPlusTwo.setHours(nowPlusTwo.getHours() + 48);
		expect(dateHelper.getPrettyTimeDiff(now, nowPlusTwo).prettyText).to.match(/days$/);
	});
});