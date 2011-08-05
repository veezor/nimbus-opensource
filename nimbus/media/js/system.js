
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
    
    $('#form_ping').submit(function(){
        $('#mensagem').slideUp().empty();
        $('#mensagem').html('<img src="/media/icons/loading_bar.gif" /> Aguarde...');
        $('#mensagem').slideDown();
        
        var type = $('#type').val();
        $.post("/system/create_or_view_network_tool/", {ip: $('#ip').val(), type: type},
            function(data){
                $('#mensagem').empty();
                if (!data) {
                    $('#mensagem').html("Erro ao executar o ping.");
                    return false;
                }
                
                $('#mensagem').html(data.msg.replace(/\n/g, "<br/>"));
            },
            "json");
        return false;
    });
    
    function update_table(table) {
        table = $('.request_list');
        $.post($(".atualizar_agora").attr("rel"), {ajax: 1}, function(data)
        {
            table.find('tbody tr').remove();
            for (var item in data) {
                down = data[item];
                tr = $('<tr>');
                pid = $('<td>').text(down.fields.pid);
                name = $('<td>').text(down.fields.name);
                criado_em = $('<td>').text(down.fields.created_at);
                estado = $('<td>').text(down.fields.status);
                
                tr.append(pid).append(name).append(criado_em).append(estado);
                tr.appendTo(table.find('tbody'));
            }
        },
        "json");
    }
    
    var countDownInterval = 20;
    var countDownTime = countDownInterval + 1;
    var counter = undefined;
    
    function countDown(){
        countDownTime--;
        if (countDownTime <= 0){
            $('.tempo_restante').text(countDownTime);
            countDownTime = countDownInterval;
            clearInterval(counter);
            update_table();
            return startit();
        }
        $('.tempo_restante').text(countDownTime);
    }

    function startit(){
        $('.tempo_restante').text(countDownTime);
        countDown();
        counter=setInterval(countDown, 1000);
    }

    startit();
    $('.atualizar_agora').click(function(){
        update_table();
        countDownTime = countDownInterval;
        clearInterval(counter);
        startit();
    });
});