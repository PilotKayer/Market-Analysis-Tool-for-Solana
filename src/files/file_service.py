from os.path import join, dirname, realpath
from src.common.logger import Logger
import json


class FileService:
    logger: Logger = Logger('FilesService')

    def save_file(self, data: dict, collection: str) -> None:
        """
        Save the collected data for a specific collection to a binary file

        :param data: The dictionary containing the data specific for the collection
        :param collection: The collection's name to be saved
        """
        time_stamp = data['data'][0]['blockTime']
        dir_name = join(dirname(realpath(__file__)), '../../saves/')

        try:
            with open(f'{dir_name}{collection}.{time_stamp}.smt', 'w') as f:
                f.write(json.dumps(data))
        except Exception as e:
            self.logger.error('An error was encountered while attempting to save to a file:')
            self.logger.error(f'Error: {str(e)}')

    def save_to_csv(self, data_points: dict, collection: str) -> None:
        """
        Given a specific collection and its data produces a csv of all the activities in the provided data.

        :param data_points: The dictionary containing the data specific for the collection
        :param collection: The collection's name to be saved
        """
        time_stamp = data_points['data'][0]['blockTime']
        dir_name = join(dirname(realpath(__file__)), '../../saves/')
        keys: list[str] = ['signature', 'type', 'source', 'tokenMint', 'collection', 'collectionSymbol', 'slot',
                           'blockTime', 'buyer', 'buyerReferral', 'seller', 'sellerReferral', 'price', 'image']

        try:
            with open(f'{dir_name}{collection}_{time_stamp}_activities.csv', 'w') as f:
                f.write(
                    'signature,type,source,tokenMint,collection,collectionSymbol,slot,blockTime,buyer,buyerReferral,seller,sellerReferral,price,image\n'
                )

                for data in data_points['data']:
                    out: str = ''

                    for key in keys:
                        if key in data.keys():
                            out += f'{data[key]},'
                        else:
                            out += ','

                    f.write(f'{out}\n')
        except Exception as e:
            self.logger.error('An error was encountered while attempting to save to a file:')
            self.logger.error(f'Error: {str(e)}')

    def load_file(self, data: dict, file_name: str, collection: str, deprecated: bool) -> None:
        """
        Loads a specific smt binary file

        :param data: The dictionary to be updated with the data loaded from the file
        :param file_name: The name of the file to load
        :param collection: The collection name used to store in "self.data"
        :param deprecated: If the file is deprecated or not
        """
        dir_name: str = join(dirname(realpath(__file__)), '../../saves/')

        try:
            with open(f'{dir_name}{file_name}', 'r') as f:
                data_loaded = json.loads(f.read())

                if deprecated:
                    data[collection] = data_loaded
                else:
                    for data_point in data_loaded['data']:
                        data[collection]['data'].append(data_point)

                    if 'attribute_data' in data_loaded.keys():
                        data[collection]['attribute_data'] = data_loaded['attribute_data']

                data[collection]['time_stamp'] = data[collection]['data'][0]['blockTime']
        except Exception as e:
            self.logger.error('An error was encountered while attempting to load a file:')
            self.logger.error(str(e))
