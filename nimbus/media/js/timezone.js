
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

$(document).ready(function() {
    function getAreaChoices() {
        $.ajax({
            type: "POST",
            url: $("#area_request").val(),
            dataType: "json",
            data: {country: $('[name=country]').val()},
            success: function(data, textStatus){
                $("select#id_area").empty();
                $.each(data, function(i, item){
                    $("select#id_area").append(
                        '<option value="'+item+'" selected="selected">'+item+'</option>'
                    );
                });
                $("select#id_area").change();
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                alert("Erro: Não foi possível obter a lista de fusos horários.");
                this; // the options for this ajax request
            }
        });
    }
    
    $("select#id_country").bind("change", getAreaChoices);
});