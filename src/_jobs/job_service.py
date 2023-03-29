from src.common.logger import Logger
from src._jobs.GetBids import GetBids
from io import BytesIO


class JobService:
    """
    This class runs the various MapReduce jobs to manipulate the large data sets
    """
    logger: Logger = Logger('JobService')

    def prepare_stdin(self, data: list[any]) -> BytesIO:
        modified_data = ''
        for d in data:
            modified_data += f'{str(d)}\n'

        return BytesIO(bytes(modified_data, 'utf8'))

    def get_bids(self, data: list[any]) -> any:
        out: any = {}

        stdin = self.prepare_stdin(data)

        job = GetBids(['--no-conf', '-'])
        job.sandbox(stdin)

        with job.make_runner() as runner:
            runner.run()
            for key, value in job.parse_output(runner.cat_output()):
                self.logger.debug(f'key: {key} -> value: {value}')
                out[key] = value

        return out
