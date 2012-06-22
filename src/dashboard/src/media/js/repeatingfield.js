var RepeatingFieldItemView = Backbone.View.extend({
  initialize: function(id, value) {
    this.id    = id;
    this.value = value;
  },

  render: function() {
    var $input = $('<input/>');
    $input.val(this.value);
    this.el = $('<div></div>');
    this.el.append($input);

    return this;
  }
});

var RepeatingFieldView = Backbone.View.extend({

  initialize: function() {
    this.items = [];

    if (this.options.description) {
      this.description = this.options.description;
    }

    if (this.options.parentId) {
      this.parentId = this.options.parentId;
    }

    this.url = '/formdata/rightsnote/' + this.parentId + '/';
    this.waitingForInput = false;
  },

  newLinkEl: function() {
    var $linkEl = $('<div class="btn">New ' + this.description + '</div>')
      , self = this;

    $linkEl.click(function() {
      if (!self.waitingForInput) {
      self.waitingForInput = true;
      var $input = $('<input/>')
        , $div = $('<div/>');
      $div.append($input);
      $(self.el).append($div);
      $input.on('change', function() {
        var value = $input.val();
        $.ajax({
          url: self.url,
          type: 'POST',
          data: {'value': value},
          success: function(result) {
            self.waitingForInput = false;
            alert('Added.');
            self.render();
          }
        });
      });

      }
    });

    return $linkEl;
  },

  render: function() {
    var self = this;
    $.ajax({
      url: self.url,
      type: 'GET',
      success: function(result) {
        $(self.el)
          .empty()
          .append(self.newLinkEl());
        for(var index in result.results) {
          var fieldData = result.results[index]
            , field = new RepeatingFieldItemView(fieldData.id, fieldData.value);

          $(self.el).append(field.render().el);
        }
      }
    });
    return this;
  }
});
