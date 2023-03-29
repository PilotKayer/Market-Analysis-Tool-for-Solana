from src.common.logger import Logger, bcolors
from src.terminal.terminal_service import TerminalService

class Terminal:
    logger = Logger('SYSTEM')
    service: TerminalService
    run: bool = False

    def __init__(self, version):
        self.service = TerminalService(version)
        self.service.set_up(['starting'])
        self.functions = {
            'test': self.service.test,
            'clt': self.service.collect_data,
            'clear': self.service.set_up,
            'data': self.service.data_gathered,
            'bids': self.service.collect_bids,
        }

    def start(self):
        self.run = True

        while self.run:
            args = input(f'{bcolors.HEADER}$> {bcolors.ENDC}')
            args = args.split(' ')
            if len(args) == 0:
                continue

            if args[0] == 'exit' or args[0] == 'ext':
                self.run = False
                continue

            try:
                self.functions[args[0]](args)
                if args[0] != 'clear': print('\n')
            except KeyError:
                self.logger.error(f'Command {args[0]} not recognized as an internal command\n')

        self.logger.debug('System stopped running')
