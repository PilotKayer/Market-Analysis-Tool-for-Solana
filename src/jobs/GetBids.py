from mrjob.job import MRJob
from mrjob.step import MRStep
import json

class GetBids(MRJob):
    def steps(self):
        return [
            MRStep(mapper=self.mapper_1,
                   reducer=self.reducer_1),
            MRStep(reducer=self.reducer_2)
        ]

    def mapper_1(self, _, line):
        test = line.replace("'", '"')
        test = test.replace('None', 'null')
        data = json.loads(test)
        keys = [
            'type',
            'price',
            'buyer',
        ]

        if set(keys).issubset(set(data.keys())):
            if data['type'] == 'bid':
                yield 'total_bids', 1
                yield 'average_bid', data['price']
                yield data['buyer'], 1

    def reducer_1(self, key, values):
        if key == 'total_bids':
            yield key, sum(values)
        elif key == 'average_bid':
            count, sum_v = 0, 0
            for i in values:
                sum_v += i
                count += 1
            yield key, (sum_v / count)
        else:
            yield 'unique_wallets', 1

    def reducer_2(self, key, values):
        yield key, sum(values)


if __name__ == '__main__':
    GetBids.run()