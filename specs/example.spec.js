var Calculator = require('../lib/example'),
	sinon = require('sinon');

describe('When adding one and two using the calculator', function () {
    var calculator;

    before(function () {
        calculator = new Calculator();
    });

    it('should result in three using the return style approach', function () {
        var result = calculator.add(1, 2);
        expect(result).equal(3);
    });
});

describe('When substracting six and eight using the calculator', function () {
    var calculator;
 
    before(function () {
        calculator = new Calculator();
    });
 
    it('should result in minus two the callback approach', function (done) {
        calculator.substract(6, 8, function(result) {
            assert.equal(result, -2);
            done();
        });
    });
});

describe('When multiplying nine and three using the calculator', function () {
    var calculator,
        eventEmitterStub,
        callbackSpy,
        clock;
 
    before(function () {
        calculator = new Calculator();
        clock = sinon.useFakeTimers();
        eventEmitterStub = sinon.stub(calculator, 'emit');
        callbackSpy = sinon.spy();
    });
 
    it('should emit the event before the callback', function (done) {
        calculator.multiply(9, 3, callbackSpy);
        clock.tick(1000);
        assert.equal(callbackSpy.called, true);
        assert.equal(eventEmitterStub.calledWithExactly('result', 27), true);
        assert.equal(eventEmitterStub.calledBefore(callbackSpy), true);
        done();
    });
 
    after(function () {
        clock.restore();
    });
});