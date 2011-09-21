
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
	
	// Preload images
    // jQuery.preloadCssImages();
	
	// uniform select fields
	//$("select").uniform();
	// CSS tweaks
	jQuery('#header #nav li:last').addClass('nobg');
	jQuery('.block_head ul').each(function() { jQuery('li:first', this).addClass('nobg'); });
	jQuery('.block table tr:odd').css('background-color', '#fbfbfb');
	jQuery('.block form input[type=file]').addClass('file');
			
	
	// Web stats
	jQuery('table.stats').each(function() {
		var statsType;
		
		if(jQuery(this).attr('rel')) { statsType = jQuery(this).attr('rel'); }
		else { statsType = 'area'; }
		
        // console.log(jQuery(this).css('width'));
		if (jQuery(this).css('width') && parseInt(jQuery(this).css('width')) < 880) {
		    width = (parseFloat(jQuery(this).css('width')) / 100) * 880 + 'px';
		} else {
		    width = '880px';
		}
		
        // console.log(width);
		
        // jQuery(this).hide().visualize({
        //  type: statsType,    // 'bar', 'area', 'pie', 'line'
        //  width: width,
        //  height: '240px',
        //  colors: ['#6fb9e8', '#ec8526', '#9dc453', '#ddd74c']
        // });
	});
	
	
	// Check / uncheck all checkboxes
	jQuery('.check_all').click(function() {
		jQuery(this).parents('form').find('input:checkbox').attr('checked', jQuery(this).is(':checked'));   
	});
		
	
	// Set WYSIWYG editor
	//jQuery('.wysiwyg').wysiwyg({css: "css/wysiwyg.css"});
	
	
	// Modal boxes - to all links with rel="facebox"
	//jQuery('a[rel*=facebox]').facebox()
	
	
	// Messages
	jQuery('.message').hide().append('<span class="close" title="Dismiss"></span>').fadeIn('slow');
	jQuery('.message .close').hover(
		function() { jQuery(this).addClass('hover'); },
		function() { jQuery(this).removeClass('hover'); }
	);
		
	jQuery('.message .close').click(function() {
		jQuery(this).parent().fadeOut('slow', function() { jQuery(this).remove(); });
	});
	
	
	// Form select styling
	//jQuery("form select.styled").select_skin();
	
	
	// Tabs
    jQuery(".tab_content").hide();
    jQuery("ul.tabs li:first-child").addClass("active").show();
    jQuery(".tab_content:first").show();
    
    jQuery("ul.tabs li").click(function() {
        jQuery(this).parent().find('li').removeClass("active");
        jQuery(this).addClass("active");
        jQuery(this).parents('.block').find(".tab_content").hide();
    
        var activeTab = jQuery(this).find("a").attr("href");
        jQuery(activeTab).show();
        return false;
    });
	
	
	// Sidebar Tabs
	jQuery(".sidebar_content").hide();
	jQuery("ul.sidemenu li:first-child").addClass("active").show();
	jQuery(".block").find(".sidebar_content:first").show();

	jQuery("ul.sidemenu li").click(function() {
		jQuery(this).parent().find('li').removeClass("active");
		jQuery(this).addClass("active");
		jQuery(this).parents('.block').find(".sidebar_content").hide();

		var activeTab = jQuery(this).find("a").attr("href");
		jQuery(activeTab).show();
		return false;
	});	
	
	
	// Block search
	jQuery('.block .block_head form .text').bind('click', function() { jQuery(this).attr('value', ''); });
	
	
	// Image actions menu
	jQuery('ul.imglist li').hover(
		function() { jQuery(this).find('ul').css('display', 'none').fadeIn('fast').css('display', 'block'); },
		function() { jQuery(this).find('ul').fadeOut(100); }
	);
	
		
	// Image delete confirmation
	jQuery('ul.imglist .delete a').click(function() {
		if (confirm("Are you sure you want to delete this image?")) {
			return true;
		} else {
			return false;
		}
	});
	
	
	// Style file input
    // jQuery("input[type=file]").filestyle({ 
    //     image: "/media/lib/images/upload.gif",
    //     imageheight : 30,
    //     imagewidth : 80,
    //     width : 250
    // });
	
	
	// File upload
	if (jQuery('#fileupload').length) {
		new AjaxUpload('fileupload', {
			action: 'upload-handler.php',
			autoSubmit: true,
			name: 'userfile',
			responseType: 'text/html',
			onSubmit : function(file , ext) {
					jQuery('.fileupload #uploadmsg').addClass('loading').text('Uploading...');
					this.disable();	
				},
			onComplete : function(file, response) {
					jQuery('.fileupload #uploadmsg').removeClass('loading').text(response);
					this.enable();
				}	
		});
	}
		
		
	jQuery.extend(DateInput.DEFAULT_OPTS, {
      month_names: ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"],
      short_month_names: ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"],
      short_day_names: ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]
    });
    
    jQuery.extend(DateInput.DEFAULT_OPTS, {
        stringToDate: function(string) {
            var matches;
            if (matches = string.match(/^(\d{2,2})-(\d{2,2})-(\d{4,4})jQuery/)) {
                return new Date(matches[3], matches[2] - 1, matches[1]);
            } else {
                return null;
            };
        },

        dateToString: function(date) {
            var month = (date.getMonth() + 1).toString();
            var dom = date.getDate().toString();
            if (month.length == 1) month = "0" + month;
            if (dom.length == 1) dom = "0" + dom;
            return dom + "-" + month + "-" + date.getFullYear();
        }
    });
    
	// Date picker
	jQuery('input.date_picker').date_input();
	

	// Navigation dropdown fix for IE6
	if(jQuery.browser.version.substr(0,1) < 7) {
		jQuery('#header #nav li').hover(
			function() { jQuery(this).addClass('iehover'); },
			function() { jQuery(this).removeClass('iehover'); }
		);
	}
	
	// IE6 PNG fix
	jQuery(document).pngFix();
	
	var data_hora = undefined;
	function update_time() {
		seconds = data_hora.getSeconds() + 1;
		if (seconds > 60) {
			seconds = 1;
		}
		data_hora.setSeconds(seconds);

		time_string = data_hora.toTimeString().substr(0, 8);
		$('#actual_time').html(time_string);
		setTimeout(update_time, 1000);
	}
	
	$('.filetree').each(function(){
		var script = $(this).attr("ref");
		$(this).fileTree({ root: '/media/lib/demo/', script: script }, function(file) { 
			alert(file);
		});
	})
	
	var actual_time_html = $('#actual_time').html();
    if (actual_time_html != null) {
        var actual_time = actual_time_html.split(':');
        var hours = actual_time[0];
        var minutes = actual_time[1];
        var seconds = actual_time[2];
        data_hora = new Date(2010, 10, 10, hours, minutes, seconds);
        update_time();
    }
            
	$(".date_picker").mask('99/99/9999');
	$(".date_picker").bind("blur focus change click keyup", function(){
	   $(this).mask('99/99/9999');
	});
	$('.mascara_hora').mask('99:99');
	$('.mascara_minuto').mask('99');
});
