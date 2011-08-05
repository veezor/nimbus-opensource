
/* Copyright © 2010, 2011 Veezor Network Intelligence (Linconet Soluções em Informática Ltda.), <www.veezor.com>

 This file is part of Nimbus Opensource Backup.

    Nimbus Opensource Backup is free software: you can redistribute it and/or 
    modify it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License.

    Nimbus Opensource Backup is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Nimbus Opensource Backup.  If not, see <http://www.gnu.org/licenses/>.

In this file, along with the Nimbus Opensource Backup code, it may contain 
third part code and software. Please check the third part software list released 
with every Nimbus Opensource Backup copy.

You can find the correct copyright notices and license informations at 
their own website. If your software is being used and it's not listed 
here, or even if you have any doubt about licensing, please send 
us an e-mail to law@veezor.com, claiming to include your software. */

function set_toggles() {
    $('.toggle').click(
        function () {
            visible = false;
            if ($('#' + $(this).attr('rel') + ':visible').size()) {
                visible = true;
            }
            
            $('#' + $(this).attr('rel')).toggle('fast');
            if (visible) {
                $.cookie('#' + $(this).attr('rel'), null);
            } else {
                $.cookie('#' + $(this).attr('rel'), true);
            }
        }
    )
    
    $('.cookie_toggle').each(
        function() {
            if ($.cookie('#' + $(this).attr('id')) == 'true') {
                $(this).show();
            }
        }
    );
}

function set_backup_type() {
    if (!$('form select[name=type]')) {
        return false;
    }
    $('form select[name=type]').change(
        function() {
            backup_type = $(this).children().filter(':selected').val();
            change_backup_type(backup_type);
        }
    );
    $('form select[name=type]').change();
}

function change_backup_type(backup_type) {
    $('#id_schedule_type').val(backup_type);
    switch (backup_type.toLowerCase()) {
        case 'weekly':
            // Do something...
            //console.log('weekly');
            $('.mtriggform').hide('fast');
            $('.mtriggform').find('input, select').attr('disabled', true);
            $('.wtriggform').show('fast');
            $('.wtriggform').find('input, select').attr('disabled', false);
            $('.triggform_message').hide('fast');
            break;
        case 'monthly':
            // Do something more...
            //console.log('monthly');
            $('.mtriggform').show('fast');
            $('.mtriggform').find('input, select').attr('disabled', false);
            $('.wtriggform').hide('fast');
            $('.wtriggform').find('input, select').attr('disabled', true);
            $('.triggform_message').hide('fast');
            break;
        default:
            // Go away.
            //console.log('default');
            $('.mtriggform').hide('fast');
            $('.mtriggform').find('input, select').attr('disabled', true);
            $('.wtriggform').hide('fast');
            $('.wtriggform').find('input, select').attr('disabled', true);
            $('.triggform_message').show('fast');
    }
}



function set_schedule_procedure() {
    $('#execute_procedure #id_run_now').change(
        function() {
            change_schedule_procedure();
        }
    );
    $('#execute_procedure #id_run_now').click();
    $('#execute_procedure #id_run_now').change();
}

function change_schedule_procedure() {
    run_now = $('#execute_procedure #id_run_now').attr('checked');
    if (!run_now) {
        $('.runscheduledform').show('fast');
        $('#execute_procedure input[type=submit]').val('Agendar');
    } else {
        $('.runscheduledform').hide('fast');
        $('#execute_procedure input[type=submit]').val('Executar');
    }
}


$(document).ready(function() {
    // Execute function to start the application.
    set_toggles();
    set_backup_type();
    set_schedule_procedure();
    $('input:text').addClass("text");
    // asks: are you sure?
    // Não importa se voce clica em 'ok' ou 'cancel', a acao eh executada assim mesmo
    // $(".negative").click(function(){
    //     if (!confirm("Tem certeza?"))
    //         return false;
    // });
});

/* minibuttons */
jQuery.ready(function() {
  jQuery('a.minibutton').bind({
    mousedown: function() {
      jQuery(this).addClass('mousedown');
    },
    blur: function() {
      jQuery(this).removeClass('mousedown');
    },
    mouseup: function() {
      jQuery(this).removeClass('mousedown');
    }
  });
});