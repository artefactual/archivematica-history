// repeating child field to a bound formset instance
function setUpRepeatingField(instanceId, idPrefix, parentId) {

  // if the form instance isn't blank, it's bound to data
  var formInstance = instanceId;

  if (formInstance != '') {
    formInstance = parseInt(formInstance);

    if (typeof rightsNotes == 'undefined') {
      rightsNotes = [];
    }

    var rights = new RepeatingRecordView({
      el: $('#rightsfields_' + formInstance),
      description: 'Rights Note',
      parentId: parentId
    });
    rightsNotes.push(rights);
    rights.render();
  }
}

// logic to show appropriate subform
function revealSelectedBasis() {
  var basis = $('#id_rightsbasis').val()
    , formsets = {
      'Copyright': 'copyright_formset',
      'Statute':   'statute_formset',
      'License':   'license_formset',
      'Policy':    false,
      'Donor':     false
  }

  // hide all formsets except basis
  for (var key in formsets) {
    if (key != basis && formsets[key]) {
      $('#' + formsets[key]).hide();
    }
  }

  // if basis has a formset, show it
  if (formsets[basis]) {
    $('#' + formsets[basis]).show();
  }
}

// setup
$(document).ready(function() {

  $.extend($.inputmask.defaults.definitions, {
    'y': {
      'validator': '[012]\\d\\d\\d',
      'cardinality': 4,
      'prevalidator': [
        { 'validator': '[012]', 'cardinality': 1 }
      ]
    }
  });

  $('input[name*="date"]').inputmask('y/m/d');

  // active formset changer
  $('#id_rightsbasis').change(revealSelectedBasis);
  revealSelectedBasis();

  if ($('#id_rightsholder').length > 0) {
    // lookup rightsholder
    $.get('lookup/rightsholder/' + $('#id_rightsholder').val(), function(data) {
      $('#id_rightsholder').val(data);
    });

    // attach autocomplete
    $("#id_rightsholder").autocomplete({  

      // define callback to format results  
      source: function(req, add){  
 
        // pass request to server  
        $.getJSON("autocomplete/rightsholders", {'text': req.term}, function(data) {  
 
          // create array for response objects  
          var suggestions = [];  
  
          // process response  
          $.each(data, function(i, val){  
            suggestions.push(val);  
          });  

          // pass array to callback  
          add(suggestions);  
        });
      }
    });
  }
});
