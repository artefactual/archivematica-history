$(function()
  {

    window.Sip = Backbone.Model.extend({
    
      initialize: function()
        {
          this.jobs = new JobCollection(this.get('jobs'));
          this.bind('change:timestamp', function()
            {
              this.view.render();
            });
        },
    });

    window.SipCollection = Backbone.Collection.extend({

      model: Sip,
      
      url: '/sips/all/',

      sync: function()
        {
          Backbone.sync.apply(this, arguments);
        }

    });

    window.SipView = Backbone.View.extend({

      className: 'sip',

      template: _.template($('#sip-template').html()),

      events: {
        'click .sip-row > .sip-detail-jobs > a': 'toggleJobs',
      },

      initialize: function()
        {
          _.bindAll(this, 'render');
          this.model.view = this;
        },
      
      render: function()
        {
          $(this.el).html(this.template(this.model.toJSON())).attr('uuid', this.model.get('uuid'));

          if (this.model.jobs.hasAlert())
          {
            $(this.el).addClass('sip-highlight');
          }

          this.$('.sip-detail-icon').html($('<img />').attr('src', this.model.jobs.getIcon()));

          var self = this;

          this.model.jobs.each(function(job)
            {
              var view = new JobView({model: job});
              self.$('.sip-detail-job-container').append(view.render().el);
            });

          return this;
        },

      toggleJobs: function(event)
        {
          event.preventDefault();

          var $jobContainer = this.$('.sip-detail-job-container');

          if ($jobContainer.is(':visible'))
          {
            $jobContainer.slideUp('fast');
            $(this.el).removeClass('sip-selected');
            this.$('.sip-detail-jobs > a').text('Show jobs');
          }
          else
          {
            $jobContainer.slideDown('fast');
            $(this.el).addClass('sip-selected');
            this.$('.sip-detail-jobs > a').text('Hide jobs');
          }
        }
    });

    window.Job = Backbone.Model.extend({

    });
    
    window.JobCollection = Backbone.Collection.extend({
    
      model: Job,

      hasAlert: function()
        {
          return undefined !== this.find(function(job)
            {
              return 0 < job.get('status') || -1 < jQuery.inArray(job.get('currentstep'), ['Requires approval', 'Failed']);
            });
        },

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
          else
          {
            return '/media/images/accept.png';
          }
        },
    
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
          _.bindAll(this, 'render');
          this.model.bind('change', this.render);
          this.model.view = this;
        },

      render: function()
        {
          $(this.el).html(this.template(this.model.toJSON()));

          if (-1 < jQuery.inArray(this.model.get('currentstep'), ['Requires approval', 'Failed']))
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
              .append(' (!)')
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
          _.bindAll(this, 'addOne', 'addAll');
          Sips.bind('refresh', this.addAll);
          Sips.fetch();
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
                  item.set(sip);
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

        return this.getUTCFullYear() + '-' + pad(this.getUTCMonth() + 1) + '-' + pad(this.getUTCDate()) + ' ' + pad(this.getUTCHours()) + ':' + pad(this.getUTCMinutes()) + ':' + pad(this.getUTCSeconds());
      };
  }
);