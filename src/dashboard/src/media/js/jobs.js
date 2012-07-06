function utcDateToLocal(dateText) {
  dateText = dateText.replace('a.m.', 'AM').replace('p.m.', 'PM');
  var date = new Date(dateText + ' UTC');
  return date.getArchivematicaDateString();
}

function log(message) {
  try
  {
    console.log(message);
  }
  catch (error)
  {
    try
    {
      window.opera.postError(a);
    }
    catch (error)
    {
    }
  }
}

function optimizeWidth() {
  var width = document.documentElement.clientWidth;

  if (1020 > width)
  {
    document.body.className = 'w-lte-1020';
  }
  else if (1200 > width)
  {
    document.body.className = 'w-lte-1200';
  }
  else
  {
    document.body.className = '';
  }
};

function tooltipPlugin(options)
  {
    var settings = {
      xOffset: 10,
      yOffset: 20,
      width: 280
    };

    return this.each(function()
      {
        var $this = $(this);
        var $tooltip;

        if (options)
        {
          $.extend(settings, options);
        }

        if (undefined === settings.content)
        {
          settings.content = $this.attr('title');
        }

        $this
          .attr('title', '')
          .mouseover(function(event)
            {
              $('.tooltip').remove();

              $tooltip = $('<div class="tooltip">' + (undefined !== settings.title ? '<p class="tooltip-title">' + settings.title + '</p>' : '') + '<div class="tooltip-content">' + settings.content + '</div></div>')
                .hide()
                .css({
                  top: (event.pageY - settings.xOffset) + 'px',
                  left: (event.pageX + settings.yOffset) + 'px',
                  width: settings.width + 'px'})
                .fadeIn()
                .appendTo('body');
            })
          .mouseout(function(event)
            {
              $tooltip.remove();
            })
          .mousemove(function(event)
            {
              $tooltip.css({
                top: (event.pageY - settings.xOffset) + 'px',
                left: (event.pageX + settings.yOffset) + 'px'});
            })
          .click(function(event)
            {
              event.preventDefault();
            });
      });
  };

Sip = Backbone.Model.extend({

  methodUrl:
  {
    'delete': '/transfer/uuid/delete/'
  },

  sync: function(method, model, options)
    {
      if (model.methodUrl && model.methodUrl[method.toLowerCase()])
      {
        options = options || {};
        options.url = model.methodUrl[method.toLowerCase()].replace('uuid', this.get('id'));
      }

      Backbone.sync(method, model, options);
    },

  initialize: function()
    {
      this.loadJobs();
    },

  hasFinished: function()
    {
      return false === this.jobs.some(function(job)
        {
          return -1 < jQuery.inArray(job.get('currentstep'), ['Requires approval', 'Executing command(s)']);
        });
    },

  set: function(attributes, options)
    {
      Backbone.Model.prototype.set.call(this, attributes, options);

      if (undefined !== this.jobs && !this.hasFinished())
      {
        this.view.update();
      }
    },

  loadJobs: function()
    {
      // Nested collection
      this.jobs = new JobCollection(this.get('jobs'));

      var self = this;
      this.jobs.each(function(job)
        {
          job.sip = self;
        });
    }
});

Job = Backbone.Model.extend({});

JobCollection = Backbone.Collection.extend({

  model: Job,

  getIcon: function()
    {
      var path = '/media/images/'
        , icon
        , title;

      var statusIcons = {
        'Requires approval':    'bell.png',
        'Awaiting decision':    'bell.png',
        'Failed':               'cancel.png',
        'Executing command(s)': 'arrow_refresh.png',
        'Rejected':             'control_stop_blue.png'
      };

      var job = this.toJSON().shift();

      for(status in statusIcons) {
         if (job.currentstep == status) {
           icon = statusIcons[status];
           title = job.currentStep;
           break;
         }
      }

      if (
        job.microservicegroup == 'Reject SIP'
        || job.type == 'Move to the rejected directory'
      ) {
        icon = 'control_stop_blue.png';
        title = 'Reject SIP';
      }

      icon = icon   || 'accept.png';
      title = title || 'Completed successfully';

      return '<img src="' + path + '/' + icon + '" title="' + title + '" />';
    },

  comparator: function(job)
    {
      return -1 * job.get('timestamp');
    }
});

var BaseSipView = Backbone.View.extend({

  className: 'sip',

  events: {
    'click .sip-row': 'toggleJobs',
    'click .sip-row > .sip-detail-actions > .btn_show_panel': 'openPanel',
    'click .sip-row > .sip-detail-actions > .btn_show_metadata': 'openPanel',
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
            // localize UTC dates
            $('.utcDate').each(function() {
              $(this).text(utcDateToLocal($(this).text()));
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
    },

  // augment dashboard action select by using a pop-up with an enhanced select widget
  activateEnhancedActionSelect: function($select, statusObject)
    {
      $select.hover(function() {
        // if not showing proxy selector and modal window
        if (!statusObject.bigSelectShowing)
        {
          // clone action selector
          var $proxySelect = $select.clone();

          // display action selector in modal window
          $('<div class="modal hide" id="big-choice-select-modal"><div class="modal-header"><button type="button" class="close" id="big-choice-select-close" data-dismiss="modal">×</button><h3>Select an action...</h3></div><div class="modal-body" id="big-choice-select-body"></div><div class="modal-footer"><a href="#" class="btn" data-dismiss="modal" id="big-choice-select-cancel">Cancel</a></div></div>')
          .modal({show: true});
          $('#big-choice-select-body').append($proxySelect);

          // style clone as Select2
          $proxySelect.select2();

          // proxy selections to action selector
          $proxySelect.change(function()
                  {
            $select.val($(this).val());
            $select.trigger('change');
            $('#big-choice-select-modal').remove();
          });

          // allow another instance to show if modal is closed
          $('#big-choice-select-close, #big-choice-select-cancel').click(function()
          {
            statusObject.bigSelectShowing = false;
            $('#big-choice-select-modal').remove();
          });

          // prevent multiple instances of this from displaying at once
          statusObject.bigSelectShowing = true;
        }
      });
    }
});

BaseDirectoryBrowserView = Backbone.View.extend({

  id: 'directory-browser',

  events: {
      'click #directory-browser-tab > a': 'remove',
      'click .dir > a': 'showDir',
      'click .file > a': 'showFile',
      'click .parent > a': 'showParent'
    },

  initialize: function()
    {
      _.bindAll(this, 'render');

      this.render();
    },

  render: function()
    {
      $('#directory-browser').remove();

      $(this.el).html(this.template).appendTo('body');

      $(this.el).fadeIn('fast');

      this.listContents();

      this.$('#directory-browser-content').resizable({ handles: 'w, s, sw' });

      return this;
    },

  remove: function(event)
    {
      event.preventDefault();

      $(this.el).fadeOut('fast', function()
        {
          $(this).remove();
        });
    },

  listContents: function(path)
    {
      var $ul = $('<ul></ul>');

      if (undefined === path)
      {
        path = '.';
      }

      var self = this;

      $.ajax({
        data: { path: undefined === path ? '.' : path },
        context: self,
        url: '/jobs/explore/' + this.options.uuid + '/',
        type: 'GET',
        success: function(data)
          {
            for (i in data.contents)
            {
              var item = data.contents[i];
              $ul.append('<li class="' + item.type + '"><a href="#"' + (undefined !== item.size ? ' title="' + parseInt(item.size / 1024, 10) + ' kB"' : '') + '>' + item.name + '</a></li>');
            }

            self.parent = data.parent;
            self.base = data.base;
          },
        complete: function()
          {
            this.$('#directory-browser-content')
              .html($ul).height($ul.height());
          }
      });
    },

  showDir: function(event)
    {
      event.preventDefault();

      this.listContents(this.buildPath($(event.target).text()));
    },

  showFile: function(event)
    {
      event.preventDefault();

      var $target = $(event.target);
      var source = '/jobs/' + this.options.uuid + '/explore/?path=' + this.buildPath($target.text());

      // Use iframe tag to open the browser download dialog...
      $('body').append('<iframe style="display: none;" src="' + source + '" />');
    },

  buildPath: function(destination)
    {
      return (this.base.length ? this.base + '/' : '') + destination;
    },

  showParent: function(event)
    {
      event.preventDefault();

      this.listContents(this.parent);
    }
});

BaseAppView = Backbone.View.extend({

  interval: window.pollingInterval ? window.pollingInterval * 1000: 5000,

  idle: false,

  initialize: function(options)
    {
      this.statusUrl = options.statusUrl;

      _.bindAll(this, 'add', 'remove');
      Sips.bind('add', this.add);
      Sips.bind('remove', this.remove);

      window.statusWidget = new window.StatusView();

      // this.manageIdle();

      this.poll(true);

      // Close pop-ups when click event is triggered somewhere else
      $(document).click(function(event)
        {
          $target = $(event.target);

          if (!$target.parents().is('#directory-browser') && !$target.is('.btn_browse_job'))
          {
            $('#directory-browser').fadeOut('fast', function()
              {
                $(this).remove();
              });
          }

        });
    },

  manageIdle: function()
    {
      $.idleTimer(this.interval * 10);

      var self = this;
      $(document)
        .bind('idle.idleTimer', function()
          {
            self.idle = true;
            $('<span id="polling-notification">Polling was disabled until next user activity is detected.</span>').appendTo('body');
          })
        .bind('active.idleTimer', function()
          {
            self.idle = false;
            $('#polling-notification').fadeOut('fast');
            self.poll();
          });
    },

  add: function(sip)
    {
      var view = new SipView({model: sip});
      var $new = $(view.render().el).hide();

      // Get the current position in the collection
      var position = Sips.indexOf(sip);

      if (0 === position)
      {
        this.el.children('#sip-body').prepend($new);
      }
      else
      {
        var $target = this.el.find('.sip').eq(position);

        if ($target.length)
        {
          $target.before($new);
        }
        else
        {
          this.el.children('#sip-body').append($new);
        }
      }

      if (!this.firstPoll)
      {
        // Animation
        $new.addClass('sip-new').show('blind', {}, 500, function()
          {
            $(this).removeClass('sip-new', 2000);
          });
      }
      else
      {
        $new.show();
      }
    },

  remove: function(sip)
    {
      $(sip.view.el).hide('blind', function()
        {
          $(this).remove();
        });
    },

  cacheNotifications: function(notifications)
    {
      // initialize local storage
      if (localStorage.getItem('archivematicaNotifications') == null)
      {
         localStorage.setItem('archivematicaNotifications', JSON.stringify({
           'notifications': [],
           'dismissed': []
         }));
      }

      // get currently stored notifications
      var localNotificationData = JSON.parse(localStorage.getItem('archivematicaNotifications'));

      // cycle through existing notifications
      for (var notificationIndex in notifications)
      {
        var notification = notifications[notificationIndex];

        // see if notification already exists
        var exists = false;
        for (var index in localNotificationData.notifications)
        {
          var localNotification = localNotificationData.notifications[index];
          if (localNotification.id == notification.id)
          {
            exists = true;
          }
        }

        //  add to localstorage if not already there and not dismissed
        if (!exists && localNotificationData.dismissed.indexOf(notification.id) == -1)
        {
          localNotificationData.notifications.push(notification);
        }
      }

      localStorage.setItem('archivematicaNotifications', JSON.stringify(localNotificationData))
    },

  poll: function(start)
    {
      this.firstPoll = undefined !== start;

      $.ajax({
        context: this,
        dataType: 'json',
        type: 'GET',
        url: this.statusUrl + '?' + new Date().getTime(),
        beforeSend: function()
          {
            window.statusWidget.startPoll();
          },
        error: function()
          {
            window.statusWidget.text('Error trying to connect to database. Trying again...', true);
          },
        success: function(response)
          {
            var objects = response.objects;

            for (i in objects)
            {
              var sip = objects[i];
              var item = Sips.find(function(item)
                {
                  return item.get('uuid') == sip.uuid;
                });

              if (undefined === item)
              {
                // Add new sips
                Sips.add(sip);
              }
              else
              {
                // Update sips
                item.set(sip);
              }
            }

            // Delete sips
            if (Sips.length > objects.length)
            {
              var unusedSips = Sips.reject(function(sip)
                  {
                    return -1 < $.inArray(sip.get('uuid'), _.pluck(objects, 'uuid'));
                  });

              Sips.remove(unusedSips);
            }

            // MCP status
            if (response.mcp)
            {
              window.statusWidget.connect();
            }
            else
            {
              window.statusWidget.text('Error trying to connect to MCP server. Trying again...', true);
            }
          },
        complete: function()
          {
            var self = this;

            window.statusWidget.endPoll();

            if (!self.idle)
            {
              setTimeout(function()
                {
                  self.poll();
                }, this.interval);
            }
          }
      });
    }
});
