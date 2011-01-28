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
      
      url: '/sips/all/',

      initialize: function()
        {

        },

      comparator: function(sip)
        {
          return 0 - sip.get('timestamp');
        },

    });

    window.SipView = Backbone.View.extend({

      className: 'sip',

      template: _.template($('#sip-template').html()),

      events: {
        'click .sip-row > .sip-detail-jobs > a': 'toggleJobs',
      },

      initialize: function()
        {
          _.bindAll(this, 'render', 'update', 'add', 'updateIcon');
          this.model.view = this;
          this.model.bind('change:timestamp', this.update);
        },
      
      render: function()
        {
          $(this.el).html(this.template(this.model.toJSON())).attr('uuid', this.model.get('uuid'));

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
          this.$('.sip-detail-icon').html('<img src="' + this.model.jobs.getIcon() + '" />');
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
            this.$('.sip-detail-jobs > a').text('Show micro-services');
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
            this.$('.sip-detail-jobs > a').text('Hide micro-services');
          }
        }
    });

    window.Job = Backbone.Model.extend({

    });
    
    window.JobCollection = Backbone.Collection.extend({
    
      model: Job,

      getIcon: function()
        {
          if (undefined !== this.find(function(job)
            {
              return 0 < job.get('status') || 'Requires approval' == job.get('currentstep');
            }))
          {
            return '/media/images/bell.png';
          }
          else if (undefined !== this.find(function(job)
            {
              return 'Failed' == job.get('currentstep');
            }))
          {
            return '/media/images/cancel.png';
          }
          else if (undefined !== this.find(function(job)
            {
              return 'Executing command(s)' == job.get('currentstep');
            }))
          {
            return '/media/images/icons/arrow_refresh.png';
          }
          else if (undefined !== this.find(function(job)
            {
              return 'Rejected' == job.get('currentstep');
            }))
          {
            return '/media/images/icons/control_stop_blue.png';
          }
          else
          {
            return '/media/images/accept.png';
          }
        }
    
    });

    window.JobView = Backbone.View.extend({
    
      className: 'job',

      events: {
        'click .btn_browse_job': 'browseJob',
        'click .btn_approve_job': 'approveJob',
        'click .btn_reject_job': 'rejectJob'
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

          if (-1 < jQuery.inArray(this.model.get('currentstep'), ['Requires approval', 'Failed', 'Rejected', 'Executing command(s)']))
          {
            $(this.el).css('background-color', '#f2d8d8');
          }
          else
          {
            $(this.el).css('background-color', '#d8f2dc');
          }

          if (1 == this.model.get('status'))
          {
            this.$('.job-detail-currentstep')
              .append('<div></div>').children()
              .append('<a class="btn_browse_job" href="#">Browse</a>')
              .append('<a class="btn_approve_job" href="#">Approve</a>')
              .append('<a class="btn_reject_job" href="#">Reject</a>')
          }

          return this;
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

                this.model.sip.view.toggleJobs();
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

        },
      
      show: function(message, error)
        {
          this.text(message);

          if (true === error)
          {
            $(this.el).addClass('status-error');
          }
          else
          {
            $(this.el).removeClass('status-error');
          }

          $(this.el).show();
        },

      hide: function()
        {
          $(this.el).hide();
        },

      text: function(message)
        {
          $(this.el).find('span').html(message);
        }

    });

    window.AppView = Backbone.View.extend({
    
      el: $('#sip-container'),

      initialize: function()
        {
          _.bindAll(this, 'addOne', 'addAll', 'add');
          Sips.bind('refresh', this.addAll);
          Sips.bind('add', this.add);
          Sips.fetch();
        },

      add: function(sip)
        {
          var index = Sips.indexOf(sip);
          var view = new SipView({model: sip});

          var $new = $(view.render().el).hide();
          var $target = this.el.find('.sip').eq(index);

          if ($target.length)
          {
            $target.before($new);
          }
          else
          {
            this.el.children('#sip-body').append($new);
          }

          // Animation
          $new.addClass('sip-new').show('blind', {}, 500, function()
            {
              $(this).removeClass('sip-new', 2000);
            });
        },
      
      addOne: function(sip)
        {
          var view = new SipView({model: sip});
          this.el.children('#sip-body').append(view.render().el);
        },

      addAll: function()
        {
          Sips.each(this.addOne);

          var self = this;
          setTimeout(function()
            {
              self.poll();
            }, window.pollingInterval ? window.pollingInterval * 1000: 5000);
        },

      poll: function()
        {
          $.ajax({
            context: this,
            dataType: 'json',
            type: 'GET',
            url: '/sips/all/',
            error: function()
              {
                // Show warning
              },
            success: function(response)
              {
                for (var i in response)
                {
                  var sip = response[i];
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

                  // Delete sips
                }
              },
            complete: function()
              {
                var self = this;
                setTimeout(function()
                  {
                    self.poll();
                  }, window.pollingInterval ? window.pollingInterval * 1000: 5000);
              }
          });
        },

    });

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