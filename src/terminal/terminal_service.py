from os import system, name
from typing import List
from src.market.market_service import MarketService
from src._jobs.job_service import JobService
from src.common.logger import Logger, bcolors


class TerminalService:
    version: str
    market_service: MarketService
    job_service: JobService
    logger = Logger('TerminalService')
    data: any = {}

    def __init__(self, version: str) -> None:
        self.version = version
        self.market_service = MarketService()
        self.job_service = JobService()

    def check_args(self, args: List[str], number: int) -> bool:
        return len(args) != number

    def clear(self, args):
        if self.check_args(args, 1):
            self.logger.error(f'Expecting no argument, but got {len(args)-1}')
            return
        # for windows
        if name == 'nt':
            _ = system('cls')
        # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')

    def set_up(self, args) -> None:
        self.clear(args)
        print(f'Designed by Davide Alejandro Castejon'
              f'\nAll rights reserved'
              f'\n\nMarket Analysis Tool for Solana'
              f'\nVersion: {self.version}\n\n')

    def data_gathered(self, args) -> None:
        if len(args) > 2:
            self.logger.error(f'Expecting no to 1 argument, but got {len(args)-1}')
            return

        if len(args) == 1:
            if len(self.data.keys()) == 0:
                self.logger.log('No data has been gathered, please use clt to gather data')
                return
            self.logger.log('Gathered data for:')
            for key in self.data.keys():
                self.logger.log(f'{key} -> {len(self.data[key]["data"])}')
        else:
            col = args[1]
            if col not in self.data.keys():
                self.logger.log(f'No data found for {col}, use the following command to fix this:')
                self.logger.log(f'clt {col}')
                return
            self.logger.log(f'Data for: {col}')
            self.logger.log(f'Floor price: {self.data[col]["stats"]["floorPrice"] / 10**9} SOL')
            self.logger.log(f'Listed count: {self.data[col]["stats"]["listedCount"]}')
            print('\n' + '#'*20 + '  DATA GATHERED  ' + '#'*20 + '\n')
            for i in (range(10) if 10 < len(self.data[col]["data"]) else range(len(self.data[col]["data"]))):
                print(bcolors.OKCYAN + str(self.data[col]["data"][i]) + bcolors.ENDC + '\n')

    def collect_data(self, args):
        if self.check_args(args, 2):
            self.logger.error(f'Expecting 1 argument, but got {len(args) - 1}')
            return

        collection = args[1]
        if collection in self.data.keys():
            self.logger.debug(f'Data for {collection} already exists')
        stats = self.market_service.get_collection_stats(collection)
        self.data[collection] = {'stats': stats}

        if not 'volumeAll' in stats:
            self.logger.error(f'Collection {collection} not found')
            return

        self.logger.debug(f'Collecting data for {collection} collection')
        self.logger.log(stats)
        data = self.market_service.get_days_of_activities(collection, 1)

        self.data[collection]['data'] = data

    def collect_bids(self, args) -> None:
        if self.check_args(args, 2):
            self.logger.error(f'Expecting 1 argument, but got {len(args) - 1}')
            return

        collection: str = args[1]
        if collection not in self.data.keys():
            self.logger.log(f'No data found for {collection}')
            self.logger.log(f'Please run: clt {collection}')
            return
        if 'bids_data' in self.data[collection].keys():
            self.logger.log(f'Data collected for {collection}')
            self.logger.log(self.data[collection]['bids_data'])
            return

        self.logger.debug(f'Gathering bid data for {collection}')
        data_gathered = self.job_service.get_bids(self.data[collection]['data'])
        self.data[collection]['bids_data'] = data_gathered

    def test(self, args):
        self.logger.log('yabadabadoo testing da dooo')
        self.collect_data(['clt', 'elixir_ovols'])
        self.collect_bids(['bids', 'elixir_ovols'])
