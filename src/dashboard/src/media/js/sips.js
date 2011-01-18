// Dashboard namespace
var Dashboard = {};
  // Dashboard.IntervalManager
  // Dashboard.SipManager

Dashboard.IntervalManager = function()
  {
    this.init();
  }
  
Dashboard.IntervalManager.prototype.init = function()
  {
    this._timeout = 60;
    this._min = 1;
    this._step = 0.25;
    this._duration = 0;
    this._count = 0;

    this._interval = this._min;
  };

Dashboard.IntervalManager.prototype.reset = function()
  {
    this._interval = this._min;
    this._duration = 0;
    this._count = 0;

    return this.get();
  };

Dashboard.IntervalManager.prototype.add = function(amt)
  {
    this._interval += amt;
    this._duration += this._interval;    
    this._count++;  
  };

Dashboard.IntervalManager.prototype.step = function()
  {
    if (this._duration >= this._timeout)
    {
      // Timer has reached the _timeout limit
      return false;
    }

    var increment = Math.round(this._step * (this._count/20));

    this.add(increment);
    return this.get();
  };

Dashboard.IntervalManager.prototype.get = function()
  {
    return this._interval * 1000;
  };

Dashboard.SipManager = function()
  {
    this.init();
  }

Dashboard.SipManager.prototype.init = function()
  {
    this.interval = 0;
    this.defaultInterval = 5000; // Default interval if IntervalManager is not present
    this.$container = $('#content');
    this.$button = $('#button');
    this.sips = [];

    // Inititalize IntervalManager if present
    if (Dashboard.IntervalManager)
    {
      this.intervalManager = new Dashboard.IntervalManager();
    }

    // State and timer properties
    this.isActive = false;
    this.interval = false;
  };

Dashboard.SipManager.prototype.get = function(system)
  {
    $.ajax({
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

          this.timerStep(system);
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
    var $sipsContainer = $('<div id=\"sips-container\" />').append();

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
    this.timerStart();
  };

Dashboard.SipManager.prototype.stop = function()
  {
    if (this.timerStop() === true)
    {
      this.setActive(false);
    }
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

Dashboard.SipManager.prototype.timerStart = function()
  {
    if (this.isActive === false)
    {
      return false;
    }

    if (this.intervalManager)
    {
      var interval = this.intervalManager.reset();
      this.timerSet(interval);
      return true;
    }
    else
    {
      this.timerSet(this.defaultInterval);
    }

    return false;
  };

Dashboard.SipManager.prototype.timerStop = function()
  {
    if (this.isActive === false)
    {
      return true;
    }

    if (this.intervalManager)
    {
      clearInterval(this.timerID);
      this.interval = false;
    }

    return true;
  };

Dashboard.SipManager.prototype.timerSet = function(interval)
  {
    if (this.isActive === false)
    {
      return false;
    }

    var self = this;
    this.interval = interval;
    clearInterval(this.timerID);

    this.timerID = setInterval(function()
      {
        self.get(true);
      }, interval);

    return true;
  };

Dashboard.SipManager.prototype.timerReset = function()
  {
    if (this.isActive === false)
    {
      return false;
    }

    if (this.intervalManager)
    {
      var interval = this.intervalManager.reset();
      return this.timerSet(interval);
    }

    this.timerStart();
    return false;
  };

Dashboard.SipManager.prototype.timerStep = function(system)
  {
    if (this.isActive === false)
    {
      if (system !== true)
      {
        return this.start();
      }

      return false;
    }

    if (this.intervalManager)
    {
      var interval = this.intervalManager.step();
      if (interval !== false)
      {
        return this.timerSet(interval);
      }

      return this.stop();
    }

    return false;
  };

Dashboard.SipManager.prototype.setActive = function(active)
  {
    if (active === true)
    {
      this.isActive = true;
      this.$button.val('Stop');

      this.get();
    }
    else if (active === false)
    {
      this.isActive = false;
      this.$button.val('Start');

      clearInterval(this.timerID);
    }
  };

Dashboard.SipManager.prototype.statusDisplay = function()
  {
    var self = this;

    this.$button.click(function()
      {
        if (self.isActive === true)
        {
          self.stop();
        }
        else
        {
          self.start();
        }
      });
  };

Dashboard.Sip = function()
  {
    if (1 == arguments.length)
    {
      this.uuid = arguments[0].sipuuid;
      this.timestamp = arguments[0].latest;
    }
  };

Dashboard.Sip.prototype.toHtml = function()
  {
    return '<div class="sip" uuid="' + this.uuid + '">' +
           '<div style="position: relative;">' +
           '<div class="sip-detail-icon"></div>' +
           '<div class="sip-detail-uuid">' + this.uuid + '</div>' +
           '<div class="sip-detail-timestamp">' + this.timestamp + '</div>'
           '</div>' +
           '</div>';
  };




