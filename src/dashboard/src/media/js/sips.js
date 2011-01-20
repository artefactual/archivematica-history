// Dashboard namespace
var Dashboard = {};
  // Dashboard.IntervalManager
  // Dashboard.SipManager
 
Dashboard.pollingInterval = 5; // Seconds

Dashboard.SipManager = function()
  {
    this.$container = $('#content');
    this.sips = [];

    this.isActive = false;
    this.interval = Dashboard.pollingInterval * 1000;

    this.statusWidget = {
      widget: $('<div id="status"><div><div><span>&nbsp;</span></div></div></div>').hide().appendTo(document.body),
      show: function(message, error)
        {
          this.text(message);

          if (true === error)
          {
            this.widget.addClass('status-error');
          }
          else
          {
            this.widget.removeClass('status-error');
          }

          this.widget.show();
        },
      hide: function()
        {
          this.widget.fadeOut(500);
        },
      text: function(message)
        {
          this.widget.find('span').html(message);
        }
    };

    var self = this;
    this.$container
      .delegate('.sip', 'click', function(event)
        {
          var sip = self.get(this.getAttribute('uuid'));
        })
      .delegate('.sip', 'hover', function(event)
        {
          if ('mouseenter' == event.type)
          {
            $(this).addClass('sip-hover');
          }
          else if ('mouseleave' == event.type)
          {
            $(this).removeClass('sip-hover');
          }
        });
  };

Dashboard.SipManager.prototype.get = function(uuid)
  {
    for (var i in this.sips)
    {
      if (uuid == this.sips[i].uuid)
      {
        return this.sips[i];
      }
    }
  };

Dashboard.SipManager.prototype.load = function()
  { 
    $.ajax({
      beforeSend: function()
        {
          this.statusWidget.show('Loading...');
        },
      context: this,
      dataType: 'json',
      error: function()
        {
          var self = this;
          var counter = 0;
          var timerID = setInterval(function()
            {
              var icounter = 5 - counter;

              if (icounter == 0)
              {
                clearInterval(timerID);
                self.start();

                return true;
              }

              self.statusWidget.show('Error connecting to server... trying again in ' + icounter + 's.', true);
              counter++;
            }, 1000);
        },
      success: function(data)
        {
          for (var i in data)
          {
            // Add Sips
            this.add(data[i]);
          }

          this.statusWidget.hide();
          this.step();
        },
      type: 'GET',
      url: '/sips/all/',
    });
  };

Dashboard.SipManager.prototype.add = function(sip)
  {
    var existingSip = this.find(sip.uuid);

    if (false === existingSip)
    {
      var newSip = new Dashboard.Sip(sip);
      this.sips.push(newSip);
      newSip.render();
    }
    else
    {
      existingSip.replace(sip);
    }
  };

Dashboard.SipManager.prototype.find = function(uuid)
  {
    for (var i in this.sips)
    {
      if (this.sips[i].uuid == uuid)
      {
        return this.sips[i];
      }
    }

    return false;
  };

Dashboard.SipManager.prototype.render = function()
  {
    var $sipsContainer = $('<div id="sips-container" />').append(
      '<div id="sips-header">' +
      '<div id="sips-header-icon">&nbsp;</div>' +
      '<div id="sips-header-directory">Directory</div>' +
      '<div id="sips-header-uuid">UUID</div>' +
      '<div id="sips-header-timestamp">Timestamp</div>' +
      '<div id="sips-header-jobs">&nbsp;</div>' +
      '</div>');

    $sipsContainer.appendTo(this.$container);
  };

Dashboard.SipManager.prototype.start = function()
  {
    this.setActive(true);
  };

Dashboard.SipManager.prototype.stop = function()
  {
    this.setActive(false);
  };

Dashboard.SipManager.prototype.toggle = function()
  {
    if (this.isActive === false)
    {
      this.start();
    }
    else
    {
      this.stop();
    }
  };

Dashboard.SipManager.prototype.setActive = function(active)
  {
    if (active === true)
    {
      this.isActive = true;
      this.render();
      this.load();
    }
    else if (active === false)
    {
      this.isActive = false;
    }
  };

Dashboard.SipManager.prototype.step = function()
  {
    if (this.isActive === false)
    {
      return false;
    }

    var self = this;
    setTimeout(function()
      {
        self.load();
      }, this.interval);
  };

Dashboard.Sip = function()
  {
    if (1 != arguments.length)
    {
      return false;
    }

    this.$container = $('#sips-container');

    this.load(arguments[0]);
    this.build();
  };

Dashboard.Sip.prototype.load = function(sip)
{
  this.directory = sip.directory;
  this.uuid = sip.uuid;
  this.timestamp = sip.timestamp;
  this.status = sip.status;
}

Dashboard.Sip.prototype.getIcon = function(status)
  {
    switch (status)
    {
      case 0:
        return '/media/images/accept.png';
      case 1:
        return '/media/images/bell.png';
    }
  };

Dashboard.Sip.prototype.build = function()
  {
    this.$object = $('<div class="sip" />').attr({'uuid': this.uuid, 'status': this.status});
    
    if (this.status)
    {
      this.$object.addClass('sip-highlighted');
    }

    this.$object.append('<div class="sip-detail sip-detail-icon"><img src="' + this.getIcon(this.status) + '" /></div>');
    this.$object.append('<div class="sip-detail sip-detail-directory">' + this.directory + '</div>');
    this.$object.append('<div class="sip-detail sip-detail-uuid">' + this.uuid + '</div>');
    this.$object.append('<div class="sip-detail sip-detail-timestamp">' + this.timestamp + '</div>');
    this.$object.append('<div class="sip-detail sip-detail-jobs"><span>Show jobs</span></div>');
  };

Dashboard.Sip.prototype.render = function()
  {
    this.$container.append(this.$object);
  };

Dashboard.Sip.prototype.replace = function(sip)
  {
    if (this.timestamp != sip.timestamp)
    {
      this.load(sip);
      this.build();

      $('div.sip[uuid=' + this.uuid + ']', this.$container).replaceWith(this.$object);

      this.$object.addClass('sip-reloaded');
      var self = this;
      setTimeout(function()
        {
          self.$object.removeClass('sip-reloaded');
        }, 500);
    }
  };