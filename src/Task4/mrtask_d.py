# What is the average trip time for different pickup locations?

from mrjob.job import MRJob
from datetime import datetime

class AverageTripTime(MRJob):

    def parse_datetime(self, datetime_str):
        formats = ['%d-%m-%Y %H:%M:%S', '%d-%m-%Y %H:%M', '%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S']
        for fmt in formats:
            try:
                return datetime.strptime(datetime_str, fmt)
            except ValueError:
                pass
        raise ValueError('no valid date format found')

    def mapper(self, _, line):
        # Skip the header line
        if not line.startswith('VendorID'):
            fields = line.split(',')
            pickup_location = fields[7]
            pickup_datetime = self.parse_datetime(fields[1])
            dropoff_datetime = self.parse_datetime(fields[2])
            trip_time = (dropoff_datetime - pickup_datetime).total_seconds() / 60.0
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