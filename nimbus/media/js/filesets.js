
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
    $('#filepath_template').clone().appendTo('.filepaths').show();
    
    $('.toggle').click(function(){
        var target = $(this).attr('ref');
        $(this).parent().parent().find('.' + target).slideToggle();
    });
    
    get_tree_path = "/filesets/get_tree/";
    
    $('#update_tree').click(function()
    {
        update_tree('/', get_tree_path);
        return false;
    });
    
    $(".tree a").click(function() {
        if (!document.getElementsByClassName('wait')[0]) {
            update_tree($(this).attr("path"), get_tree_path);
        } else {
            $('.wait').remove();
        }
        return false;
    });
    
    function adicionar_path(obj) {
        if (obj) {
            $('#filepath_template').clone().insertAfter($(obj).parent()).show();
        } else {
            $('#filepath_template').clone().appendTo('.filepaths').show();
        }
        
        $('.filepaths .add').click(function(){
            adicionar_path(this);
        });
        
        $('.filepaths .del').unbind('click').click(function(){
            remover_path(this);
        });
    }
    
    function remover_path(obj) {
        $(obj).parent().remove();
        if ($('#filepath_template').parent().children().length == 1) {
            adicionar_path();
        }
    }

    $('.filepaths .add').click(function(){
        adicionar_path(this);
    });

    $('.filepaths .del').click(function(){
        remover_path(this);
    });

    $('#computer_id').change(function(){
        $('.tree > li ul').first().remove();
    });
    
    
});
$(document).ready(function(){
    function async_submit() {
        $(".field_error").hide();
        $.ajax({
            type: "POST",
            url: $('#main_form')[0].action,
            data: $('#main_form').serialize(),
            success: function(j) {
                var response = jQuery.parseJSON(j);
                if (response.status == true) {
                    FILESET_ID = response.fileset_id;
                    $(".fileset_return").val(FILESET_ID);
                    FILESET_NAME = response.fileset_name;
                    // alert(response.message);
                    $.facebox.close();
                    set_fileset();
                    //location.reload();
                    href = window.location.href;
                    if (href.search("/procedures/profile/list/") > 0){
                        window.location = "/procedures/profile/list/#fileset_"+response.fileset_id;
                        location.reload();
                    }
                } else {
                    $("#field_error_" + response.error).show();
                    alert(response.message);
                }
            }
        });  
    };
    $('#submit_button').click(function(){
		var all_paths = $('.full_path');
		var checked_paths = new Array()
		for (var i = 0; i < all_paths.length; i++) {
			if (all_paths[i].checked == true) {
				checked_paths.push(all_paths[i].value);
			};
		};
		var inicial = parseInt($('#id_files-INITIAL_FORMS')[0].value)
		var total = inicial + checked_paths.length
		$('#id_files-TOTAL_FORMS').val(total);
		for (var i = 0; i < checked_paths.length; i++) {
		    var n = i + inicial;
			var new_path_field = '\n' + 
			'<input id="id_files-'+ n + '-path" type="hidden" name="files-'+ n +'-path" maxlength="2048" class="text" value="' + checked_paths[i] + '">\n' +
			'<input type="hidden" name="files-' + n + '-fileset" id="id_files-' + n + '-fileset">\n' +
			'<input type="hidden" name="files-' + n + '-id" id="id_files-' + n + '-id">\n';
			$('#main_form').append(new_path_field);
		};
        // $('#main_form').submit();
        if (total == 0) {
            alert("Nenhum arquivo foi selecionado")
        } else {
            if (typeof NOT_ASYNC != "undefined") {
                $('#main_form').submit()
            } else {
                async_submit();
            }
        }
	});
});

function discard_unused_fileset(fileset_id) {
    $.ajax({
        type: "POST",
        url: "/filesets/reckless_discard/",
        data: {"fileset_id": fileset_id},
        success: function(j) {
            console.log(j);
		}
    });
}