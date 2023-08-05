from flask import Flask, request, send_from_directory, make_response  # Import Flask
from flask_restful import Resource, Api
from flask_swagger_ui import get_swaggerui_blueprint
import time, copy # Import Time, Copy
from datetime import datetime, timedelta
app = Flask(__name__)  # Init Flask + API
api = Api(app)

# Swagger Code
@app.route('/swag/<path:path>')
def send_js(path):
    return send_from_directory('swag', path)
swaggerui_blueprints = get_swaggerui_blueprint('/swagger', '/swag/swag.json', config={'app-name': 'TimeKeeper'})
app.register_blueprint(swaggerui_blueprints, url_prefix='/swagger')

@app.route('/ui/<path:path>')
def send_ui(path):
    return send_from_directory('ui', path)

# Dictionaries | Variables
TimeKeeper = []  # Log Dictionary
TaskKeeper = []  # Task Dictionary
simpleResponse = False  # Text or JSON Response
def isWatch():
    if ("ESP32" in request.headers.get('User-Agent') or simpleResponse):
        return True
    else:
        return False

def txtresponse(resp):  # Set Headers to Text for simple Responses
    response = make_response(resp, 200)
    response.mimetype = "text/plain"
    return response
def timeelapsed(sec):  # Formatted Time Elapsed
    return time.strftime("%H:%M:%S", time.gmtime(sec))
def dayelapsed(sec):  # Formatted Days Elapsed
    return int(time.strftime("%j", time.gmtime(sec)))
def displog(reports):  # Returns Formatted Time Log
    logged = reports.copy()
    if 'Stop' in logged:  # Calculates Time and Prettify
        logged['Duration'] = timeelapsed(logged['Stop'] - logged['Start'])
        logged['Stop'] = time.ctime(logged['Stop'])
    else:
        logged['Elapsed'] = timeelapsed(time.time() - logged['Start'])
    logged['Start'] = time.ctime(logged['Start'])  # NOTE: THIS IS INTENTIONALLY OUTSIDE THE ELSE BLOCK
    return logged
def pTrack(name):  # Creates a New Log and Ends Previous Log if it's continuing.
    if len(TimeKeeper) != 0:
        if not ('Stop' in TimeKeeper[-1]):
            TimeKeeper[-1]['Stop'] = time.time()

    if (len(TaskKeeper) != 0) and name.isnumeric() and (int(name) < (len(TaskKeeper) )):
        if int(name) < 0:
            name = "Watch Log"
        else:
            index=(0-1-int(name))
            name=TaskKeeper[index]['Log']
    timevalueGET = request.args.get('tv') # Attempt to Get Time Value
    timevalueGET = '-1' if ((timevalueGET is None) or (not (timevalueGET.lstrip('-').isdigit()))) else str(int(timevalueGET)) # Set TimeValue = -1 if Failed to Get Time Value
    Tem = {'Log': name, 'Summary': 'http://127.0.0.1:5000/Summary/' + name, 'Start': time.time(), 'TimeValue': timevalueGET}
    TimeKeeper.append(Tem.copy())
    Tem['Start'] = time.ctime(Tem['Start'])
    return txtresponse("1") if isWatch() else Tem
def dTrack(name):  # Stops Log with given Name
    for ind, x in enumerate(TimeKeeper):
        if x['Log'] == name:
            if not ('Stop' in x):
                x['Stop'] = time.time()
def Track(name):  # Gets the Last Log of Provided Name
    for reports in reversed(TimeKeeper):
        if reports['Log'] == name:
            return displog(reports)
    if len(TimeKeeper) != 0:
        return {"Log": TimeKeeper[-1]}
    else:
        return {"Log": "Dead"}
class CreateTracker(Resource):
    def __init__(self):
        pass
    def get(self, name):  # Gets the Last Log of Provided Name
        return Track(name)
    def post(self, name):  # Creates a New Log and Ends Previous Log if it's continuing.
        return pTrack(name)
    def delete(self, name):  # Stops Log with given Name
        dTrack(name)
class pCreateTracker(Resource):
    def __init__(self):
        pass
    def get(self, name):  #  Creates a New Log and Ends Previous Log if it's continuing.
        return pTrack(name)
class dCreateTracker(Resource):
    def __init__(self):
        pass
    def get(self, name): # Stops Log with given Name
        dTrack(name)
def dSummary(name):  # Clears Everything
    global TimeKeeper
    TimeKeeper = []
def Summary(name):   # Gets all the Logs of Provided Name
    FinalReport = []
    CompleteReport = []
    TotalDuration = 0
    HourData=[0 for col in range(24)] # 24 Hour BreakDown
    DayData = {'DayTotal': 0, 'HoursTotal': HourData} # Each Day BreakDown
    LastSevenDays=[copy.deepcopy(DayData) for col in range(7)] # Care only About Last 7 Days
    for reports in (TimeKeeper):
        logged = displog(reports)
        CompleteReport.append(logged)
        if reports['Log'] == name:
            FinalReport.append(logged)
            startTime = reports['Start']
            if 'Stop' in logged:
                stopTime = reports['Stop']
            else:
                stopTime = time.time()
            timeexpenditure = stopTime - startTime
            TotalDuration += timeexpenditure
            startDayAgo = dayelapsed(time.time() - startTime)-1
            stopDayAgo = dayelapsed(time.time() - stopTime) - 1
            if startDayAgo < 7:
                if startDayAgo == stopDayAgo:
                    LastSevenDays[startDayAgo]['DayTotal'] += timeexpenditure
                    dt = datetime.now() - timedelta(days=startDayAgo)
                    today = datetime(dt.year, dt.month, dt.day).timestamp()
                    startTime = startTime - today
                    stopTime = stopTime - today
                    currentHour = 0
                    while currentHour < 24:
                        currentHourSeconds = 60*60*currentHour
                        nextHourSeconds = 60*60*(currentHour+1)
                        if startTime <= currentHourSeconds:
                            if stopTime<=currentHourSeconds:
                                LastSevenDays[startDayAgo]['HoursTotal'][currentHour] += 0 # 0
                            else:#stopTime>currentHourSeconds
                                if stopTime>=nextHourSeconds:
                                    LastSevenDays[startDayAgo]['HoursTotal'][currentHour] += 60*60 #1
                                else: # stopTime<nextHourSeconds
                                    LastSevenDays[startDayAgo]['HoursTotal'][currentHour] += stopTime-currentHourSeconds
                        else: #startTime > currentHourSeconds
                            if startTime >= nextHourSeconds:
                                LastSevenDays[startDayAgo]['HoursTotal'][currentHour] += 0  # 0
                            else: #startTime< nextHourSeconds
                                if stopTime >= nextHourSeconds:
                                    LastSevenDays[startDayAgo]['HoursTotal'][currentHour] += nextHourSeconds - startTime
                                else: #stopTime < nextHourSeconds
                                    LastSevenDays[startDayAgo]['HoursTotal'][currentHour] += stopTime - startTime
                        currentHour += 1
                elif (startDayAgo+1) == stopDayAgo:
                    pass # May or may not implement later to add continuity
    if len(FinalReport) == 0:
        return CompleteReport
    else:
        return {"Expenditure": timeelapsed(TotalDuration), "LastSeven":LastSevenDays,"Report": name, "Data": FinalReport}
def cSummary(timevaluename):   # Gets all the Logs of Provided Class of Goods or Return General Summary
    FinalReport = [] # Same
    CompleteReport = [] # Same
    TotalDuration = 0 # Different Not REAL TOTAL
    HourData=[0 for col in range(24)] # Same
    DayData = {'DayTotal': 0, 'HoursTotal': HourData} #Different Day Total/Hour Total Different
    LastSevenDays=[copy.deepcopy(DayData) for col in range(7)]
    for reports in (TimeKeeper): #For Loop Content Different
        logged = displog(reports) #Same
        CompleteReport.append(logged) #Same
        if timevaluename.lstrip('-').isdigit() and (reports['TimeValue'] == timevaluename): #Different Check
            startTime = reports['Start']
            if 'Stop' in logged:
                stopTime = reports['Stop']
            else:
                stopTime = time.time()
            timeexpenditure = stopTime - startTime
            if timeexpenditure >= (60*60): # New Conditon
                stopTime = stopTime - (timeexpenditure % (60*60))  # NEW STOP TIME
                timeexpenditure = stopTime - startTime # NEW RECALCULATE TIME EXPENDATURE
                FinalReport.append(logged)  # Different Location Previous Outside Condition
                TotalDuration += timeexpenditure
                startDayAgo = dayelapsed(time.time() - startTime)-1
                stopDayAgo = dayelapsed(time.time() - stopTime) - 1
                if startDayAgo < 7:
                    if startDayAgo == stopDayAgo:
                        LastSevenDays[startDayAgo]['DayTotal'] += timeexpenditure
                        dt = datetime.now() - timedelta(days=startDayAgo)
                        today = datetime(dt.year, dt.month, dt.day).timestamp()
                        startTime = startTime - today
                        stopTime = stopTime - today
                        currentHour = 0
                        while currentHour < 24:
                            currentHourSeconds = 60*60*currentHour
                            nextHourSeconds = 60*60*(currentHour+1)
                            if startTime <= currentHourSeconds:
                                if stopTime<=currentHourSeconds:
                                    LastSevenDays[startDayAgo]['HoursTotal'][currentHour] += 0 # 0
                                else:#stopTime>currentHourSeconds
                                    if stopTime>=nextHourSeconds:
                                        LastSevenDays[startDayAgo]['HoursTotal'][currentHour] += 60*60 #1
                                    else: # stopTime<nextHourSeconds
                                        LastSevenDays[startDayAgo]['HoursTotal'][currentHour] += stopTime-currentHourSeconds
                            else: #startTime > currentHourSeconds
                                if startTime >= nextHourSeconds:
                                    LastSevenDays[startDayAgo]['HoursTotal'][currentHour] += 0  # 0
                                else: #startTime< nextHourSeconds
                                    if stopTime >= nextHourSeconds:
                                        LastSevenDays[startDayAgo]['HoursTotal'][currentHour] += nextHourSeconds - startTime
                                    else: #stopTime < nextHourSeconds
                                        LastSevenDays[startDayAgo]['HoursTotal'][currentHour] += stopTime - startTime
                            currentHour += 1
                    elif (startDayAgo+1) == stopDayAgo:
                        pass

    if len(FinalReport) == 0:
        return CompleteReport
    else:
        return {"Expenditure": timeelapsed(TotalDuration), "TimeValueFlow": (int((TotalDuration/3600)*int(timevaluename))), "LastSeven":LastSevenDays,"Report": timevaluename, "Data": FinalReport }

class SummaryReport(Resource):
    def __init__(self):
        pass
    def get(self, name):  # Gets all the Logs of Provided Name
        return Summary(name)
    def delete(self, name):  # Clears Everything
        dSummary(name)
class dSummaryReport(Resource):
    def __init__(self):
        pass
    def get(self, name):  # Clears Everything
        dSummary(name)
class cSummaryReport(Resource):
    def __init__(self):
        pass
    def get(self, name):  # Gets all the Logs of Provided Nameg
        return cSummary(name)
def pTask(name): # Adds New Task
    Tem = {'Log': (name[:17] + '..') if len(name) > 17 else name}
    TaskKeeper.append(Tem.copy())
    return txtresponse("1") if isWatch() else Tem
def dTask(name):  # Clears Everything
    global TaskKeeper
    TaskKeeper = []
def Task(name): # Gets the last n task names. Default n = 30
    TaskReversed = []
    TaskSimple = ""
    maxTask = int(name) if name.isnumeric() else 30
    curTask = 0
    for report in reversed(TaskKeeper):
        curTask += 1
        if curTask > maxTask:
            break
        if isWatch():
            TaskSimple += report['Log'] + " " * (19 - len(report['Log'])) + "\n"
        else:
            TaskReversed.append(report)
    if len(TaskKeeper) != 0:
        return txtresponse(TaskSimple.rstrip('\n')) if isWatch() else {"Data": TaskReversed}
    else:
        return txtresponse("0") if isWatch() else {"Data": "Dead"}

class TaskList(Resource):
    def __init__(self):
        pass
    def get(self, name):  # Gets the last n task names. Default n = 30
        return Task(name)
    def post(self, name):  # Adds New Task
        return pTask(name)
    def delete(self, name):  # Clears Everything
        dTask(name)
        if isWatch():
            return txtresponse("1")
class pTaskList(Resource):
    def __init__(self):
        pass
    def get(self, name):  # Adds New Task
        return pTask(name)
class dTaskList(Resource):
    def __init__(self):
        pass
    def get(self, name):  # Clears Everything
        dTask(name)
        if isWatch():
            return txtresponse("1")

api.add_resource(CreateTracker, '/Track/<string:name>')
api.add_resource(pCreateTracker, '/pTrack/<string:name>')
api.add_resource(dCreateTracker, '/dTrack/<string:name>')


api.add_resource(SummaryReport, '/Summary/<string:name>')
api.add_resource(dSummaryReport, '/dSummary/<string:name>')
api.add_resource(cSummaryReport, '/cSummary/<string:name>')

api.add_resource(TaskList, '/Task/<string:name>')
api.add_resource(pTaskList, '/pTask/<string:name>')
api.add_resource(dTaskList, '/dTask/<string:name>')

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
