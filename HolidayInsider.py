from flask import Flask
import os
from datetime import datetime
from flask import request, render_template
import holidays

app = Flask(__name__)




@app.route('/')
def loadIndex():
    try:
        locationVariable = "c:/users/soham shah/anaconda3/envs/conda_holidays/lib/site-packages/"

        countries = [name.split(".py")[0].replace("_", " ") for name in
                     os.listdir(locationVariable + "holidays/countries/") if
                     name.endswith(".py") and not name.startswith("__")]

        # print(countries)
        return render_template("index.html", countries=countries)
    except Exception as ex:
        print(ex)




@app.route("/country/viewHoliday" , methods=["POST"])
def viewHolidaybyCountry():
    try:
        currentYear = datetime.now()
        selectedCountryName = request.form['countryName']
        selectedCountryName = selectedCountryName.title().replace(" ", "")
        print(selectedCountryName)
        specific_holiday = getattr(holidays, selectedCountryName)(years=currentYear.year).items()

        holidayList = list(specific_holiday)


        return render_template("viewHolidays.html",selectedCountryName=selectedCountryName ,
                               currentYear=currentYear,holidayList=holidayList )

    except Exception as ex:
        print(ex)
        return render_template("index.html")


@app.route("/country/viewHolidaybyMonth" , methods=["POST"])
def viewHolidaybyMonth():
    try:
        selectedCountryName = request.form['countryName']
        selectedMonth = request.form['month']
        selectedMonth = selectedMonth[-2:]
        currentYear = datetime.now()

        selectedCountryName = selectedCountryName.title().replace(" ", "")
        print(selectedCountryName)
        print(selectedMonth)

        specific_holiday = getattr(holidays, selectedCountryName)(years=currentYear.year).items()

        holidayList = list(specific_holiday)
        print(holidayList)

        monthHoliday = []
        for i in holidayList:
            print(i)
            for datetimeong in i:
                print(type(datetimeong), datetimeong)
                holidayMonths = datetimeong.strftime("%m")
                print("month:", holidayMonths, type(holidayMonths))

                if holidayMonths == selectedMonth:
                    print("month-matched")
                    monthHoliday.append(i)
                    # print(monthHoliday)
                    break

                else:
                    print("month not matched")
                    break

        print("month-holiday------------------",monthHoliday)

        if len(monthHoliday) != 0:
            return render_template("viewHolidaysbyMonth.html", holidayList=monthHoliday, currentYear=currentYear,
                                   selectedCountryName=selectedCountryName , selectedMonth = selectedMonth)

        else:
            msg="Please select other month and load index page"
            return render_template("index.html" , msg=msg)





    except Exception as ex:
        print(ex)
        return render_template("index.html")




if __name__ == '__main__':
    app.run(debug=True)
