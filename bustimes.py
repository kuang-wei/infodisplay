from ctabustracker import CTABusTracker
import config as cfg

global busstop, cbt
busstop = '1521'
cbt = CTABusTracker(cfg.buskey)

def printtime(cbt, busstop):
	times = cbt.get_stop_predictions(busstop)
	for time in times:
		busnum = time['route_id']
		arrivaltime = time['prediction']
		currenttime = cbt.get_time()
		waittime = arrivaltime - currenttime
		print "%4s is arriving at %s in %2.0f minutes"%(busnum,
												arrivaltime.strftime("%H:%M"),
												waittime.seconds/60.)
if __name__ == '__main__':
	printtime(cbt, busstop)