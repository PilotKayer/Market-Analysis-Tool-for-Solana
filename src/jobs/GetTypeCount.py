from mrjob.job import MRJob
import json


class GetTypeCount(MRJob):
    def mapper(self, _, line):
        test = line.replace("'", '"')
        test = test.replace('None', 'null')
        data = json.loads(test)

        if 'type' in data.keys():
            yield data['type'], 1

    def reducer(self, key, values):
        yield key, sum(values)


if __name__ == '__main__':
    GetTypeCount.run()
