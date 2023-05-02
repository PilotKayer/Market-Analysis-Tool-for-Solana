from requests import Response, get
from src.common.commons import NFT_MINT_ATTRIBUTE
from src.common.logger import Logger
from time import time, sleep

class MarketService:
    """
    This class runs on the Magic Eden API endpoint to collect aggregated market data
    """

    ENDPOINT: str = 'http://api-mainnet.magiceden.dev/v2'
    logger: Logger = Logger('MarketService')

    def get_collection_stats(self, collection_symbol: str) -> any:
        """
        Gets the overall markets stats for a given collection

        :parameter collection_symbol: The name of the collection we wish to look up
        """
        result: Response = get(f'{self.ENDPOINT}/collections/{collection_symbol}/stats')
        data = result.json()
        return data

    def get_collection_activities(self, collection_symbol: str, offset: int = 0, limit: int = 100) -> any:
        """
        Gets the market activities for a given collection

        :parameter collection_symbol: The name of the collection we wish to look up
        """
        sleep(0.25)
        result: Response = get(f'{self.ENDPOINT}/collections/{collection_symbol}/activities?offset={str(offset)}&limit={str(limit)}')
        try:
            data = result.json()
            return data
        except:
            self.logger.debug(f'30 sec cooldown started')
            sleep(30)
            self.logger.debug(f'Resuming collection of data')
            return self.get_collection_activities(collection_symbol, offset, limit)

    def get_days_of_activities(self, collection_symbol: str, to_remove: int) -> any:
        """
        Gets the market activities for a given collection for the past 'days' days

        :parameter collection_symbol: The name of the collection we wish to look up
        :parameter to_remove: The number of days we wish take data for
        """
        current = time()
        to_remove = current - to_remove
        output = []
        switch: bool = True
        counter: int = 0
        err_counter: int = 0

        while switch and err_counter < 99 and counter < 151:
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

        if err_counter > 0:
            self.logger.error(f'Encountered {err_counter} transaction errors')

        return output

    def get_token_attributes(self, mint: str) -> list[any]:
        """
        Get NFT metadata's attributes given a mint id

        :param mint: NFT mint id to be queried
        :return: dictionary of traits for the NFT
        """
        if mint in NFT_MINT_ATTRIBUTE.keys():
            return NFT_MINT_ATTRIBUTE[mint]

        result: Response = get(f'{self.ENDPOINT}/tokens/{mint}')
        try:
            data = result.json()['attributes']
            NFT_MINT_ATTRIBUTE[mint] = data
            return data
        except:
            if result.status_code == 400:
                data = result.json()
                if data['errors'][0]['msg'] == 'invalid token_mint':
                    return ['invalid token_mint']
            self.logger.debug('15 sec cooldown started')
            sleep(15)
            self.logger.debug('Resuming collection of data')
            return self.get_token_attributes(mint)

    def get_token_collection(self, mint: str) -> str:
        """
        Get NFT's collection symbol given a mint id

        :param mint: NFT mint id to be queried
        :return: collection symbol
        """

        result: Response = get(f'{self.ENDPOINT}/tokens/{mint}')
        try:
            data = result.json()['collection']
            return data
        except:
            data = result.json()
            if data['errors'][0]['msg'] == 'invalid token_mint':
                return 'invalid token_mint'
            self.logger.debug(f'15 sec cooldown started')
            sleep(15)
            self.logger.debug(f'Resuming collection of data')
            return self.get_token_collection(mint)