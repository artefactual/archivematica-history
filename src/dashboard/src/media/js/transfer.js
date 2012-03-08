/*
This file is part of Archivematica.

Copyright 2010-2012 Artefactual Systems Inc. <http://artefactual.com>

Archivematica is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Archivematica is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Archivematica.  If not, see <http://www.gnu.org/licenses/>.
*/

$(function()
  {

    window.Sip = Backbone.Model.extend({

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

    window.SipCollection = Backbone.Collection.extend({

      model: Sip,

      url: '/transfer/status/',

      initialize: function()
        {

        },

      comparator: function(sip)
        {
          return -1 * sip.get('timestamp');
        }

    });

    window.SipView = Backbone.View.extend({

      className: 'sip',

      template: _.template($('#sip-template').html()),

      events: {
        'click .sip-row': 'openPanel',
        'click .sip-row > .sip-detail-actions > .btn_show_panel': 'openPanel',
        'click .sip-row > .sip-detail-actions > .btn_show_jobs': 'toggleJobs',
        'click .sip-row > .sip-detail-actions > .btn_remove_sip': 'remove'
      },

      initialize: function()
        {
          _.bindAll(this, 'render', 'update', 'updateIcon');
          this.model.view = this;
          this.model.bind('change:timestamp', this.update);
        },

      render: function()
        {
          $(this.el).html(this.template(this.model.toJSON()));

          this.$jobContainer = this.$('.sip-detail-job-container');

          this.$('.sip-detail-actions > a').twipsy();

          return this;
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
          this.$('.sip-detail-icon-status').html(this.model.jobs.getIcon());
        },

      openPanel: function(event)
        {
          event.preventDefault();

          window.location = '/transfer/' + this.model.get('uuid') + '/';
        },

      toggleJobs: function(event)
        {
          event.preventDefault();
          event.stopPropagation();

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
          event.stopPropagation();

          $(this.el).addClass('sip-removing');

          var self = this;

          $('<div>' +
              '<p><strong>Are you sure you want to remove this transfer from the dashboard? Note that this does not delete the transfer or related entities.</strong></p>' +
              '<p>Directory: ' + this.model.get('directory') + '<br />UUID: ' + this.model.get('uuid') + '<br />Status: ' + $(this.el).find('.sip-detail-icon-status > img').attr('title') + '</p>' +
            '</div>').dialog(
            {
              modal: true,
              resizable: false,
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
              return job.get('microservice') === 'Assign file UUIDs and checksums';
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
              return 0 < job.get('status') || 'Requires approval' === job.get('currentstep');
            }))
          {
            path = '/media/images/bell.png';
            title = 'Requires approval';
          }
          else if (undefined !== this.find(function(job)
            {
              return 0 < job.get('status') || 'Awaiting decision' === job.get('currentstep');
            }))
          {
            path = '/media/images/bell.png';
            title = 'Awaiting decision';
          }
          else if (undefined !== this.find(function(job)
            {
              return 'Failed' === job.get('currentstep');
            }))
          {
            path = '/media/images/cancel.png';
            title = 'Failed';
          }
          else if (undefined !== this.find(function(job)
            {
              return 'Executing command(s)' === job.get('currentstep');
            }))
          {
            path = '/media/images/arrow_refresh.png';
            title = 'Executing command(s)';
          }
          else if (undefined !== this.find(function(job)
            {
              return 'Rejected' === job.get('currentstep');
            }))
          {
            path = '/media/images/control_stop_blue.png';
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
          return -1 * job.get('timestamp');
        }

    });

    window.JobView = BaseJobView.extend({

      className: 'job',

      events: {
        'click .btn_browse_job': 'browseJob',
        'click .btn_approve_job': 'approveJob',
        'click .btn_reject_job': 'rejectJob',
        'click .btn_show_tasks': 'showTasks',
        'change select': 'action'
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

          $(this.el).css(
            'background-color', 
            this.getStatusColor(this.model.get('currentstep'))
          );

          // Micro-services requiring approval
          if (1 === this.model.get('status'))
          {
            this.$('.job-detail-actions')
              .append('<a class="btn_browse_job" href="#" title="Browse"><span>Browse</span></a>')
              .append('<a class="btn_approve_job" href="#" title="Approve"><span>Approve</span></a>')
              .append('<a class="btn_reject_job" href="#" title="Reject"><span>Reject</span></a>');
          }
          else
          {
            // ...
          }

          choices = this.model.get('choices');

          if (choices)
          {
            var $select = $('<select />').append('<option>Actions</option>');

            for (var code in choices)
            {
              $select.append('<option value="' + code + '">- ' + choices[code] + '</option>');
            }

            this.$('.job-detail-actions').append($select);
          }

          this.$('.job-detail-microservice > a').tooltip();

          this.$('.job-detail-actions > a').twipsy();

          return this;
        },

      action: function(event)
        {
          var value = $(event.target).val();

          $.ajax({
            context: this,
            data: { uuid: this.model.get('uuid'), choice: value },
            type: 'POST',
            success: function(data)
              {
                this.model.set({
                  'currentstep': 'Executing command(s)',
                  'status': 0
                });

                this.model.sip.view.updateIcon();
              },
            url: '/mcp/execute/'
          });
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
        }

    });

    window.DirectoryBrowserView = Backbone.View.extend({

      id: 'directory-browser',

      template: _.template($('#directory-browser-template').html()),

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

      poll: function(start)
        {
          this.firstPoll = undefined !== start;

          $.ajax({
            context: this,
            dataType: 'json',
            type: 'GET',
            url: '/transfer/status/',
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

    Date.prototype.getArchivematicaDateTime = function()
      {
        pad = function (n)
          {
            return n < 10 ? '0' + n : n;
          }

        return this.getFullYear() + '-' + pad(this.getMonth() + 1) + '-' + pad(this.getDate()) + ' ' + pad(this.getHours()) + ':' + pad(this.getMinutes()); // + ':' + pad(this.getSeconds());
      };

    window.log = function(message)
      {
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
      };

    optimizeWidth = function()
      {
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

    window.onresize = optimizeWidth;
    window.onload = optimizeWidth;

  }
);
