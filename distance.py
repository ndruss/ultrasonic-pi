#Libraries
import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

class DistanceSensor:
    def __init__(self, trig: int, echo: int):
        self.trig = trig
        self.echo = echo

        #set GPIO direction (IN / OUT)
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)        

    def distance(self):
        # set Trigger to HIGH
        GPIO.output(self.trig, True)
    
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.trig, False)
    
        start_time = time.time()
        stop_time = time.time()
    
        # save StartTime
        while GPIO.input(self.echo) == 0:
            start_time = time.time()
    
        # save time of arrival
        while GPIO.input(self.echo) == 1:
            stop_time = time.time()
    
        # time difference between start and arrival
        time_elapsed = stop_time - start_time
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (time_elapsed * 34300) / 2
    
        return distance


def loop(sensor_1_fn = None):
    sensor_1 = DistanceSensor(5, 19)
    sensor_2 = DistanceSensor(12, 20)
    distance_1 = sensor_1.distance
    distance_2 = sensor_2.distance

    fast = 0.75
    slow = 1
    refresh_rate = fast

    now = time.time
    sleep = time.sleep
    time_last_active = now()
    time_to_sleep = 6000
    is_active = True

    def cm_to_percent(cm):
        percent = (1 - dist_1 / 30) + 0.2
        return min(1, max(percent, 0))

    while True:
        dist_1 = distance_1()
        dist_2 = distance_2()
        time_inactive = now() - time_last_active

        if dist_1 > 100:
            if time_inactive > time_to_sleep:
                refresh_rate = slow
                is_active = False
        else:
            refresh_rate = fast
            time_last_active = now()
            is_active = True
        
        if is_active:
            # print ('%.2f' % dist_1, '|', '%.2f' % dist_2)
            # print ('sensor 2: %.2f cm' % dist_2)
            level_1 = cm_to_percent(dist_1)
            sensor_1_fn(level_1)
        
        else:
            print ('Inactive for %.2f seconds' % time_inactive)

        sleep(refresh_rate)

def sense_distance(sensor_1_fn = None):
    try: loop(sensor_1_fn)

    except KeyboardInterrupt:
        print('Measurement stopped by User')    
        GPIO.cleanup()

# if __name__ == '__main__':
#     try: sense_distance()
 
#     except KeyboardInterrupt:
#         print('Measurement stopped by User')    
#         GPIO.cleanup()
