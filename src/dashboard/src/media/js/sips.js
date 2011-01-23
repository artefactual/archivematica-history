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

          if (this.model.get('status'))
          {
            $(this.el).addClass('sip-highlight');
          }

          var self = this;

          this.$('.sip-detail-icon').html(function()
            {
              var $img = $('<img />');
              switch (self.model.get('status'))
              {
                case 0:
                  $img.attr('src', '/media/images/accept.png');
                  break;

                case 1:
                  $img.attr('src', '/media/images/bell.png');
                  break;
              }

              return $img;
            });

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

          return this;
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