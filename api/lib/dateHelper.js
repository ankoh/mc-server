// From: http://stackoverflow.com/questions/1787939/check-time-difference-in-javascript
exports.getPrettyTimeDiff = function (lowerDate, upperDate) {
  var result = {};
  var diff = upperDate.getTime() - lowerDate.getTime();

  // Get diff in days
  result.days = Math.floor(diff / 1000 / 60 / 60 / 24);
  diff -= result.days * 1000 * 60 * 60 * 24;
  // Get diff in hours
  result.hours = Math.floor(diff / 1000 / 60 / 60);
  diff -= result.hours * 1000 * 60 * 60;
  // Get diff in minutes
  result.minutes = Math.floor(diff / 1000 / 60);
  diff -= result.minutes * 1000 * 60;
  // Get diff in seconds
  result.seconds = Math.floor(diff / 1000);

  // Render the diffs into friendly duration string
  // Days
  var sDays = '00';
  if (result.days > 0) {
      sDays = String(result.days);
  }
  if (sDays.length === 1) {
      sDays = '0' + sDays;
  }
  // Format Hours
  var sHour = '00';
  if (result.hours > 0) {
      sHour = String(result.hours);
  }
  if (sHour.length === 1) {
      sHour = '0' + sHour;
  }
  //  Format Minutes
  var sMins = '00';
  if (result.minutes > 0) {
      sMins = String(result.minutes);
  }
  if (sMins.length === 1) {
      sMins = '0' + sMins;
  }
  //  Format Seconds
  var sSecs = '00';
  if (result.seconds > 0) {
      sSecs = String(result.seconds);
  }
  if (sSecs.length === 1) {
      sSecs = '0' + sSecs;
  }

  //  Set Duration
  var sDuration = sDays + ':' + sHour + ':' + sMins + ':' + sSecs;
  result.duration = sDuration;

  // Set friendly text for printing
  if(result.days === 0) {
      if(result.hours === 0) {
          if(result.minutes === 0) {
              var sSecHolder = result.seconds > 1 ? 'seconds' : 'second';
              result.prettyText = result.seconds + ' ' + sSecHolder;
          } else { 
              var sMinutesHolder = result.minutes > 1 ? 'minutes' : 'minute';
              result.prettyText = result.minutes + ' ' + sMinutesHolder;
          }
      } else {
          var sHourHolder = result.hours > 1 ? 'hours' : 'hour';
          result.prettyText = result.hours + ' ' + sHourHolder;
      }
  } else { 
      var sDayHolder = result.days > 1 ? 'days' : 'day';
      result.prettyText = result.days + ' ' + sDayHolder;
  }
  return result;
};


// Convert a date string into a mysql date string
exports.getMySQLDateString = function(dateString) {
  var myDate = new Date(dateString);
  var myDate_string = myDate.toISOString();
  myDate_string = myDate_string.replace("T"," ");
  myDate_string = myDate_string.substring(0, myDate_string.length - 5);
  return myDate_string;
};