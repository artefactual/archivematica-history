$(function()
  {

    window.Sip = Backbone.Model.extend({
    
      initialize: function()
        {
          this.loadJobs();
        },

      hasFinished: function()
        {
          return false == this.jobs.some(function(job)
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

    window.SipCollection = Backbone.Collection.extend({

      model: Sip,

      url: '/sips/go/',

      initialize: function()
        {

        },

      comparator: function(sip)
        {
          return 0 - sip.get('timestamp');
        }

    });

    window.SipView = Backbone.View.extend({

      className: 'sip',

      template: _.template($('#sip-template').html()),

      events: {
        'click .sip-row > .sip-detail-icon-status > a': 'toggleJobs',
        'click .sip-row > .sip-detail-actions > .btn_show_jobs': 'toggleJobs',
        'click .sip-row > .sip-detail-actions > .btn_remove_sip': 'remove',
      },
     
      initialize: function()
        {
          _.bindAll(this, 'render', 'update', 'add', 'updateIcon');
          this.model.view = this;
          this.model.bind('change:timestamp', this.update);
        },
      
      render: function()
        {
          $(this.el).html(this.template(this.model.toJSON()));

          this.$jobContainer = this.$('.sip-detail-job-container');

          return this;
        },

      update: function()
        {
          // Reload nested collection
          this.model.loadJobs(); // .refresh() shouldn't work here

          // Update timestamp
          this.$('.sip-detail-timestamp').html(
            new Date(this.model.get('timestamp') * 1000).getArchivematicaDateTime()
          );

          // Update icon
          this.updateIcon();

          if (this.$jobContainer.is(':visible'))
          {
            this.$jobContainer.empty();

            var self = this;

            this.model.jobs.each(function(job)
              {
                var view = new JobView({model: job});
                self.$jobContainer.append(view.render().el);
              });
          }
        },

      updateIcon: function()
        {
          this.$('.sip-detail-icon-status > a').html(this.model.jobs.getIcon());
        },

      toggleJobs: function(event)
        {
          if (event)
          {
            event.preventDefault();
          }

          if (this.$jobContainer.is(':visible'))
          {
            this.$jobContainer.slideUp('fast');
            $(this.el).removeClass('sip-selected');
          }
          else
          {
            this.$jobContainer.empty();

            var self = this;
            this.model.jobs.each(function(job)
              {
                var view = new JobView({model: job});
                self.$jobContainer.append(view.render().el);
              });

            this.$jobContainer.slideDown('fast');
            $(this.el).addClass('sip-selected');
          }
        },

      remove: function(event)
        {
          event.preventDefault();

          $(this.el).addClass('sip-removing');

          var self = this;

          $('<div>' +
              '<p><strong>Are you sure you want to remove this SIP from the dashboard? Note that this does not delete the SIP or related entities.</strong></p>' +
              '<p>Directory: ' + this.model.get('directory') + '<br />UUID: ' + this.model.get('uuid') + '<br />Status: ' + $(this.el).find('.sip-detail-icon-status > a > img').attr('title') + '</p>' +
            '</div>').dialog(
            {
              modal: true,
              resizable: false,
              title: false,
              draggable: false,
              title: 'Remove SIP',
              width: 480,
              close: function(event, ui)
                {
                  if (event.which !== undefined)
                  {
                    $(self.el).removeClass('sip-removing');
                  }
                },
              buttons: [
                  {
                    text: 'Confirm',
                    click: function() {

                      var $dialog = $(this);

                      self.model.destroy({
                        success: function (model, response)
                          {
                            $dialog.dialog('close');

                            setTimeout(function()
                              {
                                $(self.el).hide('blind', function()
                                  {
                                    $(this).remove();
                                  });
                              }, 250);
                          },
                        error: function(model, response)
                          {
                            $dialog.dialog('close');
                            $(self.el).removeClass('sip-removing');
                          }

                      });
                    }
                  },
                  {
                    text: 'Cancel',
                    click: function() {
                        $(this).dialog('close');
                        $(self.el).removeClass('sip-removing');
                      }
                  }]
            });
        },

      getIngestStartTime: function()
        {
          // Use "Assign file UUIDs and checksums" micro-service to represent ingest start time
          // TODO: fastest solution would be to use the first microservice of the collection, once is ordered correctly
          var job = this.model.jobs.detect(function(job)
            {
              return job.get('microservice') == 'Assign file UUIDs and checksums';
            });

          // Fallback: use last micro-service timestamp
          if (undefined === job)
          {
            job = this.model.jobs.last();
          }

          return new Date(job.get('timestamp') * 1000).getArchivematicaDateTime();
        }
    });

    window.Job = Backbone.Model.extend({

    });
    
    window.JobCollection = Backbone.Collection.extend({
    
      model: Job,

      getIcon: function()
        {
          var path = '';
          var title = '';

          if (undefined !== this.find(function(job)
            {
              return 0 < job.get('status') || 'Requires approval' == job.get('currentstep');
            }))
          {
            path = '/media/images/bell.png';
            title = 'Requires approval';
          }
          else if (undefined !== this.find(function(job)
            {
              return 'Failed' == job.get('currentstep');
            }))
          {
            path = '/media/images/cancel.png';
            title = 'Failed';
          }
          else if (undefined !== this.find(function(job)
            {
              return 'Executing command(s)' == job.get('currentstep');
            }))
          {
            path = '/media/images/icons/arrow_refresh.png';
            title = 'Executing command(s)';
          }
          else if (undefined !== this.find(function(job)
            {
              return 'Rejected' == job.get('currentstep');
            }))
          {
            path = '/media/images/icons/control_stop_blue.png';
            title = 'Rejected';
          }
          else
          {
            path = '/media/images/accept.png';
            title = 'Completed successfully';
          }

          return '<img src="' + path + '" title="' + title + '" />';
        },

      comparator: function(job)
        {
          return 0 - job.get('timestamp');
        }

    });

    window.JobView = Backbone.View.extend({

      className: 'job',

      events: {
        'click .btn_browse_job': 'browseJob',
        'click .btn_approve_job': 'approveJob',
        'click .btn_reject_job': 'rejectJob',
        'click .btn_show_tasks': 'showTasks',
      },

      template: _.template($('#job-template').html()),

      initialize: function()
        {
          _.bindAll(this, 'render', 'approveJob', 'rejectJob');
          this.model.bind('change', this.render);
          this.model.view = this;
        },

      render: function()
        {
          $(this.el).html(this.template(this.model.toJSON()));

          if (-1 < jQuery.inArray(this.model.get('currentstep'), ['Requires approval', 'Failed', 'Rejected']))
          {
            $(this.el).css('background-color', '#f2d8d8');
          }
          else if ('Executing command(s)' == this.model.get('currentstep'))
          {
            $(this.el).css('background-color', '#fedda7');
          }
          else
          {
            $(this.el).css('background-color', '#d8f2dc');
          }

          if (1 == this.model.get('status'))
          {
            this.$('.job-detail-actions')
              .append('<a class="btn_browse_job" href="#">Browse</a>')
              .append('<a class="btn_approve_job" href="#">Approve</a>')
              .append('<a class="btn_reject_job" href="#">Reject</a>')
          }

          this.$('.job-detail-microservice > a').tooltip();

          return this;
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

          alert("browsejob " + this.model.get('uuid'));
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

    });

    window.StatusView = Backbone.View.extend({

      id: 'status',

      template: _.template($('#status-template').html()),

      initialize: function()
        {
          this.render();
        },

      render: function()
        {
          $(this.el).html(this.template()).hide().appendTo('body');

          return this;
        },

      hide: function()
        {
          var self = this;
          setTimeout(function()
            {
              $(self.el).fadeOut('fast');
            }, 1000);
        },

      text: function(message, error)
        {
          $(this.el).show().find('span').html(message);

          if (true === error)
          {
            $(this.el).addClass('status-error');
          }
          else
          {
            $(this.el).removeClass('status-error');
          }
        }

    });

    window.AppView = Backbone.View.extend({
    
      el: $('#sip-container'),

      interval: window.pollingInterval ? window.pollingInterval * 1000: 5000,
      
      idle: false,

      initialize: function()
        {
          _.bindAll(this, 'add', 'remove');
          Sips.bind('add', this.add);
          Sips.bind('remove', this.remove);

          window.statusWidget = new window.StatusView();

          // this.manageIdle();

          this.poll(true);
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
          
          if (0 == position)
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

      poll: function(start)
        {
          this.firstPoll = undefined !== start;

          $.ajax({
            context: this,
            dataType: 'json',
            type: 'GET',
            url: '/sips/go/',
            beforeSend: function()
              {
                window.statusWidget.text(undefined !== start ? 'Loading...' : 'Refreshing...');
              },
            error: function()
              {
                window.statusWidget.text('Error trying to connect to database. Trying again...', true);
              },
            success: function(response)
              {
                var objects = response.objects;

                for (var i in objects)
                {
                  var sip = objects[i];
                  var item = Sips.find(function(item) { return item.get('uuid') == sip.uuid; });

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
                  window.statusWidget.hide();
                }
                else
                {
                  window.statusWidget.text('Error trying to connect to MCP server. Trying again...', true);
                }
              },
            complete: function()
              {
                var self = this;

                if (!self.idle)
                {
                  setTimeout(function()
                    {
                      self.poll();
                    }, this.interval);
                }
              }
          });
        },

    });

    $.fn.tooltip = function(options)
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

    Date.prototype.getArchivematicaDateTime = function()
      {
        pad = function (n)
          {
            return n < 10 ? '0' + n : n;
          }

        return this.getUTCFullYear() + '-' + pad(this.getUTCMonth() + 1) + '-' + pad(this.getUTCDate()) + ' ' + pad(this.getUTCHours()) + ':' + pad(this.getUTCMinutes()); // + ':' + pad(this.getUTCSeconds());
      };
  }
);