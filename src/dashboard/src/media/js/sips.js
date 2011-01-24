$(function()
  {

    window.Sip = Backbone.Model.extend({

      initialize: function()
        {
          this.jobs = new JobCollection(this.get('jobs'));
        }

    });

    window.SipCollection = Backbone.Collection.extend({

      model: Sip,
      
      url: '/sips/all/'
      
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

      toggleJobs: function()
        {
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
      
      template: _.template($('#job-template').html()),

      initialize: function()
        {
          _.bindAll(this, 'render');
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
            this.$('.job-detail-currentstep').append(' (MCP)');
          }

          return this;
        },

    });

    window.StatusView = Backbone.View.extend({

      id: 'status',

      template: _.template($('#status-template').html()),

      initialize: function()
        {

        },
      
      show: function()
        {
        },

      hide: function()
        {
        },

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

          var $current = this.el.find('.sip[uuid=' + sip.get('uuid') + ']');
          if ($current.length)
          {
            if ($current.hasClass('sip-selected'))
            {
              
            }
            else
            {
              $current.replaceWith(view.render().el);
            }
          }
          else
          {
            this.el.children('#sip-body').append(view.render().el);
          }
        },

      addAll: function()
        {
          Sips.each(this.addOne);

          setTimeout(function()
            {
              Sips.fetch();
            }, window.pollingInterval ? window.pollingInterval * 1000: 5000);
        }

    });

  }
);