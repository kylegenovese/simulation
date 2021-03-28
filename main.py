import itertools
import random
import simpy
import math

BATTERYTHRESHOLD = 40


def distance(p1, p2):
    distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
    return distance

class Car(object):
    def __init__(self, env):
        self.env = env
        # Start the run process everytime an instance is created.
        self.action = env.process(self.run())
        self.battery = 100
        self.num_drivers = 0
        self.num_charges = 0
        self.time_charging = 0
        self.time_driving = 0
        self.X = 0
        self.Y = 0

    def run(self):
        while True:
            #print('Parking at %d' % self.env.now)
            # We yield the process that process() returns
            # to wait for it to finish

            if(self.battery < BATTERYTHRESHOLD):
                #print('Start charging at %d' % self.env.now)
                charge_duration = .4 * (100 - self.battery)
                self.status = 1
                yield self.env.process(self.charge(charge_duration))

            next_driver_arrival = random.randint(1, 30)
            yield self.env.timeout(next_driver_arrival)

            # The charge process has finished and
            # we can start driving again.
            yield self.env.process(self.driver())

    def driver(self):
        #print('Next driver starts at %d' % self.env.now)
        dest_X = random.randint(-20,20)
        dest_Y = random.randint(-20, 20)

        trip_duration = distance([dest_X, dest_Y], [self.X, self.Y])
        yield self.env.timeout(trip_duration)

        self.battery = self.battery - trip_duration * 0.5
        #print("battery level at end: {}".format(self.battery))

        self.time_driving += trip_duration
        self.X = dest_X
        self.Y = dest_Y
        self.num_drivers += 1

    def charge(self, duration):
        self.battery = 100
        yield self.env.timeout(duration)
        #print('Charge complete at %d' % self.env.now)
        self.num_charges += 1
        self.time_charging += duration

if __name__ == '__main__':
    env = simpy.Environment()
    car = Car(env)
    env.run(until=1050)

    print('Number of drivers: %d' % car.num_drivers)
    print('Number of charges: %d' %car.num_charges)
    print('Time spent charging: %d' %car.time_charging)
    print('Time spent driving: %d' %car.time_driving)