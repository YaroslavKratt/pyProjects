import json
from scipy import interpolate
import matplotlib.pyplot as plt


jsonFile=open("737-505-20k_Page_063.json","r")
parsedJson=json.loads(jsonFile.read())
curves=parsedJson[0]["curves"]
nx=[]
ny=[]
tagValue=[]
pointsOfOneCurve=[]
allCurvePoints=[]
onePoint=[]
z=[]
for i in range(len(curves)):
     points = curves[i]["points"]
     pointsOfOneCurve=[]
     for j in range(len(points)):
          nx.append(points[j]["nx"])
          ny.append(points[j]["ny"])
          tagValue.append(int(curves[i]["tagvalue"]))
          if int(curves[i]["tagvalue"]) not in z:
              z.append(int(curves[i]["tagvalue"]))
          onePoint=[points[j]["nx"],points[j]["ny"]]
          pointsOfOneCurve.append(onePoint)
     allCurvePoints.append(pointsOfOneCurve)

def linInerpOnInterval(X,x,y):
    if X<x[0]:
       Y= y[0] + (y[1] - y[0]) / (x[1] - x[0]) * (X - x[0])
       return Y
    else:
        if X>x[len(x)-1]:
            Y=y[len(x)-2] + (y[len(x)-1] - y[len(x)-2]) / (x[len(x)-2] - x[len(x)-1]) * (X - x[len(x)-1])
            return Y
        else:
            for i in range(len(x)):
                if X>=x[i] and X<=x[i+1] and i<len(x)-1:
                   Y= y[i] + (y[i+1] - y[i]) / (x[i+1] - x[i]) * (X - x[i])

    return Y


def twoDLinearInterpolation(X, Y, curves, value, ):
    interpolatedY=[]
    x=[]
    y=[]
    for i in range(len(curves)):
        xOfOneCurve=[]
        yOfOneCurve=[]
        for j in range(len(curves[i])):
            xx=curves[i][j][0]
            yy=curves[i][j][1]
            xOfOneCurve.append(xx)
            yOfOneCurve.append(yy)
        plt.plot(xOfOneCurve, yOfOneCurve)
        plt.axis([28000,56000,-60, 60])
        plt.scatter(xOfOneCurve, yOfOneCurve, edgecolors='r', s=10)
        plt.grid()
        x.append(xOfOneCurve)
        y.append(yOfOneCurve)
    plt.show()

    for i in range(len(curves)):
                interpolatedY.append(linInerpOnInterval(X,x[i],y[i]))
    plt.plot(interpolatedY, value)
    plt.axis([-60, 60, -1000, 10000])
    plt.scatter(interpolatedY,value, edgecolors='r', s=10)
    plt.grid()
    plt.show()
    tempArr=zip(interpolatedY,value)
    sortedArr = sorted(tempArr, key=lambda tup: tup[0])
    interpolatedY= [x[0] for x in sortedArr]
    print(interpolatedY)

    value = [x[1] for x in sortedArr]
    print(value)
    return linInerpOnInterval(Y,interpolatedY,value)

print(twoDLinearInterpolation(43000,40,allCurvePoints,z))
f = interpolate.interp2d(nx, ny, tagValue, kind='linear')
print(f(43000, 40))



