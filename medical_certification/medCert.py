from dateutil.relativedelta import relativedelta
from datetime import date
from datetime import timedelta
requirements={"Class1":{"Common Exam":{"age":[{'range': (1, 60), 'span': 12}, {'range': (60, 100), 'span': 6} ]},#до 60 - +12мес, от 60 - +6 мес
                        "ECG":{"age": [{'range': (1, 30), 'span': 60}, {'range': (30, 40), 'span': 24},{'range': (40, 50), 'span': 12},{'range': (50, 60), 'span': 12}, {'range': (60, 100), 'span': 6}]
                        },
                        "Oculist":{"age":[{'range': (1, 60), 'span': 12}, {'range': (60, 100), 'span': 6} ]},
                        "Audio":{"age":[{'range': (1, 40), 'span': 60},{'range': (40, 100), 'span': 24}]}

                        },
              "Class1 OnePilot":{"Common Exam":{"age":[{'range': (1, 40), 'span': 12}, {'range': (40, 100), 'span': 6}] },
                        "ECG":{"age":[{'range': (1, 30), 'span': 60},{'range': (30, 40), 'span': 24},{'range': (40, 50), 'span': 12},{'range': (50, 60), 'span': 12},{'range': (60, 100), 'span': 6}]
                               },
                        "Oculist":{"age":[{'range': (1, 60), 'span': 12}, {'range': (60, 100), 'span': 6} ]},
                        "Audio":{"age":[{'range': (1, 40), 'span': 60},{'range': (40, 100), 'span': 24}]}
                        },
              "Class2":{"Common Exam":{"age":[{'range': (1, 40), 'span': 60}, {'range': (40, 50), 'span': 24},{'range': (50, 100), 'span': 12}]},
                        "ECG":{"age":[{'range': (40, 50) , 'span': 60},{'range': (50, 100), 'span': 24}]
                               },
                        "Oculist":{"age":[{'range': (1, 40), 'span': 60}, {'range': (40, 50), 'span': 24},{'range': (50, 100), 'span': 12}]},
                        "Audio": {"age": [{'range': (1, 40), 'span': 60}, {'range': (40, 100), 'span': 24}]}

                        },
              "Steward": {"Common Exam": {"age": [{'range': (1, 100), 'span': 60}]},
                         "ECG": {"age": [{'range': (40, 50), 'span': 60}, {'range': (50, 100), 'span': 24}]},
                         "Oculist": {"age": [{'range': (1, 100), 'span': 60}]},
                         "Audio":{"age":None},
                         }
              }

def getDatesOfNextMedicalExam(requirements, speciality,  lastDates, birthday):
    nextDates={}
    nextDates.update({"Common Exam":getNextDate(requirements, speciality, lastDates.get("Common Exam"),"Common Exam",birthday)})
    nextDates.update({"ECG":getNextDate(requirements, speciality, lastDates.get("ECG"),"ECG",birthday)})
    nextDates.update({"Oculist":getNextDate(requirements, speciality, lastDates.get("Oculist"),"Oculist",birthday)})
    nextDates.update({"Audio":getNextDate(requirements, speciality,  lastDates.get("Audio"),"Audio",birthday)})
    return nextDates
def returnDate(birthday, dateOfExam,rangeAndSpan):
    age=relativedelta(dateOfExam,birthday)
    rangeAndSpan
    if rangeAndSpan == None:
        return None
    for i, value in enumerate(rangeAndSpan):
        startOfRange=value.get("range")[0]
        endOfRange=value.get("range")[len(value.get("range"))-1]
        span=value.get("span")
        if age.years >= startOfRange and age.years < endOfRange:
            if age.years*12+age.months+span<endOfRange*12:
                return dateOfExam+relativedelta(months=span)
            else:
                if age.years*12+age.months+span>endOfRange*12+rangeAndSpan[i+1].get("span"):
                    span = endOfRange * 12 - age.years * 12 - age.months + rangeAndSpan[i + 1].get("span")
                    return dateOfExam + relativedelta(months=+span)
                else:
                    return dateOfExam+relativedelta(months=+span)




def getNextDate(requirements, speciality, lastDateOfExam,examName,birthday):
    rangeAndSpan=requirements.get(speciality).get(examName).get("age")
    if  rangeAndSpan==None:
        return None
    if returnDate(birthday, lastDateOfExam, rangeAndSpan)==None or returnDate(birthday,lastDateOfExam,rangeAndSpan)==None :
        return None
    if returnDate(birthday, lastDateOfExam,rangeAndSpan)<=date.today():
        return returnDate(birthday,date.today(),rangeAndSpan)
    else:
        return returnDate(birthday,lastDateOfExam,rangeAndSpan)

def mainTest(requirements, speciality, lastDateOfExam,examName,birthday):

    if requirements.get(speciality).get(examName) == None:
        return None
    rangeAndSpan = requirements.get(speciality).get(examName).get("age")

    if returnDate(birthday, lastDateOfExam, rangeAndSpan) == None or returnDate(birthday, lastDateOfExam, rangeAndSpan) == None:
        return None

    if returnDate(birthday, lastDateOfExam,rangeAndSpan)<=date.today():
        test(date.today(), birthday, returnDate(birthday, date.today(), rangeAndSpan), speciality, examName)
    else:
        test(lastDateOfExam, birthday, returnDate(birthday, lastDateOfExam, rangeAndSpan), speciality, examName)

def test(date,birthday,nextDate,speciality,examName):
    age = relativedelta(date,birthday)
    rangeAndSpan=requirements.get(speciality).get(examName).get("age")

    for i, value in enumerate(rangeAndSpan):
        startOfRange=value.get("range")[0]
        endOfRange=value.get("range")[len(value.get("range"))-1]
        span=value.get("span")
        if age.years >= startOfRange and age.years < endOfRange:
            if age.years*12+age.months+span<endOfRange*12:
                if relativedelta(nextDate,date).years*12+relativedelta(nextDate,date).months!=span:
                    print("Error, check 1 if")
                    print(relativedelta(nextDate, date).years * 12 + relativedelta(nextDate, date).months)

                else:
                    print(" OK 1")
                    print("Span= " + str(span))



            else:
                if age.years*12+age.months+span>endOfRange*12+rangeAndSpan[i+1].get("span"):
                    span = endOfRange * 12 - (age.years * 12 + age.months) + rangeAndSpan[i + 1].get("span")
                    if relativedelta(nextDate, date).years * 12 + relativedelta(nextDate, date).months != span:
                        print("Error, check 2 if")
                        print(relativedelta(nextDate, date).years * 12 + relativedelta(nextDate, date).months)
                    else:
                        print("OK 2")
                        print("Span= " + str(span))



                else:
                    if relativedelta(nextDate, date).years * 12 + relativedelta(nextDate, date).months != span:
                        print("Error, check 3 if")
                        print(relativedelta(nextDate, date).years * 12 + relativedelta(nextDate, date).months)

                    else:
                        print("OK 3")
                        print("Span= " + str(span))



lastDates={"Common Exam":date(2016, 4, 1),"ECG":date(2016, 1, 14),"Oculist":date(2017, 1, 14),"Audio":date(2018, 4,3 )}
birthday=date(1978, 4, 4)
'''print("now he/she is " + str((relativedelta(date.today(), birthday).years)) + "years old")
print("now he/she is " + str(
    (relativedelta(date.today(), birthday).years * 12 + relativedelta(date.today(), birthday).months)) + "months old")
print("at last visit he/she was " + str((relativedelta(lastDates.get("ECG"), birthday).years)) + " years old")
print("at last visit he/she was " + str((relativedelta(lastDates.get("ECG"), birthday).years * 12 + relativedelta(
    lastDates.get("ECG"), birthday).months)) + " months old")
print(returnDate(birthday, date(2018, 1, 14),requirements.get("Class1").get("ECG").get("age")))
'''

for i in requirements:
    print("                                   "+i)
    print()
    print(getDatesOfNextMedicalExam(requirements,i, lastDates, birthday))
    for j in requirements.get(i):
        print("          "+j)
        print("now he/she is " + str((relativedelta(date.today(), birthday).years)) + "years old")
        print("now he/she is " + str((relativedelta(date.today(), birthday).years * 12 + relativedelta(date.today(),birthday).months)) + "months old")
        print("at last visit he/she was " + str((relativedelta(lastDates.get(j), birthday).years)) + " years old")
        print("at last visit he/she was " + str((relativedelta(lastDates.get(j),birthday).years * 12 + relativedelta( lastDates.get(j), birthday).months)) + " months old")
        mainTest(requirements, i,lastDates.get(j),j,birthday)






