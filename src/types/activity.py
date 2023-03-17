class Activity(object):
    feature_names: list[str] = [
        'signature',
        'type',
        'source',
        'token_mint',
        'collection',
        'collection_symbol',
        'slot',
        'block_time',
        'buyer',
        'buyer_referral',
        'seller',
        'seller_referral',
        'price',
        'image',
    ]

    signature: str
    type: str
    source: str
    token_mint: str
    collection: str
    collection_symbol: str
    slot: int
    block_time: int
    buyer: str
    buyer_referral: str
    seller: str
    seller_referral: str
    price: int
    image: str

    def __init__(self, d):
        for k, v in d.items():
            if isinstance(k, (list, tuple)):
                setattr(self, k, [Activity(x) if isinstance(x, dict) else x for x in v])
            else:
                setattr(self, k, Activity(v) if isinstance(v, dict) else v)