var BaseJobView = Backbone.View.extend({

  initialize: function()
    {
      _.bindAll(this, 'render', 'approveJob', 'rejectJob');
      this.model.bind('change', this.render);
      this.model.view = this;
    },

  showTasks: function(event)
    {
      event.preventDefault();

      $.ajax({
        context: this,
        type: 'GET',
        dataType: 'html',
        success: function(data)
          {
            $('<div class="task-dialog"></div>')
              .append('<table>' + $(data).find('tbody').html() + '</table>')
              .dialog({
                title: this.model.sip.get('directory') + ' &raquo ' + this.model.get('microservice') + ' &raquo Tasks',
                width: 640,
                height: 480,
                modal: true,
                buttons: [
                  {
                    text: 'Close',
                    click: function() { $(this).dialog('close'); }
                  }]
              });
          },
        url: '/tasks/' + this.model.get('uuid') + '/'
      });
    },

  browseJob: function(event)
    {
      event.preventDefault();
      event.stopPropagation();

      this.directoryBrowser = new window.DirectoryBrowserView({ uuid: this.model.get('uuid') });
    },

  approveJob: function(event)
    {
      event.preventDefault();

      $.ajax({
        context: this,
        data: { uuid: this.model.get('uuid') },
        type: 'POST',
        success: function(data)
          {
            this.model.set({
              'currentstep': 'Executing command(s)',
              'status': 0
            });

            this.model.sip.view.updateIcon();
          },
        url: '/mcp/approve-job/'
      });
    },

  rejectJob: function(event)
    {
      event.preventDefault();

      $.ajax({
        context: this,
        data: { uuid: this.model.get('uuid') },
        type: 'POST',
        success: function(data)
          {
            this.model.set({
              'currentstep': 'Rejected',
              'status': 0
            });

            this.model.sip.view.updateIcon();
            // this.model.sip.view.toggleJobs();
          },
        url: '/mcp/reject-job/'
      });
    },

  getStatusColor: function(status)
    {
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
