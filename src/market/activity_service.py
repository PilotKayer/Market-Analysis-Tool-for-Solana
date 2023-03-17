from src.types.activity import Activity


class ActivityService:

    @staticmethod
    def activity_list(data_list: list) -> list[Activity]:
        out: list[Activity] = []
        for data in data_list:
            out.append(Activity(data))
        return out

    @staticmethod
    def prepare_data(data: list[dict]) -> dict:
        out: dict = {'signature': [], 'type': [], 'source': [], 'token_mint': [], 'collection': [],
                     'collection_symbol': [], 'slot': [], 'block_time': [], 'buyer': [], 'buyer_referral': [],
                     'seller': [], 'seller_referral': [], 'price': [], 'image': []}

        for d in data:
            for key in out:
                try:
                    out[key].append(d[key])
                except:
                    out[key].append(None)

        return out