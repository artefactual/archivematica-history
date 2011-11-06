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
    window.StatusView = Backbone.View.extend({

      el: '#connection-status',

      template: _.template($('#status-template').html()),

      initialize: function()
        {
          this.render();
        },

      render: function()
        {
          $(this.el).html(this.template());

          var self = this;

          this.$led = $(this.el).find('img');
          this.$text = $(this.el).find('#status-message').hide();

          return this;
        },

      connect: function()
        {
          log('Connected.');
          this.$led.attr({'src': '/media/images/bullet_green.png', 'title': 'Connected'});
          this.cleanText();
        },

      startPoll: function()
        {
          log('Start poll.');
          this.$led.attr({'src': '/media/images/bullet_orange.png', 'title': 'Loading'});
        },

      endPoll: function()
        {
          log('End poll.');
        },

      hide: function()
        {
          var self = this;
          setTimeout(function()
            {
              $(self.el).children('status-message').fadeOut('fast');
            }, 1000);
        },

      cleanText: function()
        {
          this.$text.hide('fast');
        },

      text: function(message, error)
        {
          log("Status message: " + message + " (isError: " + error + ")");
          this.$text.show().find('span').html(message);

          if (true === error)
          {
            this.$led.attr({'src': '/media/images/bullet_delete.png', 'title': 'Disconnected'});
            this.$text.addClass('status-error');
          }
          else
          {
            this.$text.removeClass('status-error');
          }
        }

    });

  }
)
