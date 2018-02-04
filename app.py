from flask import Flask
from flask import request, render_template, url_for
from src.html_to_table import HTMLTableParser
from icsGenerator import generateics
# from ics import Calendar
# from urllib2 import urlopen
import sys
app = Flask(__name__)


@app.route('/convert', methods = ['POST'])
def hello():
    print(request, file=sys.stderr)
    print(request.form, file=sys.stderr)
    num = 8
    courses = []
    courses.append(request.form['course1'])
    courses.append(request.form['course2'])
    courses.append(request.form['course3'])
    courses.append(request.form['course4'])
    courses.append(request.form['course5'])
    courses.append(request.form['course6'])
    courses.append(request.form['course7'])
    courses.append(request.form['course8'])

    names = []
    names.append(request.form['name1'])
    names.append(request.form['name2'])
    names.append(request.form['name3'])
    names.append(request.form['name4'])
    names.append(request.form['name5'])
    names.append(request.form['name6'])
    names.append(request.form['name7'])
    names.append(request.form['name8'])

    dates = []
    dates.append(request.form['month1'] + ' ' + request.form['year1'])
    dates.append(request.form['month2'] + ' ' + request.form['year2'])
    dates.append(request.form['month3'] + ' ' + request.form['year3'])
    dates.append(request.form['month4'] + ' ' +  request.form['year4'])
    dates.append(request.form['month5'] + ' ' +  request.form['year5'])
    dates.append(request.form['month6'] + ' ' +  request.form['year6'])
    dates.append(request.form['month7'] + ' ' +  request.form['year7'])
    dates.append(request.form['month8'] + ' ' +  request.form['year8'])

    print(courses, file=sys.stderr)
    print(dates, file=sys.stderr)
    print(names, file=sys.stderr)

    hp = HTMLTableParser()
    count = 0
    with open('events.txt','w') as f:
        pass

    for i in range(num):
        if courses[i] != '':
            with open('events.txt','a') as f:
                f.write(names[i] + '\n')
                f.write(dates[i] + '\n')
            success = hp.parse_url(courses[i])
            if success:
                count += 1

    print("Successfully converted {} pdf(s)!".format(count), file=sys.stderr)
    generateics()

    filename = 'deadlines.ics'
    text = ''
    with open(filename, 'r') as cal:
        text = "<br />".join(cal.readlines())

    f = open('templates/page.html','w')
    url = url_for('static', filename=filename)
    message = """<!DOCTYPE html>
              <html>
              <div>""" + text + """ </div>

              </html>"""

    # msg = <a href="""+url+"""> Download</a> </div>
    f.write(message)
    print("wrote", file=sys.stderr)
    f.close()
    print("rendering...", file=sys.stderr)

    return render_template('page.html')

if __name__ == '__main__':
    app.run(host='https://stark-waters-86085.herokuapp.com/')
    # app.run(debug=True, host='localhost',port=4041)
