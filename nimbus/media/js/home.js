
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

    function create_chart(obj_id, data, ticks, chart_type, labels) {
        var fill = false;
        var render = $.jqplot.PieRenderer;
        var highlighter_show = true;
        var cursor_show = true;
        var pointLabels_show = false;

        if (chart_type == 'bar') {
            var render = $.jqplot.BarRenderer;
            highlighter_show = false;
            cursor_show = false;
            pointLabels_show = true;
        } else if (chart_type == 'area') {
            var render = $.jqplot.LineRenderer;
            var fill = true;
        }

        $.jqplot(obj_id, [data], {
            seriesDefaults: {
                renderer: render,
                pointLabels: {
                    location:'s',
                    show: pointLabels_show,
                    labels: labels
                },
                fill: true,
                /* color: '#95BACB', */
                color: '#67c7a1',
                markerOptions: {
                    show: true,
                    lineWidth: 5,
                    size: 5,
                    color: 'red'
                }
            },
            axes: {
                xaxis: {
                    renderer: $.jqplot.CategoryAxisRenderer,
                    ticks: ticks,
                    min: 0
                },
                yaxis: {
                    tickOptions:{ 
                        mark: 'outside',    // Where to put the tick mark on the axis
                                    // 'outside', 'inside' or 'cross',
                        showMark: true,
                        showGridline: true, // wether to draw a gridline (across the whole grid) at this tick,
                        markSize: 4,        // length the tick will extend beyond the grid in pixels.  For
                                            // 'cross', length will be added above and below the grid boundary,
                        show: true,         // wether to show the tick (mark and label),
                        showLabel: true,    // wether to show the text label at the tick,
                        formatString: '%.2f',
                    },
                    min: 0,
                    //max: 2000
                     
                }
            },
            highlighter: { show:highlighter_show },
            cursor: { show: cursor_show },
        });
    };


    $('.jqplotchart').each(function(){
        var chart_id = $(this).attr('id');
        var data = $(this).children().filter('chartdata').text().split(',');
        data = $.map(data, function(e){
            return parseFloat(e);
        });
        var labels = $(this).children().filter('chartlabels').text().split(',');
        var header = $(this).children().filter('chartheader').text().split(',');
        var chart_type = $(this).attr('charttype');
        $(this).text('');

        create_chart(chart_id, data, header, chart_type, labels);
    });
});
