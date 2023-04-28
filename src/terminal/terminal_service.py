from os import system, name, listdir
from os.path import isfile, join, dirname, realpath
from src.market.market_service import MarketService
from src.jobs.job_service import JobService
from src.common.logger import Logger
from src.common.commons import BColors
from src.files.file_service import FileService
from time import time


class TerminalService:
    version: str
    market_service: MarketService
    job_service: JobService
    file_service: FileService
    logger = Logger('TerminalService')
    data: any = {}

    def __init__(self, version: str) -> None:
        self.version = version
        self.market_service = MarketService()
        self.job_service = JobService()
        self.file_service = FileService()

    def check_args(self, args: list[str], number: int) -> bool:
        """
        Checks if the number of expected arguments is the same as the received arguments.

        :param args: The received arguments
        :param number: The number of expected arguments
        :return: A boolean defining if the check passed (false) or failed (true)
        """
        failure: bool = len(args) != (number + 1)

        if failure:
            if number == 0:
                self.logger.error(f'Expecting no argument, but got {len(args) - 1}')
            else:
                self.logger.error(f'Expecting {number} argument{"s" if number != 1 else ""}, but got {len(args) - 1}')

        return failure

    def clear(self, args: list[str]) -> None:
        """
        Clears the terminal window for both Windows or Linux/Mac OSs

        :param args: The input arguments
        """
        if self.check_args(args, 0):
            return

        # for windows
        if name == 'nt':
            _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')

    def set_up(self, args: list[str]) -> None:
        """
        Displays the top message of the Terminal, as well as clear it

        :param args: The input arguments
        """
        if self.check_args(args, 0):
            return

        self.clear(args)
        print(f'Designed by Davide Alejandro Castejon'
              f'\nAll rights reserved'
              f'\n\nMarket Analysis Tool for Solana'
              f'\nVersion: {self.version}\n\n')

    def data_gathered(self, args: list[str]) -> None:
        """
        Displays in the Terminal the data gathered so far

        :param args: Possible argument for a given collection
        """
        if len(args) > 2 or len(args) == 0:
            self.logger.error(f'Expecting no to 1 argument, but got {len(args) - 1}')
            return

        if len(args) == 1:
            if len(self.data.keys()) == 0:
                self.logger.error('No data has been gathered, please use "clt" to gather data or "help" to learn more')
                return

            self.logger.log('Gathered data for:')
            for key in self.data.keys():
                self.logger.log(
                    f'{key} -> {len(self.data[key]["data"])} {"-b" if "bids_data" in self.data[key].keys() else ""} {"-a" if "attribute_data" in self.data[key].keys() else ""}')
        else:
            col: str = args[1]

            if col not in self.data.keys():
                self.logger.error(f'No data found for {col}, use the following command to fix this:')
                self.logger.error(f'clt {col}')
                return

            self.logger.log(f'### Data for: {col}\n')
            self.logger.log(f'Floor price: {self.data[col]["stats"]["floorPrice"] / 10 ** 9} SOL')
            self.logger.log(f'Listed count: {self.data[col]["stats"]["listedCount"]}')

            if 'bids_data' in self.data[col].keys():
                print()
                self.logger.log(f'### Bids data collected:\n')
                for key in self.data[col]['bids_data']:
                    self.logger.log(f'{key} -> {self.data[col]["bids_data"][key]}')

            if 'attribute_data' in self.data[col].keys():
                print()
                self.logger.log(f'### Attribute data collected\n')
                self.logger.log(f'Use: "att {col}" to see Attribute data')

    def collect_data(self, args: list[str]) -> None:
        """
        Uses the market service to collect fresh data up to 1 day of age

        :param args: Collection name required as an argument
        """
        if self.check_args(args, 1):
            return

        collection: str = args[1]
        time_missing: float = -1
        temp_save: list[any] = []

        if collection in self.data.keys():
            if 'time_stamp' in self.data[collection].keys():
                stamp: str = self.data[collection]['time_stamp']
                time_missing = time() - float(stamp)
                if time_missing > 24 * 60 * 60:
                    time_missing = 24 * 60 * 60
                if time_missing <= 0:
                    self.logger.error(f'Data already collected for {collection}')
                    return
                else:
                    temp_save = self.data[collection]['data']

        stats = self.market_service.get_collection_stats(collection)
        if 'volumeAll' not in stats:
            self.logger.error(f'Collection {collection} not found')
            return

        self.data[collection] = {'stats': stats}

        self.logger.debug(f'Collecting data for {collection} collection')
        if time_missing == -1:
            data = self.market_service.get_days_of_activities(collection, (24 * 60 * 60))
        else:
            data = self.market_service.get_days_of_activities(collection, int(time_missing))
            for temp in temp_save:
                data.append(temp)

        self.data[collection]['data'] = data
        self.data[collection]['time_stamp'] = data[0]['blockTime']

        self.logger.debug('Data collected successfully')

    def remove_data(self, args: list[str]) -> None:
        """
        Remove loaded data for a collection

        :param args: Collection name required as an argument
        """
        if self.check_args(args, 1):
            return

        collection: str = args[1]
        if collection not in self.data.keys():
            self.logger.error(f'No collection named {collection} found in the loaded data')
            return

        self.data.pop(collection)
        self.logger.debug(f'Data for {collection} has been removed')

    def collect_bids(self, args: list[str]) -> None:
        """
        Collects the bid's data for the collection.
        This collects only bids which target a specific token and not the whole collection.

        :param args: Collection name required as an argument
        """
        if self.check_args(args, 1):
            return

        collection: str = args[1]

        if collection not in self.data.keys():
            self.logger.error(f'No data found for {collection}')
            self.logger.error(f'Please run: clt {collection}')
            return

        if 'bids_data' in self.data[collection].keys():
            self.logger.log(f'Data collected for {collection}:')
            for key in self.data[collection]['bids_data']:
                self.logger.log(f'{key} -> {self.data[collection]["bids_data"][key]}')
            return

        self.logger.debug(f'Gathering bid data for {collection}')

        data_gathered = self.job_service.get_bids(self.data[collection]['data'])
        self.data[collection]['bids_data'] = data_gathered
        self.collect_bids(args)

        self.logger.debug('Bid data collected successfully')

    def collect_attributes(self, args: list[str]) -> None:
        """
        Collects the attribute's data for the collection

        :param args: Collection name required as an argument
        """
        if self.check_args(args, 1):
            return

        collection: str = args[1]
        data_to_parse: list[any] = []

        if collection not in self.data.keys():
            self.logger.error(f'No data found for {collection}')
            self.logger.error(f'Please run: clt {collection}')
            return

        if 'attribute_data' in self.data[collection].keys():
            if 'time_stamp' in self.data[collection]['attribute_data'].keys() and 'time_stamp' in self.data[collection].keys():
                time_stamp: str = self.data[collection]['attribute_data']['time_stamp']

                if time_stamp == self.data[collection]['time_stamp']:
                    self.logger.log(f'Data collected for {collection}')

                    for key in self.data[collection]['attribute_data']:
                        if key == 'time_stamp':
                            continue

                        print()
                        self.logger.log(f'### Attribute: {key}:')
                        for data in self.data[collection]['attribute_data'][key]:
                            self.logger.log(f"{list(data.keys())[0]} -> {data[list(data.keys())[0]]} SOL")

                    return

                for data in self.data[collection]['data']:
                    if int(data['blockTime']) > int(time_stamp):
                        data_to_parse.append(data)
                    else:
                        break

        self.logger.debug(f'Gathering attributes data for {collection}')

        if len(data_to_parse) > 0:
            data_gathered = self.job_service.get_activity_attributes(data_to_parse)
            temp = {}

            keys_one: list[str] = list(self.data[collection]['attribute_data'].keys())
            keys_two: list[str] = list(data_gathered.keys())
            list_of_keys: list[str] = list(set(keys_one) - {'time_stamp'}) + list(set(keys_two) - set(keys_one) - {'time_stamp'})

            for trait_type in list_of_keys:
                if trait_type not in temp.keys():
                    temp[trait_type] = []

                if trait_type in self.data[collection]['attribute_data']:
                    for data in self.data[collection]['attribute_data'][trait_type]:
                        for value in data.keys():
                            price: float = data[value]

                            if trait_type in data_gathered.keys():
                                if value in data_gathered[trait_type]:
                                    for i, x in enumerate(data_gathered[trait_type]):
                                        if x == value:
                                            price = (price + data_gathered[trait_type][i][x]) / 2

                            temp[trait_type].append({value: price})
                else:
                    for data in data_gathered[trait_type]:
                        for value in data.keys():
                            price = data[value]
                            temp[trait_type].append({value: price})

            data_gathered = temp
        else:
            data_gathered = self.job_service.get_activity_attributes(self.data[collection]['data'])

        self.data[collection]['attribute_data'] = data_gathered
        self.data[collection]['attribute_data']['time_stamp'] = self.data[collection]['time_stamp']
        self.collect_attributes(args)

        self.logger.debug('Attribute data collected successfully')

    def save_to_smt_file(self, args: list[str]) -> None:
        """
        Save the collected data for a specific collection or for all gathered collections

        :param args: Optional collection name
        """
        if len(args) <= 1:
            self.logger.log('Do you wish to save all the gathered data? (Y/n)')
            ans: str = input(f'{BColors.OK_BLUE}?> {BColors.END_C}')

            if ans.lower() != 'y' and ans.lower() != 'yes':
                self.logger.log('Data not getting saved')
                return
            else:
                self.logger.debug('Saving data')
                for collection in list(self.data.keys()):
                    self.file_service.save_file(self.data[collection], collection)
        else:
            collection: str = args[1]

            if collection not in self.data.keys():
                self.logger.error(f'No data found for {collection}')
                self.logger.error(f'Please run: clt {collection}')
                return

            self.logger.debug(f'Saving data for {collection}')
            self.file_service.save_file(self.data[collection], collection)

        self.logger.debug('Data successfully saved')

    def save_to_csv(self, args: list[str]) -> None:
        """
        Crates a csv file with all the collected data for a specified collection

        :param args: Collection name required as an argument
        """
        if self.check_args(args, 1):
            return

        col: str = args[1]
        if col not in self.data.keys():
            self.logger.error(f'No data found for {col}')
            self.logger.error(f'Please run: clt {col}')
            return

        self.logger.debug(f'Saving data for {col}')
        self.file_service.save_to_csv(self.data[col], col)
        self.logger.debug('Data successfully saved as csv')

    def read_from_smt_file(self, args: list[str]) -> None:
        """
        Finds all save files and prompts the user to load one

        :param args: The input arguments
        """
        if self.check_args(args, 0):
            return

        dir_name: str = join(dirname(realpath(__file__)), '../../saves/')
        list_of_files: list[str] = [f for f in listdir(dir_name) if isfile(join(dir_name, f))]
        if len(list_of_files) == 0:
            self.logger.error('No save file found in "saves/" folder')
            return

        self.logger.log('### Save files found:')
        for index, file_name in enumerate(list_of_files):
            self.logger.log(f'{index + 1}: {file_name}')

        print()
        self.logger.log(f'Please select a file from the number 1 to {len(list_of_files)}')
        ans: str = input(f'{BColors.OK_BLUE}?> {BColors.END_C}')
        try:
            ans_int: int = int(ans)
            file_name: str = list_of_files[ans_int - 1]
            deprecated: bool = False
            stamp: list[str] = file_name.split('.')
            collection: str = stamp[0]

            now: float = time()
            if now - int(stamp[1]) >= (24 * 60 * 60):
                deprecated = True
                self.logger.log(f'File {file_name} is deprecated, do you wish to load it anyway? (Y/n)')
                ans: str = input(f'{BColors.OK_BLUE}?> {BColors.END_C}')
                if ans.lower() != 'y' and ans.lower() != 'yes':
                    self.logger.log('User decided not to load data')
                    return

            if not deprecated:
                self.logger.debug(f'Collecting fresh data for {collection}')

                stats = self.market_service.get_collection_stats(collection)
                self.data[collection] = {'stats': stats}
                self.data[collection]['data'] = self.market_service.get_days_of_activities(collection, int(now - int(stamp[1])))

                self.logger.debug('Fresh data collected, bids and attribute data needs to be recalculated')

            self.file_service.load_file(self.data, file_name, collection, deprecated)

            self.logger.debug('File loaded successfully')
        except ValueError:
            self.logger.error(f'Expected an integer from 1 to {len(list_of_files)}')

    def get_nft_token(self, args: list[str]) -> None:
        """
        Collects a specific NFT given a mint and shows its attributes and (if calculated) their calculated SOL value

        :param args: Mint address required as an argument
        """
        if self.check_args(args, 1):
            return

        mint: str = args[1]
        token = self.market_service.get_token_attributes(mint)
        if token[0] == 'invalid token_mint':
            self.logger.error('Invalid token mint received')
            return
        else:
            self.logger.log(f'Token {mint} has been found\n')

        collection: str = self.market_service.get_token_collection(mint)
        values: list[float] = []
        attribute_data: bool = False

        if collection in self.data.keys():
            if 'attribute_data' in self.data[collection].keys():
                attribute_data = True

        for attribute in token:
            self.logger.log(f'{attribute["trait_type"]} : {attribute["value"]}')
            if attribute_data:
                temps = self.data[collection]['attribute_data'][attribute["trait_type"]]
                found: bool = False

                for temp in temps:
                    if str(attribute["value"]) in temp.keys():
                        self.logger.log(f'Trait valued at: {temp[str(attribute["value"])]} SOL')
                        values.append(temp[str(attribute["value"])])

                        found = True
                        break

                if not found:
                    self.logger.log(f'Trait valued at: {self.data[collection]["stats"]["floorPrice"]/10**9} SOL (Trait not found, using floor price)')
                    values.append(self.data[collection]["stats"]["floorPrice"]/10**9)

        if len(values) != 0:
            avg: float = sum(values) / len(values)
            print()
            self.logger.log(f'The NFT has an average attribute value of: {avg} SOL')
        else:
            print()
            self.logger.log('No trait values have been found')
            self.logger.log('Run the following command to access more NFT data:')
            self.logger.log(f'bids {collection}')

    def get_activity_types(self, args: list[str]) -> None:
        """
        Displays the count of the various types of transactions collected in the data

        :param args: Collection name required as an argument
        :return:
        """
        if self.check_args(args, 1):
            return

        collection: str = args[1]

        if collection not in self.data.keys():
            self.logger.error(f'No data found for {collection}')
            self.logger.error(f'Please run: clt {collection}')
            return

        types = self.job_service.get_activity_types(self.data[collection]['data'])

        self.logger.log(f'### Types found for {collection}:\n')
        for key in types:
            self.logger.log(f'{key} -> {types[key]}')

    def get_full_collection(self, args: list[str]) -> None:
        """
        Given a collection, it collects/load from file (or both) the data.
        Then performs calculations to determine bids data and attribute data.

        :param args: Collection name required as an argument
        """
        if self.check_args(args, 1):
            return

        symbol: str = args[1]
        if symbol in self.data.keys():
            self.logger.error(f'Collection {symbol} already loaded')
            self.logger.error(f'Use "rem {symbol}" to remove the data')
            return

        self.logger.debug(f'Attempting to load save file for {symbol}')

        dir_name: str = join(dirname(realpath(__file__)), '../../saves/')
        list_of_files: list[str] = [f for f in listdir(dir_name) if isfile(join(dir_name, f))]
        deprecated: bool = False

        for file_name in list_of_files:
            stamp: list[str] = file_name.split('.')
            collection = stamp[0]

            if collection == symbol:
                try:
                    deprecated = False
                    now = time()

                    if now - int(stamp[1]) >= (24 * 60 * 60):
                        self.logger.log(f'File {file_name} is deprecated. Do you wish to load it anyway? (Y/n)')
                        ans: str = input(f'{BColors.OK_BLUE}?> {BColors.END_C}')

                        if ans.lower() != 'y' and ans.lower() != 'yes':
                            deprecated = True
                        else:
                            continue

                    if not deprecated:
                        self.logger.debug(f'Collecting fresh data for {symbol}')

                        stats = self.market_service.get_collection_stats(collection)
                        self.data[collection] = {'stats': stats}
                        data = self.market_service.get_days_of_activities(collection, int(now - float(stamp[1])))
                        self.data[collection]['data'] = data
                        self.data[collection]['time_stamp'] = data[0]['blockTime']

                    self.logger.debug('Loading file...')
                    self.file_service.load_file(self.data, file_name, collection, deprecated)
                except Exception as e:
                    self.logger.error(str(e))

                break

        if symbol not in self.data.keys():
            self.logger.debug(f'Collecting data for {symbol}')
            self.collect_data(['clt', symbol])

        if not deprecated:
            self.logger.debug(f'Collecting bids data for {symbol}')
            self.collect_bids(['bids', symbol])

            self.logger.debug(f'Collecting attribute data for {symbol}')
            self.collect_attributes(['att', symbol])

        self.logger.debug('Saving data to file...')
        self.file_service.save_file(self.data[symbol], symbol)

        self.logger.debug('Full data loaded')

    def test(self, args: list[str]) -> None:
        """
        Runs the three loggers to check they are all working properly.
        Also displays the arguments this function receives for testing purposes

        :param args: Input agruments
        """
        self.logger.log('Testing the three types of loggers')
        self.logger.debug('Testing the three types of loggers')
        self.logger.error('Testing the three types of loggers')

        self.logger.log(f'Received arguments {args}')