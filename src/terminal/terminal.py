from src.common.logger import Logger, BColors
from src.terminal.terminal_service import TerminalService


class Terminal:
    logger = Logger('Terminal')
    service: TerminalService
    run: bool = False

    def __init__(self, version: str):
        self.service = TerminalService(version)
        self.service.set_up(['starting'])
        self.functions = {
            'help': self.help,
            'test': self.service.test,
            'clt': self.service.collect_data,
            'rem': self.service.remove_data,
            'clear': self.service.set_up,
            'data': self.service.data_gathered,
            'bids': self.service.collect_bids,
            'att': self.service.collect_attributes,
            'save': self.service.save_to_smt_file,
            'csv': self.service.save_to_csv,
            'load': self.service.read_from_smt_file,
            'nft': self.service.get_nft_token,
            'types': self.service.get_activity_types,
            'full': self.service.get_full_collection,
        }
        # todo: add a save to csv

    def help(self, args: list[str]) -> None:
        """
        Displays what each function does

        :param args: Optional name of the function
        """
        if len(args) == 1:
            for key in self.functions:
                print(f'{key}:\t{self.functions[key].__doc__}')
        elif len(args) == 2:
            symbol = args[1]

            if symbol not in self.functions.keys():
                self.logger.error(f'No function {symbol} found')
                return

            print(f'{symbol}:\t{self.functions[symbol].__doc__}')
        else:
            self.logger.error(f'Expecting no to 1 argument, but instead received {len(args) - 1} arguments')

    def start(self) -> None:
        """
        Launches the Terminal to let it start gathering the user inputs
        """
        self.run = True

        while self.run:
            args = input(f'{BColors.HEADER}$> {BColors.END_C}')
            args = args.split(' ')
            if len(args) == 0:
                continue

            if args[0] == 'exit' or args[0] == 'ext':
                self.run = False
                continue

            try:
                self.functions[args[0]](args)
                if args[0] != 'clear':
                    print('\n')
            except KeyError as e:
                self.logger.error(f'Command {args[0]} not recognized as an internal command\n')
                self.logger.error(str(e))

        self.logger.debug('System stopped running')
