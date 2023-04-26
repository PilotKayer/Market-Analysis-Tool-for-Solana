from src.jobs.GetBids import GetBids
from src.jobs.GetActAttributes import GetActAttributes
from src.jobs.GetTypeCount import GetTypeCount
from io import BytesIO


class JobService:
    """
    This class runs the various MapReduce jobs to manipulate the data sets
    """

    def prepare_stdin(self, data: list[any]) -> BytesIO:
        """
        Prepares the data in bytes format so that it can be manipulated by the various MapReduce jobs

        :param data: The list of data to be prepared
        :return: The data in the correct bytes format
        """
        modified_data = ''
        for d in data:
            modified_data += f'{str(d)}\n'

        return BytesIO(bytes(modified_data, 'utf8'))

    def get_bids(self, data: list[any]) -> dict:
        """
        Runs the GetBids MapReduce python file

        :param data: The data to process
        :return: The processed data in dict format
        """
        out: any = {}

        stdin = self.prepare_stdin(data)

        job = GetBids(['--no-conf', '-'])
        job.sandbox(stdin)

        with job.make_runner() as runner:
            runner.run()
            for key, value in job.parse_output(runner.cat_output()):
                out[key] = value

        return out

    def get_activity_attributes(self, data: list[any]) -> dict:
        """
        Runs the GetActAttributes MapReduce python file

        :param data: The data to process
        :return: The processed data in dict format
        """
        out: any = {}

        stdin = self.prepare_stdin(data)

        job = GetActAttributes(['--no-conf', '-'])
        job.sandbox(stdin)

        with job.make_runner() as runner:
            runner.run()
            for key, value in job.parse_output(runner.cat_output()):
                if key[0] not in out.keys():
                    out[key[0]] = []
                out[key[0]].append({key[1]: value})

        return out

    def get_activity_types(self, data: list[any]) -> dict:
        """
        Runs the GetTypeCount MapReduce python file

        :param data: The data to process
        :return: The processed data in dict format
        """
        out: any = {}

        stdin = self.prepare_stdin(data)

        job = GetTypeCount(['--no-conf', '-'])
        job.sandbox(stdin)

        with job.make_runner() as runner:
            runner.run()
            for key, value in job.parse_output(runner.cat_output()):
                out[key] = value

        return out
