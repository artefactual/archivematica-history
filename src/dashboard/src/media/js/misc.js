var NotificationView = Backbone.View.extend({
  initialize: function() {
    this.displayed = [];
  },

  add: function(attributes)
  {
    // logic to add notifications on client-side will go here
  },

  render: function() {
    // get currently stored notifications
    var localNotificationData = JSON.parse(localStorage.getItem('archivematicaNotifications'));

    if (localNotificationData != null)
    {
      // cycle through notifications
      for(var index in localNotificationData.notifications) {
        var notification = localNotificationData.notifications[index];

        // if notification hasn't been displayed on this page yet, display it
        if (this.displayed.indexOf(notification.id) == -1)
        {
          var $notificationDiv = $('<div class="alert-message"></div>');

          $notificationDiv
            .html(notification.message)
            .click(function() {
              // fade out notification
              $(this).fadeOut();

              // delete notification from localStorage

              // load notifications
              var localNotificationData = JSON.parse(localStorage.getItem('archivematicaNotifications'))
                , revisedNotifications = [];

              // remove the one that was clicked on
              for(var index in localNotificationData.notifications) {
                var compareNotification = localNotificationData.notifications[index];
                if (notification.id != compareNotification.id)
                {
                  revisedNotifications.push(compareNotification);
                }
              }

              // store revised notifications
              localNotificationData.notifications = revisedNotifications;
              localStorage.setItem('archivematicaNotifications', JSON.stringify(localNotificationData));
            });

          $(this.el).append($notificationDiv);

          // note that it has been displayed on the page
          this.displayed.push(notification.id);
        }
      }
    }

    // refresh notifications each second
    var self = this;
    setTimeout(function() {
      self.render();
    }, 1000);
  }
});

$(document).ready(
  function()
    {
      $('.preview-help-text')

        // Preview text
        .children('.preview')
          .show()
          .children('a')
            .click(function(event)
              {
                event.preventDefault();
                $(this).closest('.preview').hide();
                $(this).closest('.preview-help-text').children('.content').show();
              })
          .end()
        .end()

        // Content
        .children('.content')
          .hide()
          .append(' <a href="#">(collapse)</a>')
          .children('a')
            .click(function(event)
              {
                event.preventDefault();
                $(this).closest('.content').hide();
                $(this).closest('.preview-help-text').children('.preview').show();
              });
    });
