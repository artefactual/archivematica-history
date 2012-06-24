var RepeatingRecordRecordView = Backbone.View.extend({
  initialize: function(id, values) {
    this.id    = id;
    this.values = values;
  },

  getValues: function() {
    var values = {};
    $(this.el).children().each(function() {
      values[$(this).attr('name')] = $(this).val();
    });
    return values;
  },

  render: function() {
    this.el = $('<div></div>');

    for(field in this.values) {
      var $input = $('<textarea></textarea>');
      $input.attr('name', field);
      $input.val(this.values[field]);
      this.el.append($input);
    }

    return this;
  }
});

var RepeatingRecordView = Backbone.View.extend({

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
      $(this).attr('disabled', 'true');
      if (!self.waitingForInput) {
      self.waitingForInput = true;
      var field = new RepeatingRecordRecordView(
          0,
          {
            'rightsgrantednote': ''
          }
        )
        , fieldEl = field.render().el;

      var $input = $(fieldEl)
        , $div = $('<div/>');

      $div.append($input);
      $(self.el).append($div);
      $input.on('change', function() {
console.log(field.getValues());
        $.ajax({
          url: self.url,
          type: 'POST',
          data: field.getValues(),
          success: function(result) {
            $(self).attr('disabled', 'false');
            self.waitingForInput = false;
            self.render();
          }
        });
      });

      }
    });

    return $linkEl;
  },

  appendDelHandlerToRecord: function(fieldEl, id) {
    var $delHandle = $('<span>X</span>')
      , self = this;

    $(fieldEl).append($delHandle);

    $delHandle.click(function() {
      $.ajax({
        url: self.url + '/' + id,
        type: 'DELETE',
        data: {'id': id},
        success: function(result) {
          alert('Deleted.');
          self.render();
        }
      });
    });
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
            , field = new RepeatingRecordRecordView(
                fieldData.id,
                {
                  'rightsgrantednote': fieldData.value
                }
              )
            , fieldEl = field.render().el;

          self.appendDelHandlerToRecord(fieldEl, fieldData.id);

          $(self.el).append(fieldEl);
        }
      }
    });
    return this;
  }
});
