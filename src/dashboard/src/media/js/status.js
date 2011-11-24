/*
this file is part of archivematica.

copyright 2010-2011 artefactual systems inc. <http://artefactual.com>

archivematica is free software: you can redistribute it and/or modify
it under the terms of the gnu general public license as published by
the free software foundation, either version 2 of the license, or
(at your option) any later version.

archivematica is distributed in the hope that it will be useful,
but without any warranty; without even the implied warranty of
merchantability or fitness for a particular purpose.  see the
gnu general public license for more details.

you should have received a copy of the gnu general public license
along with archivematica.  if not, see <http://www.gnu.org/licenses/>.
*/

$(function()
  {
    window.PendingJobsView = Backbone.View.extend({

      el: 'body',

      initialize: function()
        {
          this.poll();

          this.transfer = this.$('ul.nav > li').eq(1);
          this.sip = this.$('ul.nav > li').eq(2);
          // this.dip = this.$('ul.nav > li').eq(5);
        },

      render: function()
        {
        },

      update: function(node, value)
        {
          led = node.find('span');

          if (!value)
          {
            led.remove();

            return false;
          }

          if (!led.length)
          {
            led = node.append('<span />').children('span');
          }

          led.text(value);
        },

      poll: function()
        {
          var self = this;

          $.ajax({
            context: this,
            dataType: 'json',
            type: 'GET',
            url: '/status/',
            beforeSend: function()
              {

              },
            error: function()
              {

              },
            success: function(response)
              {
                this.update(this.transfer, response.transfer);
                this.update(this.sip, response.sip);
                this.update(this.dip, response.dip);
              },
            complete: function()
              {
                var self = this;

                setTimeout(function()
                  {
                    self.poll();
                  }, 5000);

              }
          });
        }
    });

  window.PendingJobs = new window.PendingJobsView;

  }
)
