#Libraries
import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

class DistanceSensor:
    def __init__(self, trig: int, echo: int):
        self.trig = trig
        self.echo = echo

    def setup(self):
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


def sense_distance():
    sensor_1 = DistanceSensor(13, 26)
    sensor_1.setup()

    fast = 0.075
    slow = 0.5
    refresh_rate = fast

    time_last_active = time.time()
    is_active = True

    while True:
        dist = sensor_1.distance()
        time_inactive = time.time() - time_last_active

        if dist > 100:
            if time_inactive > 3:
                refresh_rate = slow
                is_active = False
        else:
            refresh_rate = fast
            time_last_active = time.time()
            is_active = True
        
        if is_active:
            print ('%.2f cm' % dist)
        
        else:
            print ('Inactive for %.2f seconds' % time_inactive)

        time.sleep(refresh_rate)


if __name__ == '__main__':
    try: sense_distance()
 
    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print('Measurement stopped by User')    
        GPIO.cleanup()
