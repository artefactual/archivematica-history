// Dashboard namespace
var Dashboard = {};
  // Dashboard.IntervalManager
  // Dashboard.SipManager
  
Dashboard.SipManager = function()
  {
    this.$container = $('#content');
    this.sips = [];

    this.isActive = false;
    this.interval = 5000;
    if (1 == arguments.length)
    {
      this.interval = arguments[0] * 1000;
    }

    this.loadingWidget = {
      widget: $('<div id="loading"><div><div><span>Loading...</span></div></div></div>').hide().appendTo(document.body),
      show: function()
        {
          this.widget.show();
        },
      hide: function()
        {
          this.widget.fadeOut(500);
        }
    };
  };

Dashboard.SipManager.prototype.get = function()
  { 
    $.ajax({
      beforeSend: function()
        {
          this.loadingWidget.show();
        },
      context: this,
      dataType: 'json',
      success: function(data)
        {
          this.sips = [];

          for (var i in data)
          {
            // Add Sips
            this.add(data[i]);
          }

          this.render();
          this.loadingWidget.hide();
          this.step();
        },
      type: 'GET',
      url: '/sips/all/',
    });
  };

Dashboard.SipManager.prototype.add = function(sip)
  {
    this.sips.push(new Dashboard.Sip(sip));
  };

Dashboard.SipManager.prototype.render = function()
  {
    var $sipsContainer = $('<div id="sips-container" />').append(
      '<div id="sips-header">' +
      '<div id="sips-header-icon">&nbsp;</div>' +
      '<div id="sips-header-directory">Directory</div>' +
      '<div id="sips-header-uuid">UUID</div>' +
      '<div id="sips-header-timestamp">Timestamp</div>' +
      '</div>');

    for (var i in this.sips)
    {
      $sipsContainer.append(this.sips[i].toHtml());
    }

    if ($('#sips-container').length)
    {
      $('#sips-container').remove();
    }

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
      this.get();
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
        self.get();
      }, this.interval);
  };

Dashboard.Sip = function()
  {
    if (1 == arguments.length)
    {
      this.directory = arguments[0].directory;
      this.uuid = arguments[0].uuid;
      this.timestamp = arguments[0].timestamp;
    }
  };

Dashboard.Sip.prototype.toHtml = function()
  {
    return '<div class="sip" uuid="' + this.uuid + '">' +
           '<div class="sip-detail-icon">&nbsp;</div>' +
           '<div class="sip-detail-directory">' + this.directory + '</div>' +
           '<div class="sip-detail-uuid">' + this.uuid + '</div>' +
           '<div class="sip-detail-timestamp">' + this.timestamp + '</div>'
           '</div>';
  };