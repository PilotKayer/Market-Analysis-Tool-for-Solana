from mrjob.job import MRJob
import json

from src.market.market_service import MarketService


class GetActAttributes(MRJob):
    ms = MarketService()

    def mapper(self, _, line):
        test = line.replace("'", '"')
        test = test.replace('None', 'null')
        data = json.loads(test)
        keys = [
            'type', 'price',
            'buyer', 'tokenMint'
        ]

        # TODO: change the logic, add all bids and all sales separate
        if set(keys).issubset(set(data.keys())):
            if data['type'] == 'bid' or data['type'] == 'buyNow':
                attributes = self.ms.get_token_attributes(data['tokenMint'])
                for attribute in attributes:
                    yield (attribute['trait_type'], attribute['value']), data['price']

    def reducer(self, key, values):
        count, sum_v = 0, 0
        for i in values:
            sum_v += i
            count += 1
        yield key, (sum_v / count)


if __name__ == '__main__':
    GetActAttributes.run()
