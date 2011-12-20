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

$(document).ready(function() {
  // active formset changer
  $('#id_rightsbasis').change(revealSelectedBasis);
  revealSelectedBasis();

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
  })
});
