var BaseJobView = Backbone.View.extend({
  'getStatusColor': function(status) {
    // use colors to differentiate status of jobs
    var statusColors = {
          'Failed':               '#f2d8d8',
          'Rejected':             '#f2d8d8',
          'Requires approval':    '#ffffff',
          'Executing command(s)': '#fedda7',
        },
        bgColor;

    return (statusColors[status] == undefined)
      ? '#d8f2dc'
      : statusColors[status];
  }
});
