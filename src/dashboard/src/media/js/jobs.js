Date.prototype.getArchivematicaDateTime = function()
  {
    return this.getArchivematicaDateString();
  };

Date.prototype.getArchivematicaDateString = function()
  {
    var pad = function (n)
      {
        return n < 10 ? '0' + n : n;
      }
 
    var dateText = this.getFullYear()
      + '-' + pad(this.getMonth() + 1)
      + '-' + pad(this.getDate())
      + ' ' + pad(this.getHours())
      + ':' + pad(this.getMinutes());

    return dateText;
  };

var BaseSipView = Backbone.View.extend({

  className: 'sip',

  events: {
    'click .sip-row': 'openPanel',
    'click .sip-row > .sip-detail-actions > .btn_show_panel': 'openPanel',
    'click .sip-row > .sip-detail-actions > .btn_show_jobs': 'toggleJobs',
    'click .sip-row > .sip-detail-actions > .btn_remove_sip': 'remove'
  },

  render: function()
    {
      var self = this;

      $(this.el).html(this.template(this.model.toJSON()));

      this.$jobContainer = this.$('.sip-detail-job-container');

      this.$('.sip-detail-actions > a').twipsy();

      $(this.el).hover(
        function() {
          // temporarily increase bottom margin if hovering over closed SIP container
          var nextSibling = $(self.el).next();
          if (nextSibling.children(':nth-child(2)').is(':visible')) {
            // ease in margin setting
            $(self.el).animate({
              'margin-bottom': '10px',
              queue: true
            }, 200);
          }
        },
        function() {
          // open SIP containers don't need temporary bottom margin adjustment
          if (!$(self.el).children(':nth-child(2)').is(':visible')) {
            self.updateBottomMargins();
          }
         }
      );

      return this;
    },

  toggleJobs: function(event)
    {
      var self = this;

      event.preventDefault();
      event.stopPropagation();

      if (this.$jobContainer.is(':visible'))
      {
        this.$jobContainer.slideUp('fast', function()
          {
            self.updateBottomMargins();
          }
        );

        $(this.el).removeClass('sip-selected');
      }
      else
      {
        this.updateJobContainer();
      }
    },

  updateJobContainer: function()
    {
      var groups = {}
        , group
        , self = this;

      // separate jobs by group
      this.model.jobs.each(function(job)
        {
          group = job.get('microservicegroup');
          groups[group] = groups[group] || new JobCollection();
          groups[group].add(job);
        }
      );

      // take note of any groups that have been open by the user before
      // we refresh the DOM
      var openGroups = [];
      $(this.$jobContainer).children('.microservicegroup').each(function () {
        // if group is open, take note of it
        var group = $(this).children(':first').children('.microservice-group-name').text()
          , visible = $(this).children(':nth-child(2)').is(':visible');

        if (visible) {
          openGroups.push(group);
        }
      });

      // refresh DOM
      this.$jobContainer.empty();

      // display groups
      for(group in groups) {
        var group = new MicroserviceGroupView({
          name: group,
          jobs: groups[group]
        });
        group.template = _.template(
          $('#microservice-group-template').html()
        );
        this.$jobContainer.append(group.render().el);
      }

      // re-open any groups that were open before the DOM elements were refreshed
      $(this.$jobContainer).children('.microservicegroup').each(function () {
        var group = $(this).children(':first').children('.microservice-group-name').text()
          , visible = $(this).children(':nth-child(2)').is(':visible');

        // show jobs in group if group was open
        if (openGroups.indexOf(group) != -1) {
          $(this).children(':nth-child(2)').show();
        }
      });

      this.$jobContainer.slideDown('fast', function()
        {
          self.updateBottomMargins();
        }
      );
      $(this.el).addClass('sip-selected');
    },

  updateBottomMargins: function()
    {
       $('.sip').each(function()
         {
           // create bottom margin if next SIP has been toggled open
           var finalBottomMargin =
             ($(this).children(':nth-child(2)').is(':visible'))
               ? '10px'
               : '0px';

            // ease in margin setting
            $(this).animate({
              'margin-bottom': finalBottomMargin,
              queue: true
            }, 200);
         }
       );
    },

  update: function()
    {
      // Reload nested collection
      this.model.loadJobs(); // .refresh() shouldn't work here

      // Update timestamp
      this.$('.sip-detail-timestamp').html(this.getIngestStartTime());

      // Update icon
      this.updateIcon();

      if (this.$jobContainer.is(':visible'))
      {
        this.updateJobContainer();
      }
    },

  updateIcon: function()
    {
      this.$('.sip-detail-icon-status').html(this.model.jobs.getIcon());
    },

  getIngestStartTime: function()
    {
      // Use "Assign file UUIDs and checksums" micro-service to represent ingest start time
      // TODO: fastest solution would be to use the first microservice of the collection, once is ordered correctly
      var job = this.model.jobs.detect(function(job)
        {
          return job.get('type') === 'Assign file UUIDs and checksums';
        });

      // Fallback: use last micro-service timestamp
      if (undefined === job)
      {
        job = this.model.jobs.last();
      }

      return new Date(job.get('timestamp') * 1000).getArchivematicaDateTime();
    }
});

var MicroserviceGroupView = Backbone.View.extend({

  className: 'microservicegroup',

  initialize: function()
    {
      this.name = this.options.name || '';
      this.jobs = this.options.jobs || new JobCollection();
    },

  render: function()
    {
      var self = this;

      // render group wrapper
      $(this.el).html(this.template({
        name: this.name
      }));

      // add container for jobs
      var jobDiv = $('<div></div>').hide();
      $(this.el).append(jobDiv);

      // render jobs to container
      this.jobs.each(function(job) {
        var view = new JobView({model: job});
        jobDiv.append(view.render().el);
      });

      // toggle job container when user clicks handle
      $(this.el).children(':first').click(function() {
        var arrowEl = $(this).children('.microservice-group-arrow')
          , arrowHtml = (jobDiv.is(':visible')) ? '&#x25B8' : '&#x25BE';
        $(arrowEl).html(arrowHtml);
        jobDiv.toggle('fast');
      });

      return this;
    }
});

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
                title: this.model.sip.get('directory') + ' &raquo ' + this.model.get('type') + ' &raquo Tasks',
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
            'Awaiting decision':    '#ffffff',
            'Executing command(s)': '#fedda7',
          },
          bgColor;

      return (statusColors[status] == undefined)
        ? '#d8f2dc'
        : statusColors[status];
    }
});
