# What is the average trip time for different pickup locations?

from mrjob.job import MRJob

class AverageTripTime(MRJob):

    def mapper(self, _, line):
        # Skip the header line
        if not line.startswith('VendorID'):
            fields = line.split(',')
            pickup_location = fields[7]
            trip_time = float(fields[4])
            yield pickup_location, (trip_time, 1)

    def combiner(self, pickup_location, trip_times):
        total_trip_time = 0
        total_count = 0
        for trip_time, count in trip_times:
            total_trip_time += trip_time
            total_count += count
        yield pickup_location, (total_trip_time, total_count)

    def reducer(self, pickup_location, trip_times):
        total_trip_time = 0
        total_count = 0
        for trip_time, count in trip_times:
            total_trip_time += trip_time
            total_count += count
        average_trip_time = total_trip_time / total_count
        yield pickup_location, average_trip_time


if __name__ == '__main__':
    AverageTripTime.run()