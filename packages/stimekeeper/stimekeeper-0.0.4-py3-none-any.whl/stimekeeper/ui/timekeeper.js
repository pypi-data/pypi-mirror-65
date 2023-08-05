var tkMaxID = 1;
var tkStartTime = Date.now();
var tkTimeEnable = false;
var currPopID = "";
var currBadgeHolder = Array(5).fill('');
var tkSummaryToday;
var listOfSeven = {"-1": [0, 0, 0, 0, 0, 0, 0], "1": [0, 0, 0, 0, 0, 0, 0], "-5": [0, 0, 0, 0, 0, 0, 0]};
var listOfReady = {"-1": false, "1": false, "-5": false};
var listOfData = {"-1": [], "1": [], "-5": []};
var tkSliderClassType;
var tkTimeValueEnable = true;
function tk_id(tk_input) {
    return tk_input.substring(7);
}

function openSummary() {
    $('.card_summary_activity').show();
    $('.card_tasklist').hide();
    $('.card_overview').hide();
    $('.tk_grp').addClass("tk_inv");
}
function openTaskList() {
    $('.card_summary_activity').hide();
    $('.card_tasklist').show();
    $('.card_overview').hide();
    $('.tk_grp').addClass("tk_inv");
}
function openOverview() {
    $('.card_summary_activity').hide();
    $('.card_tasklist').hide();
    $('.card_overview').show();
    $('.tk_grp').removeClass("tk_inv");
}
function prepOverview() {
    listOfReady["-1"] = false;
    listOfReady["1"] = false;
    listOfReady["-5"] = false;
    getSummary("-1", true, false);
    getSummary("1", true, false);
    getSummary("-5", true, false);
}
function tkOverviewGraphTab() {
    $('.tk_tbe').addClass("tk_inv");
    $('.tk_gra').removeClass("tk_inv");
    $('.tk_grp').removeClass("tk_inv");
}
function tkOverviewTableTab() {
    $('.tk_gra').addClass("tk_inv");
    $('.tk_tbe').removeClass("tk_inv");
    $('.tk_grp').addClass("tk_inv");

}
function prepOverviewGraph() {
    if (listOfReady["-1"] && listOfReady["1"] && listOfReady["-5"]) {
        var a = tkMultTimeArrays(listOfSeven["-1"], -1);
        var b = tkMultTimeArrays(listOfSeven["1"], 1);
        var c = tkMultTimeArrays(listOfSeven["-5"], -5);
        var totalList = tkAddTimeArrays(tkAddTimeArrays(a, b), c);
        $(".tk_tod").html("*" + totalList[6]);
        tkprepGraphs(totalList);
        $(".tk_tbl").html("");
        tkGetNameTimeType(listOfData["-1"]);
        tkGetNameTimeType(listOfData["1"]);
        tkGetNameTimeType(listOfData["-5"]);


    }
}

function tkSlideUpdateBackground() {
    if (tkTimeValueEnable) {
        var val = tkSliderClassType.bootstrapSlider('getValue');
        if (val === 1) {
            $(".main-footer").css("background-color", "#dc3545");
        } else if (val === 2) {
            $(".main-footer").css("background-color", "#17a2b8");
        } else {
            $(".main-footer").css("background-color", "#28a745");
        }
    }
}
function tkGetNameTimeType(listData) {
    if (!($.isEmptyObject(listData))) {

        var time;
        for (var key of Object.keys(listData)) {
            if (typeof listData[key].Elapsed !== 'undefined') {
                time = listData[key].Elapsed;
            } else {
                time = listData[key].Duration;
            }
            tkAddTDP(listData[key].Log, time, listData[key].TimeValue);
        }
    }
}
function tkAddTDP(name, time, type) {
    var badge;
    if (type==="-1"){
        badge="info";
    }else if (type==="-5"){
        badge="danger";
    }else{
        badge="success";
    }
    $(".tk_tbl").append(`<tr>
                                                        <td>${name}</td>
                                                        <td>${time}</td>
                                                        <td>
                                                            <span class="badge badge-${badge} tk_spc">${type}</span> <i class="fas fa-chart-bar tk_spb" data-openname="${name}"></i>
                                                        </td>
                                                    </tr>`);
}
function tkMultTimeArrays(a, b) {
    var c = a.map(function (v, i) {
        return (v * b / 60);
    });
    return c;
}
function tkAddTimeArrays(a, b) {
    var c = a.map(function (v, i) {
        return (v + b[i]);
    });
    return c;
}
function getTrack() {
    $.getJSON("../Track/Last")
            .done(function (json) {
                if (typeof json.Log.Log !== 'undefined') {//This will be false if the Task name itself is "Last"
                    json = json.Log;
                }
                if (typeof json.Start !== 'undefined') {
                    $("#tf_act").text(json.Log);
                    var d = new Date(json.Start * 1000);
                    tkStartTime = d.getTime();
                    tkTimeEnable = true;
                    console.log("JSON Data!: " + json.Log + json.Start);

                }
            })
            .fail(function (jqxhr, textStatus, error) {
                var err = textStatus + ", " + error;
                console.log("Request Failed: " + err);
                toastr.error("Failed");
            });
}
function getArrayMinutes(secondsArray) {
    var minutesArray = []
    for (var i = 0, length = secondsArray.length; i < length; i++) {
        minutesArray[i] = secondsArray[i] / 60;
    }
    return minutesArray;
}
function getWeekMinutes(lastSevenArray) {

    var minutesArray = []
    for (var i = 0, length = lastSevenArray.length; i < length; i++) {
        minutesArray[i] = lastSevenArray[i].DayTotal / 60;
    }
    return minutesArray.reverse();
}
function getArrayMinutesWeek(lastSevenArray) {
    var minutesArray = []
    for (var i = 0, length = lastSevenArray.length; i < length; i++) {
        minutesArray[i] = getArrayMinutes(lastSevenArray[i].HoursTotal);
    }
    return minutesArray.reverse();
}
function getSummary(name, isCurrencySummary, updateGUI) {
    var addc = "";
    if (isCurrencySummary) {
        addc = "c";
    }
    $.getJSON("../" + addc + "Summary/" + encodeURIComponent(name))
            .done(function (json) {
                if (typeof json.Expenditure !== 'undefined') {//This will be false if the Task name itself is "Last"
                    WeekMinutes = getWeekMinutes(json.LastSeven);
                    if (updateGUI) {
                        DayTotalMinutes = json.LastSeven[0].DayTotal / 60;
                        HoursTotalMinutes = getArrayMinutes(json.LastSeven[0].HoursTotal);
                        HoursTotalMinutesWeek = getArrayMinutesWeek(json.LastSeven);
                        drawSummaryToday(DayTotalMinutes);
                        drawScheduleTable(HoursTotalMinutes);
                        drawScheduleTableWeek(HoursTotalMinutesWeek);
                        drawSummaryWeek(WeekMinutes);
                        var reportname = json.Report.toString();
                        reportname = reportname.substring(0, Math.min(15, reportname.length));
                        jQuery("#tk_nam").html(reportname);
                    } else {
                        listOfSeven[name] = WeekMinutes;
                        listOfData[name] = json.Data;
                        listOfReady[name] = true;
                        prepOverviewGraph();
                    }
                } else {
                    if (updateGUI) {
                        toastr.warning("Summary Not Found");
                        openTaskList();
                    } else {
                        listOfSeven[name] = [0, 0, 0, 0, 0, 0, 0];
                        listOfData[name] = [];
                        listOfReady[name] = true;
                        prepOverviewGraph();
                    }

                }
            })
            .fail(function (jqxhr, textStatus, error) {
                var err = textStatus + ", " + error;
                console.log("Request Failed: " + err);
                if (updateGUI) {
                    toastr.error("Failed: Graph Acquistion");
                } else {
                    toastr.error("Failed: Data Acquistion");
                    listOfSeven[name] = [0, 0, 0, 0, 0, 0, 0];
                    listOfData[name] = [];
                    listOfReady[name] = true;
                    prepOverviewGraph();
                }
            });
}
function tkGetTKVal() {
    if (tkTimeValueEnable) {
        val = tkSliderClassType.bootstrapSlider('getValue');
        if (val === 1) {
            return "-5";
        } else if (val === 2) {
            return "-1";
        } else {
            return "1";
        }
    } else {
        return "0";
    }
}
function addTrack(name) {
    $.getJSON("../pTrack/" + encodeURIComponent(name), {tv: tkGetTKVal()})
            .done(function (json) {
                if (typeof json.Log !== 'undefined') {
                    $("#tf_act").text(json.Log);
                    console.log("JSON Data: " + json.Log + json.Start);
                    tkStartTime = Date.now();
                    tkTimeEnable = true;
                }
            })
            .fail(function (jqxhr, textStatus, error) {
                var err = textStatus + ", " + error;
                console.log("Request Failed: " + err);
                toastr.error("Failed");
//                alert("Failed");
            });
}
function addTask() {
    $.getJSON("../pTask/" + encodeURIComponent(jQuery("#tk_txt").val()))
            .done(function (json) {
                if (typeof json.Log !== 'undefined') {
                    jQuery("#tk_txt").val("");
                    $("#tk_lis").prepend(taskHTML(json.Log));
                    console.log("JSON Data: " + json.Log);
                }
            })
            .fail(function (jqxhr, textStatus, error) {
                var err = textStatus + ", " + error;
                console.log("Request Failed: " + err);
                toastr.error("Failed");
                //                alert("Failed");
            });
}
function destroyTask() {
    $.getJSON("../dTask/All")
            .done(function (json) {
                emptyTaskList();
                toastr.success("List Destroyed");
            })
            .fail(function (jqxhr, textStatus, error) {
                var err = textStatus + ", " + error;
                console.log("Request Failed: " + err);
                toastr.error("Failed");
//                alert("Failed");
            });
}
function destroySummary() {
    $.getJSON("../dSummary/All")
            .done(function (json) {
                openTaskList();
                tkTimeEnable = false;
                $("#tf_act").text("Task Name");
                toastr.success("Logs Destroyed");
            })
            .fail(function (jqxhr, textStatus, error) {
                var err = textStatus + ", " + error;
                console.log("Request Failed: " + err);
                toastr.error("Failed");
//                alert("Failed");
            });
}
function emptyTaskList() {
    $("#tk_lis").html("");
}
function addTaskList(name) {
    $("#tk_lis").append(taskHTML(name));
}
function remTaskList(tk_current_id) {
    $("#tk_lis_" + tk_current_id).remove();
}
function taskHTML(name) {
    tkMaxID += 1;  //WILL RUN INTO PROBLEMS AT 1000  
    var nexttkID = ('000' + tkMaxID).substr(-3);

    return `<li id="tk_lis_${nexttkID}">
                                                <small class="btn-sm btn-primary tk_ply" id="tk_ply_${nexttkID}"><i class="fa fa-play"></i></small>
                                                <!-- drag handle -->
                                                <span class="handle">
                                                    <i class="fas fa-ellipsis-v"></i>
                                                    <!--<i class="fas fa-ellipsis-v"></i>-->
                                                </span>

                                                <!-- todo text -->
                                                <span class="text tk_tsk" id="tk_tsk_${nexttkID}">${name}</span>
                                                <!-- Emphasis label -->
                                                <small class="badge tk_inv" id="tk_bad_${nexttkID}"><i class="far fa-clock"></i> <strong id="tk_bge_${nexttkID}"></strong></small>
                                                <!-- General tools such as edit or delete-->
                                                <div class="tools">
                                                    <a id="tk_tag_${nexttkID}" rel="popover" tabindex="0" class="btn btn-xs btn-danger" role="button"><i class="fas fa-clock tk_tag"></i></a>
                                                    <i class="fas fa-chart-bar tk_bar" id="tk_bar_${nexttkID}"></i>
                                                    <i class="fas fa-trash tk_del" id="tk_del_${nexttkID}"></i>
                                                </div>
                                            </li>`;
    return `<li id="tk_lis_${nexttkID}">
                                                <small class="btn-sm btn-primary tk_ply" id="tk_ply_${nexttkID}"><i class="fa fa-play"></i></small>
                                                <!-- drag handle -->
                                                <span class="handle">
                                                    <i class="fas fa-ellipsis-v"></i>
                                                    <!--<i class="fas fa-ellipsis-v"></i>-->
                                                </span>
                                                
                                                <!-- todo text -->
                                                <span class="text tk_tsk" id="tk_tsk_${nexttkID}">${name}</span>
                                                <!-- Emphasis label -->
                                                <!--<small class="badge badge-danger"><i class="far fa-clock"></i>1</small>-->
                                                <!-- General tools such as edit or delete-->
                                                <div class="tools">
                                                    <i class="fas fa-clock"></i>
                                                    <i class="fas fa-chart-bar"></i>
                                                    <i class="fas fa-trash"></i>
                                                </div>
                                            </li>
<a  rel="popover" tabindex="0" class="btn btn-lg btn-danger" role="button">Dismissible popover</a>
<button type="button" >Click to toggle popover</button>
`;
    `<li>
                                                <!-- drag handle -->
                                                <span class="handle">
                                                    <i class="fas fa-ellipsis-v"></i>
                                                    <i class="fas fa-ellipsis-v"></i>
                                                </span>
                                                <!-- checkbox -->
                                                <div  class="icheck-primary d-inline ml-2">
                                                    <input type="checkbox" value="" name="todo1" id="todoCheck1">
                                                    <label for="todoCheck1"></label>
                                                </div>
                                                <!-- todo text -->
                                                <span class="text">${name}<i class="fas fa-circle-notch fa-spin"></i></span>
                                                <!-- Emphasis label -->
                                                <small class="badge badge-danger"><i class="far fa-clock"></i>1</small>
                                                <!-- General tools such as edit or delete-->
                                                <div class="tools">
                                                    <i class="fas fa-edit"></i>
                                                    <i class="fas fa-trash-o"></i>
                                                </div>
                                            </li>
                                            `;
}
function getTask() {
    $.getJSON("../Task/All")
            .done(function (json) {
                if ((typeof json.Data !== 'undefined') && json.Data !== "Dead") {
                    emptyTaskList();
                    $.each(json.Data, function (i, task) {
                        if (i === 20) {
                            return false;
                        }
                        addTaskList(task.Log);
                        console.log(i + ": " + task.Log);
                    });
                } else {
                    console.log("Couldn't Parse Response Properly");
                }
            })
            .fail(function (jqxhr, textStatus, error) {
                var err = textStatus + ", " + error;
                console.log("Request Failed: " + err);
                toastr.error("Couldn't Connect Properly");
//                alert("Couldn't Connect Properly");
            });
}
function openClassGoods(txt) {
    openSummary();
    getSummary(txt, true, true);
}
function reListen() {
    toastr.info('Version 0.0.4');
    emptyTaskList();
    getTask();
    getTrack();
    jQuery(document).on('click', '.tk_add', function () {
        addTask();

    });
    jQuery(document).on('click', '.tk_cgh', function () {
        openTaskList();

    });
    jQuery(document).on('keyup', '#tk_txt', function () {
        if (event.keyCode === 13) {
            addTask();
        }
    });
    jQuery(document).on('click', '.tk_ply', function () {
        var tk_current_id = tk_id(jQuery(this).attr('id'));
        if ((parseInt(tk_current_id) || 0) !== 0) {
            txt = jQuery("#tk_tsk_" + tk_current_id).text();
            console.log(txt);
            addTrack(txt);
        } else {
            addTrack(jQuery("#tk_txt").val());
        }


    });
    jQuery(document).on('click', '.tk_dst', function () {
        destroyTask();
    });
    jQuery(document).on('click', '.tk_dty', function () {
        destroySummary();
    });
    jQuery(document).on('click', '.tk_del', function () {
        remTaskList(tk_id(jQuery(this).attr('id')));
    });
    jQuery(document).on('click', '.tk_bar', function () {
        var tk_current_id = tk_id(jQuery(this).attr('id'));
        var txt = jQuery("#tk_tsk_" + tk_current_id).text();
        openSummary();
        getSummary(txt, false, true);
    });
    jQuery(document).on('click', '.tk_spc', function () {
        var txt = jQuery(this).html().toString();
        openClassGoods(txt);
    });
    jQuery(document).on('click', '.tk_spb', function () {
        var txt = jQuery(this).data('openname').toString();
        openSummary();
        getSummary(txt, false, true);
    });
    
    jQuery(document).on('click', '.tk_cls', function () {
        var tk_current_id = tk_id(jQuery(this).attr('id'));
        openClassGoods(tk_current_id);
    });
    jQuery(document).on('click', '.tk_shg', function () {
        tkOverviewGraphTab();
    });
    jQuery(document).on('click', '.tk_sht', function () {
        tkOverviewTableTab();
    });
    jQuery(document).on('click', '.tk_ctg', function () {
        openOverview();
        prepOverview();
        tkOverviewGraphTab();
    });
    jQuery(document).on('click', '.tk_cta', function () {
        openOverview();
        prepOverview();
        tkOverviewTableTab();
    });
    jQuery(document).on('click', '.tk_stv', function () {
        tkTimeValueEnable = !tkTimeValueEnable;
        if (tkTimeValueEnable) {
            $('.tk_stv').html('Disable Time Value');
            tkSlideUpdateBackground();
        } else {
            $('.tk_stv').html('Enable Time Value');
            $(".main-footer").css("background-color", "#ffc107");
        }

    });
//    jQuery(document).on('click', '.tk_tag', function () {
//        alert('Tag');
//    });
    jQuery(document).on('mousedown', '.tk_tim', function (event) {
        tagPick(jQuery(this).html());
        $('.popover').remove();
    });
    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        var goToTabSTR = $(e.target).attr("href").toString();
        if (goToTabSTR.includes("day-chart")) {
            showCanvasDay();
        } else if (goToTabSTR.includes("week-chart")) {
            showCanvasWeek();
        }

    });
    popTag();
    setInterval(updateTimer, 1000);

    drawSummaryToday(0);
    drawSummaryWeek([1, 2, 3, 4, 5, 6, 7]);
    drawScheduleTable([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]);
    drawScheduleTableWeek([[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]]);
    showCanvasDay();

    tkSliderClassType = $('#tk_gdt').bootstrapSlider();

    $("#tk_gdt").on("slide", function (slideEvt) {
        if (tkTimeValueEnable) {
            if (slideEvt.value === 1) {
                $(".main-footer").css("background-color", "#dc3545");
            } else if (slideEvt.value === 2) {
                $(".main-footer").css("background-color", "#17a2b8");
            } else {
                $(".main-footer").css("background-color", "#28a745");
            }
        }
    });
    $("#tk_gdt").on("change", function () {
        tkSlideUpdateBackground();
    });
    tkSlideUpdateBackground();

    openTaskList();
}
function showCanvasWeek() {
    $("#canvas_schedule").parent().addClass("tk_inv");
    $("#canvas_schedule_week").parent().removeClass("tk_inv");
}
function showCanvasDay() {
    $("#canvas_schedule_week").parent().addClass("tk_inv");
    $("#canvas_schedule").parent().removeClass("tk_inv");
}
function tagPick(num) {
    if (jQuery.isNumeric(num)) {
        valueOrignal = $("#tk_bge_" + currPopID).html();
        if (jQuery.isNumeric(valueOrignal)) {
            currBadgeHolder[parseInt(valueOrignal) - 1] = "";
        }
        prevBadgeNum = currBadgeHolder[parseInt(num) - 1];
        if (jQuery.isNumeric(prevBadgeNum)) {
            $("#tk_bad_" + prevBadgeNum).addClass("tk_inv");
        }
        currBadgeHolder[parseInt(num) - 1] = currPopID;
        $("#tk_bad_" + currPopID).removeClass("tk_inv");
        $("#tk_bge_" + currPopID).html(num);
    }

    toastr.info(num);
}
function popTag() {
    var popOverSettings = {
        placement: 'bottom',
        container: 'body',
        html: true,
        selector: '[rel="popover"]', //Sepcify the selector here 
        content: function () {
            return $($("#tk_pop").html());
        },
        title: "Watch Tag"
    };
    jQuery(document).popover(popOverSettings).on("show.bs.popover", function (e) {
        // hide all other popovers
//                console.log(jQuery(e.target).attr("id"));
        currPopID = tk_id(jQuery(e.target).attr('id'));
//                $("[rel=popover]").not(e.target).popover("destroy");;
        $(".popover").remove();
    });
}
function updateTimer() {
    if (tkTimeEnable) {
        var seconds = Math.round((Date.now() - tkStartTime) / 1000); //in ms 
        var hours = ("0" + Math.floor(seconds / 3600)).slice(-2);
        seconds %= 3600;
        var minutes = ("0" + Math.floor(seconds / 60)).slice(-2);
        seconds = seconds % 60;
        seconds = ("0" + seconds).slice(-2);
        jQuery("#tf_tim").text(hours + ":" + minutes + ":" + seconds);
    }
}
jQuery(document).ready(function () {
    reListen();


});
