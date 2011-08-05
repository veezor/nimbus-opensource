
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

$(document).ready(function(){
    $('.toggle').click(function(){
        var target = $(this).attr('ref');
        $(this).parent().parent().find('.' + target).slideToggle();
        return false;
    });
    
    $(".tree a").click(function()
    {
        /*
get_tree_path = "/restore/get_tree/";
        update_tree($(this).attr("path"), get_tree_path, '.tree');
*/
        get_tree_path = "/restore/get_tree/";
        if (!document.getElementsByClassName('wait')[0]) {
            update_tree($(this).attr("path"), get_tree_path, '.tree');
        } else {
            $('.wait').remove();
        }
        return false;
    });

    $(".tree_computer a").click(function()
    {
        get_tree_path = "/restore/get_client_tree/";
        update_tree($(this).attr("path"), get_tree_path, ".tree_computer", "radio", "path_restore");
        return false;
    });

    $('#buscar_arquivos').click(function(){
        get_tree_path = "/restore/get_tree/";
        
        job_id = $('#jobs_list').val();
        pattern = $('#pattern').val();
        root_path = '/';
        $('.tree .directory.first ul').remove().removeClass("open");
        
        $.post($("#url_tree").val(),
               {job_id: job_id, pattern: pattern},
               function(data) {
                   mount_tree(data, root_path, get_tree_path)
               },
               "json");
        return false;
    });
    
    $('#procedure_id').change(function()
    {
        if ($(this).val()) {
            $('.restore_step_1').slideDown();
        } else {
            $('.restore_step_1').slideUp();
        }
    });
    $('#procedure_id').change();
    
    $('#computer_id').change(function()
    {
        var computer_id = $(this).val();
        $.getJSON('/restore/get_procedures/' + computer_id + '/', {}, function(data)
        {
            if (data['error']) {

                //help-me fix-me
                $('.computer_error').html($('<p>').text(data['error'])).addClass("message error").append('<span class="close" title="Dismiss"></span>').fadeIn('slow');
            	jQuery('.message .close').hover(
        		function() { jQuery(this).addClass('hover'); },
        		function() { jQuery(this).removeClass('hover'); }
	            );

                jQuery('.message .close').click(function() {
                    jQuery(this).parent().fadeOut('slow', function() { jQuery(this).remove(); });
                });
                

            }
        
            $('#procedure_id').empty();
            $('<option>').attr('value', '').text(' - Selecione - ').appendTo('#procedure_id');
            for (proc in data) {
                proc = data[proc];
                if (proc['fields'] && proc['fields']['name']) {
                    $('<option>').attr('value', proc['pk']).text(proc['fields']['name']).appendTo("#procedure_id");
                }
            }
            $('.procedure_select').slideDown();
        });
    });
    $('#computer_id').change();

    $('#procedure_id').change(function()
    {
        if ($(this).val()) {
            $('.restore_step_1').slideDown();
        } else {
            $('.restore_step_1').slideUp();
        }
    });
    $('#procedure_id').change();
    
    $('.submit_step_1').click(function(){
        data_inicio = $('#data_inicio').val();
        data_inicio = data_inicio.replace(/\//gi,"-");
        data_fim = $('#data_fim').val();
        data_fim = data_fim.replace(/\//gi,"-");
        computer_id = $('#computer_id').val();
        procedure_id = $('#procedure_id').val();
    
        $('.restore_step_2').slideUp();
        $('.restore_step_3').slideUp();
        $('.restore_step_4').slideUp();
        $('.restore_step_5').slideUp();
        
        if (data_inicio && data_fim) {
            //alert('/restore/get_jobs/' + procedure_id + '/' + data_inicio + '/' + data_fim + '/');
            $.getJSON(
                '/restore/get_jobs/' + procedure_id + '/' + data_inicio + '/' + data_fim + '/',
                function(data)
                {
                    $("#jobs_list").empty();
                    if (data) {
                        // TODO: Populate the jobs list.
                        $("<option>").val("").text(" - " + data.length + " jobs, selecione um  - ").attr("selected", "selected").appendTo("#jobs_list");
                        // exemplo
                        //$("<option>").val("2").text(" Job de exemplo, selecione este ").attr("selected", "selected").appendTo("#jobs_list");
                        for (var i in data) {
                            job = data[i];
                            if (job.fields && job.fields.realendtime) {
                                $("<option>").val(job.pk).text(job.fields.realendtime + ' - ' + job.fields.jobfiles + ' arquivos').appendTo("#jobs_list");
                            }
                        }
                        $("#jobs_list").change();
                        $('.restore_step_2').slideDown();
                    }
                }
            );
        }
    
        return false;
    });
    
    $('.submit_step_1').click();
    
    
    $('#jobs_list').change(
        function(){
            $('.restore_step_3').slideUp();
            
            $('.tree .directory.first ul').remove().removeClass("open");
            
            if ($(this).val()) {
                $('.restore_step_3').slideDown();
            } else {
                $('.restore_step_3').slideUp();
            }
        }
    ).click();
    
    $(".open_step_4").click(function(){
        $(".restore_step_4").slideDown();
        return false;
    });
    
    
    $('#pattern').keydown(
        function(e){
            if (e.keyCode == 13) {
                $('#buscar_arquivos').click();
                return false;
            }
        }
    )
});
