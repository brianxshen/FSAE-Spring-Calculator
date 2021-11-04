import numpy as np
import matplotlib.pyplot as plt

cgDistribution = 0.535 # rear percent
aeroDistribution = 0.57 # rear percent
sprungWeight = 540 # lbs
springRateFront = 450
springRateRear = 600
tireRateFront = 650
tireRateRear = 650
maxSpringCompression = 1.97 # inches: 50mm
motionRatioFront = 1.02**2 # spring travel / wheel travel
motionRatioRear = 1**2
wheelRateFront = springRateFront*motionRatioFront
wheelRateRear = springRateRear*motionRatioRear
rideRateFront = (tireRateFront*wheelRateFront)/(tireRateFront+(wheelRateFront))#kT*kW/kT+kW
rideRateRear = (tireRateRear*wheelRateRear)/(tireRateRear+(wheelRateRear))

# add anti dive & anti squat
# use slopes and calculate intersection
cgHeight = 1 # inches
hardpoints = np.array([[1662.67,286.09,158.743], # Lower wishbone front pivot
                      [1993.51,237.98,115.613], # Lower wishbone rear pivot
                      [1872.184,540.552,131.553], # Lower wishbone outer ball joint 
                      [1729.116,290.0,276.839], # Upper wishbone front pivot
                      [1996.21,290.435,257.662], # Upper wishbone rear pivot
                      [1879.975,531.778,324.838]]) # Upper wishbone outer ball joint
wheelCenter = np.array([1870.8051,610.076,228.573])
# x: left right, y: in out, z: up down
hardpointsDelta = np.array([wheelCenter-hardpoints[0], # wheel center 0,0,0
                            wheelCenter-hardpoints[1],
                            wheelCenter-hardpoints[2],
                            wheelCenter-hardpoints[3],
                            wheelCenter-hardpoints[4],
                            wheelCenter-hardpoints[5]])

averageDF = 150
maxDF = 600

wheelbase = 61
averageSpeed = 35 # mph

def cornerWeight(cgD,aeroD,DF):
  return (sprungWeight*cgD/2)+(DF*aeroD/2)

def downforceWeight(aeroD,DF):
  return (DF*aeroD/2)

def naturalFreq(springRate,cgD,aeroD):
  return (np.sqrt(springRate*12/(cornerWeight(cgD,aeroD,averageDF)/32.2))/(2*np.pi))

def totalDroop():
  return [cornerWeight(1-cgDistribution,1-aeroDistribution,maxDF)/wheelRateFront,
  cornerWeight(cgDistribution,aeroDistribution,maxDF)/wheelRateRear]

def downforceDroop(): 
  return [downforceWeight(1-aeroDistribution,averageDF)/rideRateFront,
  downforceWeight(aeroDistribution,averageDF)/rideRateRear,
  downforceWeight(1-aeroDistribution,maxDF)/rideRateFront,
  downforceWeight(aeroDistribution,maxDF)/rideRateRear]

def antiPercent(vDist,hDist):
  return (vDist/hDist)/(cgHeight/wheelbase)

totalDroopList = totalDroop()
downforceDroopList = downforceDroop()
print('Spring Rate (F/R): ' + str('{0:.3g}'.format(springRateFront)) + ' lbs/in | ' + str('{0:.3g}'.format(springRateRear)) + ' lbs/in')
print('Ride Rate (F/R): ' + str('{0:.3g}'.format(rideRateFront)) + ' lbs/in | ' + str('{0:.3g}'.format(rideRateRear)) + ' lbs/in')
print('Downforce (Avg/Max): ' + str(averageDF) + ' lbs | ' + str(maxDF) + ' lbs')
print('Natural Frequency (F/R): ' + str('{0:.3g}'.format(naturalFreq(rideRateFront,1-cgDistribution,1-aeroDistribution))) + ' Hz | ' + str('{0:.3g}'.format(naturalFreq(rideRateRear,cgDistribution,aeroDistribution))) + ' Hz')
print('Avg. Droop (F/R): ' + str('{0:.3g}'.format(downforceDroopList[0])) + ' inches | ' + str('{0:.3g}'.format(downforceDroopList[1])) + ' inches')
print('Max Droop (F/R): ' + str('{0:.3g}'.format(downforceDroopList[2])) + ' inches | ' + str('{0:.3g}'.format(downforceDroopList[3])) + ' inches')
print('Max Spring Compression (F/R): ' + str('{0:.3g}'.format(totalDroopList[0])) + ' inches | ' + str('{0:.3g}'.format(totalDroopList[1])) + ' inches') 

x = np.linspace(0,1.5,100)

p = np.sin(naturalFreq(rideRateFront,1-cgDistribution,1-aeroDistribution) * x)
q = np.sin(naturalFreq(rideRateRear,cgDistribution,aeroDistribution) * x - (wheelbase/(averageSpeed*17.6)))

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
# ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('center')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.set_title('Ride Frequency (' + str(averageSpeed) + ' mph, ' + str(wheelbase) + ' in WB)')
ax.set_xlabel('Time (sec)')
ax.set_ylabel('Suspension Travel')

plt.plot(x,p, 'b-', label='Front Ride Rate: ' + str('{0:.3g}'.format(naturalFreq(rideRateFront,1-cgDistribution,1-aeroDistribution))) + ' Hz')
plt.plot(x,q, 'c-', label='Rear Ride Rate: ' + str('{0:.3g}'.format(naturalFreq(rideRateRear,cgDistribution,aeroDistribution))) + ' Hz')
# plt.title('Ride Frequency')

plt.legend(loc='lower left')

plt.show()