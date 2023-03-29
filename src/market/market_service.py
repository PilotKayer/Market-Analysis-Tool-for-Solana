from requests import Response, get
from src.market.activity_service import ActivityService
from src.types.activity import Activity
from src.common.logger import Logger
from time import time, sleep

class MarketService:
    """
    This class runs on the Magic Eden API endpoint to collect aggregated market data
    """

    endpoint: str = 'http://api-mainnet.magiceden.dev/v2'
    activity_service: ActivityService = ActivityService()
    logger: Logger = Logger('MarketService')

    def get_collection_stats(self, collection_symbol: str) -> any:
        """
        Gets the overall markets stats for a given collection

        :parameter collection_symbol: The name of the collection we wish to look up
        """
        result: Response = get(f'{self.endpoint}/collections/{collection_symbol}/stats')
        data = result.json()
        return data

    def get_collection_activities(self, collection_symbol: str, offset: int = 0, limit: int = 100) -> any:
        """
        Gets the market activities for a given collection

        :parameter collection_symbol: The name of the collection we wish to look up
        """
        sleep(0.25)
        result: Response = get(f'{self.endpoint}/collections/{collection_symbol}/activities?offset={str(offset)}&limit={str(limit)}')
        try:
            data = result.json()
            return data
        except:
            self.logger.debug('30 sec cooldown started')
            sleep(30)
            self.logger.debug('Resuming collection of data')
            return self.get_collection_activities(collection_symbol, offset, limit)

    def get_days_of_activities(self, collection_symbol: str, days: int) -> any:
        """
        Gets the market activities for a given collection for the past 'days' days

        :parameter collection_symbol: The name of the collection we wish to look up
        :parameter days:The number of days we wish take data for
        """
        current = time()
        to_remove = current - (days * 24 * 60 * 60)
        output = []
        switch: bool = True
        counter: int = 0
        err_counter: int = 0

        while switch and err_counter < 200:
            data_points = self.get_collection_activities(collection_symbol, offset=counter*100)

            for data in data_points:
                if data == 'errors':
                    err_counter += 1
                elif data['blockTime'] > to_remove:
                    output.append(data)
                else:
                    switch = False
                    break

            if type(data_points) == list:
                counter += 1

        time_taken = time()
        self.logger.debug(f'It took {int(time_taken-current)} seconds to complete the task')

        if err_counter > 0: self.logger.error(f'In the last {days} days there were {err_counter} transaction errors\nErrors: {err_counter}')
        return output


