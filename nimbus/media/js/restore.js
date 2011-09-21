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

// Todo o código abaixo e referente apenas ao STEP 4
$(document).ready(function(){
    $('#buscar_arquivos').click(function(){
        do_search();
    });
    $('#add_checked').click(function(){
        for (var f = 0; f < $(".full_path").length; f++) {
            if ($(".full_path")[f].checked == true) {
                append_file_to_restore($(".full_path")[f].value)
            }
        }
        return false;
    });
    $("#submit_files").click(function() {
        if ($(".added_file").length == 0) {
            alert("Nenhum arquivo foi selecionado para restauração");
            return false;
        } else {
            for (var f = 0; f < $(".added_file").length; f++) {
                console.log($(".added_file")[f].textContent);
                $("#step4_form").append("<input type='hidden' name='paths' value='"+ $(".added_file")[f].textContent +"'></input>");
            }
            $("#step4_form").submit();
        }
    });
    // Trata se alguem apertar ENTER no campo de busca de arquivos
    $("#pattern").keypress(function(e) {
        code= (e.keyCode ? e.keyCode : e.which);
        if (code == 13) {
            do_search();
            e.preventDefault();
        }
    });
});
    function do_search() {
        get_tree_path = "/restore/get_tree/";
        $(".search_result").remove();
		$("#search_result_list").append("<li class='search_result'>Buscando arquivos <img src='/media/icons/loading_bar.gif'/></li>");    
        // jobid = job_id.value
        pattern = $('#pattern').val();
        root_path = '/';
    
        $.post("/restore/get_tree_search_file/",
               {job_id: job_id.value, pattern: pattern},
               function(data) {
                   $(".search_result").remove();
                   if (data.length == 0) {
                       $("#search_result_list").append("<li class='search_result'>Nenhum arquivo encontrado</li>");
                   } else {
                       for (var f = 0; f < data.length; f++) {
                           append_file_to_search(data[f]);
                       }
                   }
               },
               "json");
        return false;
    }
    function path_kind(path) {
        if (path[path.length -1] == "/") {
            var kind = "directory";
        } else {
            var kind = "file";
        };
        return kind
    };
    function append_file_to_search(file) {
        var kind = path_kind(file);
        $("#search_result_list").append('<li class="'+kind+' search_result" onClick="append_file_to_restore($(this)[0].textContent);"><span class="listed_file">' + file + '</span></li>')
    };
    function append_file_to_restore(file) {
        var kind = path_kind(file);
        $("#restore_file_list").append('<li class="'+kind+' selected_file" onClick="$(this).remove();"><span class="added_file">' + file + '</span></li>')
    }
// Fim do código do STEP 4
