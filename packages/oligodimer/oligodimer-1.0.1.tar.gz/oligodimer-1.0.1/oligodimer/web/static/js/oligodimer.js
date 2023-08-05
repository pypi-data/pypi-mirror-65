function tooltip_init() {
    // Tooltip for bootstrap
    $('[data-toggle="tooltip"]').tooltip({html: true});
    $('[data-toggle="popover"]').popover({html: true});
}

function highlight_changed_field(originalValFor) {
    var inputs = $(':text.save-input');
    for (var i=0; i<inputs.length; i++) {
        var el = inputs[i];
        if (el.value!=originalValFor[el.name]) {
            $(el).css('background-color', '#ffffbf');
        }
        else {
            $(el).css('background-color', 'white');
        }
    }
}

function generate_dimer_result(data){
    $('#dimers-result').addClass('hidden')
    $('#dimers-result tbody').html('');
    $('#dimers-result').next('.alert-danger,.alert-success').remove();
    if ('error' in data) {
        $('#dimers-result').after($('#result-template-error').html());
        $('#dimers-result').next('.alert-danger').append('<p>ERROR: '+data['error']+'</p>');
        return
    }
    if (jQuery.isEmptyObject(data['dimers'])==true) {
        $('#dimers-result').after($('#result-template-error').html());
        $('#dimers-result').next('.alert-danger').append('<p>No dimers detected.</p>').removeClass('alert-danger').addClass('alert-success');
        return
    }
    for (i in data['dimers']) {
        dimer = data['dimers'][i];
        $('#dimers-result tbody').append('<tr>'
        +'<td>'+dimer[0]['id']+'</td>'
        +'<td><span class="monospace-style">'+dimer[0]['seq']+'</span></td>'
        +'<td>'+dimer[1]['id']+'</td>'
        +'<td><span class="monospace-style">'+dimer[1]['seq']+'</span></td>'
        +'<td>'+dimer[2]+'</td>'
        +'<td><pre>'+dimer[3]+'</pre></td>'
        +'</tr>');
        $('#dimers-result').removeClass('hidden')
    }
}

// ***********************  Begin main functions  ***********************  
// ********* Page load *********
var db_name_change = new Object;
var config_data = new Object;
var originalValFor = new Object;
$(function () {
    var inputs = $(':text.save-input');
    for (var i=0; i<inputs.length; i++) {
        var el = inputs[i];
        originalValFor[el.name] = el.defaultValue;
    }
    // load last save
    $('.save-input').phoenix();
    highlight_changed_field(originalValFor);
    tooltip_init();
});

// ********* Highlight differences when user changes *****************************************
$('input').blur(function(){
    highlight_changed_field(originalValFor);
})


// ********* The reset buttton *******************************************************
$(':reset').click(function(){
    highlight_changed_field(originalValFor);
});

// ********* User submit the form *******************************************************
$('#form-dimer').validationEngine('attach', {
    onValidationComplete: function(form, status) {
        if (status) {
            $('#running-indicator').removeClass('hidden');
            var currentAjax = $.post($SCRIPT_ROOT + '/run', $('#form-dimer').serialize(), function(data){
                $('#running-indicator').addClass('hidden');
                generate_dimer_result(JSON.parse(data));
            });
        }
    }
});

