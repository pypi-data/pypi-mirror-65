var tkOverviewGraphTimeValue;
var tkScheduleTable;
var tkScheduleTableWeek;
var tkSummaryWeek;
function roundTKVal(num) {
    return Math.round(num * 100) / 100;
}

function disDeriv(a) {
    var b = $.extend(true, [], a);
    b.unshift("0");
    a.push("0");
    var c = a.map(function (v, i) {
        return (v - b[i]);
    });
    a.pop();
    c.pop();
    c[0] = 0;
    return c;
}
function drawSummaryToday(minActivity) {
    if (typeof tkSummaryToday !== 'undefined') {
        tkSummaryToday.destroy();
    }

    var minRestDay = 1440 - minActivity;
    var hourActivity = roundTKVal(minActivity / 60);
    var hourRestDay = roundTKVal(minRestDay / 60);

    // Donut Chart
    var pieChartCanvas = $('#canvas_sum_today').get(0).getContext('2d')
    var pieData = {
        labels: [
            'Rest of Day(' + hourRestDay + ' Hrs)',
            'This Activity(' + hourActivity + ' Hrs)',
        ],
        datasets: [
            {
                data: [minRestDay, minActivity],
                backgroundColor: ['#FFFFFF', '#00a65a'],
            }
        ]
    }
    var pieOptions = {
        legend: {
            display: false
        },
        maintainAspectRatio: false,
        responsive: true,
    }
    //Create pie or douhnut chart
    // You can switch between pie and douhnut using the method below.
    tkSummaryToday = new Chart(pieChartCanvas, {
        type: 'pie',
        data: pieData,
        options: pieOptions
    });
}
function drawSummaryWeek(hoursArray) {
    if (typeof tkSummaryWeek !== 'undefined') {
        tkSummaryWeek.destroy();
    }
    // Sales chart
    var salesChartCanvas = document.getElementById('canvas_sum_week').getContext('2d');

    var netHoursArray = disDeriv(hoursArray);

    //$('#revenue-chart').get(0).getContext('2d');

    var salesChartData = {
        labels: ['6 Days Ago', '5 Days Ago', '4 Days Ago', '3 Days Ago', '2 Days Ago', 'Yesterday', 'Today'],
        datasets: [
            {
                label: 'Hours',
                backgroundColor: 'rgba(60,141,188,0.9)',
                borderColor: 'rgba(60,141,188,0.8)',
                pointRadius: false,
                pointColor: '#3b8bba',
                pointStrokeColor: 'rgba(60,141,188,1)',
                pointHighlightFill: '#fff',
                pointHighlightStroke: 'rgba(60,141,188,1)',
                data: hoursArray
            },
            {
                label: 'Rate of Hours',
                backgroundColor: 'rgba(210, 214, 222, 1)',
                borderColor: 'rgba(210, 214, 222, 1)',
                pointRadius: false,
                pointColor: 'rgba(210, 214, 222, 1)',
                pointStrokeColor: '#c1c7d1',
                pointHighlightFill: '#fff',
                pointHighlightStroke: 'rgba(220,220,220,1)',
                data: netHoursArray
            },
        ]
    };

    var salesChartOptions = {
        maintainAspectRatio: false,
        responsive: true,
        legend: {
            display: false
        },
        scales: {
            xAxes: [{
                    gridLines: {
                        display: false,
                    }
                }],
            yAxes: [{
                    gridLines: {
                        display: false,
                    },
                    ticks: {
                        suggestedMax: 60 * 3  // minimum value will be 0.
                    }
                }]
        }
    };

    var lineChartData = jQuery.extend(true, {}, salesChartData);
    lineChartData.datasets[0].fill = false;
    lineChartData.datasetFill = false;

    tkSummaryWeek = new Chart(salesChartCanvas, {
        type: 'line',
        data: lineChartData,
        options: salesChartOptions
    });
}
function drawScheduleTable(hoursArray) {
    if (typeof tkScheduleTable !== 'undefined') {
        tkScheduleTable.destroy();
    }
    var salesChartData = {
        labels: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'],
        datasets: [
            {
                label: 'Minutes',
                backgroundColor: 'rgba(60,141,188,0.9)',
                borderColor: 'rgba(60,141,188,0.8)',
                pointRadius: false,
                pointColor: '#3b8bba',
                pointStrokeColor: 'rgba(60,141,188,1)',
                pointHighlightFill: '#fff',
                pointHighlightStroke: 'rgba(60,141,188,1)',
                data: hoursArray
            },
        ]
    };



    var stackedBarChartCanvas = $('#canvas_schedule').get(0).getContext('2d')
    var stackedBarChartData = jQuery.extend(true, {}, salesChartData)

    var stackedBarChartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            xAxes: [{
                    stacked: true,
                    display: true,
                    ticks: {
                        suggestedMax: 60,
                        beginAtZero: true   // minimum value will be 0.
                    }
                }],
            yAxes: [{
                    stacked: true,

                }]
        }
    };

    tkScheduleTable = new Chart(stackedBarChartCanvas, {
        type: 'horizontalBar',
        data: stackedBarChartData,
        options: stackedBarChartOptions
    });
}
function drawScheduleTableWeek(hoursArrayWeek) {
    if (typeof tkScheduleTableWeek !== 'undefined') {
        tkScheduleTableWeek.destroy();
    }
    var salesChartData = {
        labels: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'],
        datasets: [
            {
                label: '6 Days Ago',
                backgroundColor: 'rgba(140,141,230,0.9)',
                borderColor: 'rgba(140,141,230,0.8)',
                pointRadius: false,
                pointColor: '#3b8bba',
                pointStrokeColor: 'rgba(140,141,230,1)',
                pointHighlightFill: '#fff',
                pointHighlightStroke: 'rgba(140,141,230,1)',
                data: hoursArrayWeek[0]
            },
            {
                label: '5 Days Ago',
                backgroundColor: 'rgba(30,255,188,0.9)',
                borderColor: 'rgba(30,255,188,0.8)',
                pointRadius: false,
                pointColor: '#3b8bba',
                pointStrokeColor: 'rgba(30,255,188,1)',
                pointHighlightFill: '#fff',
                pointHighlightStroke: 'rgba(30,255,188,1)',
                data: hoursArrayWeek[1]
            },
            {
                label: '4 Days Ago',
                backgroundColor: 'rgba(100,100,30,0.9)',
                borderColor: 'rgba(100,100,30,0.8)',
                pointRadius: false,
                pointColor: '#3b8bba',
                pointStrokeColor: 'rgba(100,100,30,1)',
                pointHighlightFill: '#fff',
                pointHighlightStroke: 'rgba(100,100,30,1)',
                data: hoursArrayWeek[2]
            },
            {
                label: '3 Days Ago',
                backgroundColor: 'rgba(230,200,10,0.9)',
                borderColor: 'rgba(230,200,10,0.8)',
                pointRadius: false,
                pointColor: '#3b8bba',
                pointStrokeColor: 'rgba(230,200,10,1)',
                pointHighlightFill: '#fff',
                pointHighlightStroke: 'rgba(230,200,10,1)',
                data: hoursArrayWeek[3]
            },
            {
                label: '2 Days Ago',
                backgroundColor: 'rgba(60,30,20,0.9)',
                borderColor: 'rgba(60,30,20,0.8)',
                pointRadius: false,
                pointColor: '#3b8bba',
                pointStrokeColor: 'rgba(60,30,20,1)',
                pointHighlightFill: '#fff',
                pointHighlightStroke: 'rgba(60,30,20,1)',
                data: hoursArrayWeek[4]
            },
            {
                label: 'Yesterday',
                backgroundColor: 'rgba(210, 214, 222,0.9)',
                borderColor: 'rgba(210, 214, 222,0.8)',
                pointRadius: false,
                pointColor: '#3b8bba',
                pointStrokeColor: 'rgba(210, 214, 222,1)',
                pointHighlightFill: '#fff',
                pointHighlightStroke: 'rgba(210, 214, 222,1)',
                data: hoursArrayWeek[5]
            },
            {
                label: 'Today',
                backgroundColor: 'rgba(60,141,188,0.9)',
                borderColor: 'rgba(60,141,188,0.8)',
                pointRadius: false,
                pointColor: '#3b8bba',
                pointStrokeColor: 'rgba(60,141,188,1)',
                pointHighlightFill: '#fff',
                pointHighlightStroke: 'rgba(60,141,188,1)',
                data: hoursArrayWeek[6]
            }
        ]
    };



    var stackedBarChartCanvas = $('#canvas_schedule_week').get(0).getContext('2d')
    var stackedBarChartData = jQuery.extend(true, {}, salesChartData)

    var stackedBarChartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            xAxes: [{
                    stacked: true,
                    display: true,
                    ticks: {
                        suggestedMax: (60 * 7),
                        beginAtZero: true   // minimum value will be 0.
                    }
                }],
            yAxes: [{
                    stacked: true,

                }]
        }
    };

    tkScheduleTableWeek = new Chart(stackedBarChartCanvas, {
        type: 'horizontalBar',
        data: stackedBarChartData,
        options: stackedBarChartOptions
    });
}
function tkprepGraphs(hoursArray) {
    if (typeof tkOverviewGraphTimeValue !== 'undefined') {
        tkOverviewGraphTimeValue.destroy();
    }
    var ticksStyle = {fontColor: '#495057',fontStyle: 'bold'};
    var mode = 'index';
    var intersect = true;
    var netHoursArray = disDeriv(hoursArray);
    var $visitorsChart = $('#visitors-chart');
    tkOverviewGraphTimeValue = new Chart($visitorsChart, {
        data: {
            labels: ['6 Days Ago', '5 Days Ago', '4 Days Ago', '3 Days Ago', '2 Days Ago', 'Yesterday', 'Today'],
            datasets: [{
                    type: 'line',
                    data: hoursArray,
                    backgroundColor: 'transparent',
                    borderColor: '#007bff',
                    pointBorderColor: '#007bff',
                    pointBackgroundColor: '#007bff',
                    fill: false
                            // pointHoverBackgroundColor: '#007bff',
                            // pointHoverBorderColor    : '#007bff'
                },
                {
                    type: 'line',
                    data: netHoursArray,
                    backgroundColor: 'tansparent',
                    borderColor: '#ced4da',
                    pointBorderColor: '#ced4da',
                    pointBackgroundColor: '#ced4da',
                    fill: false
                            // pointHoverBackgroundColor: '#ced4da',
                            // pointHoverBorderColor    : '#ced4da'
                }]
        },
        options: {
            maintainAspectRatio: false,
            tooltips: {
                mode: mode,
                intersect: intersect
            },
            hover: {
                mode: mode,
                intersect: intersect
            },
            legend: {
                display: false
            },
            scales: {
                yAxes: [{
                        // display: false,
                        gridLines: {
                            display: true,
                            lineWidth: '4px',
                            color: 'rgba(0, 0, 0, .2)',
                            zeroLineColor: 'transparent'
                        },
                        ticks: $.extend({
                            beginAtZero: true,
                            suggestedMax: 10
                        }, ticksStyle)
                    }],
                xAxes: [{
                        display: true,
                        gridLines: {
                            display: false
                        },
                        ticks: ticksStyle
                    }]
            }
        }
    });
}
jQuery(document).ready(function () {
    tkprepGraphs([0, 0, 0, 0, 0, 0, 0]);

});