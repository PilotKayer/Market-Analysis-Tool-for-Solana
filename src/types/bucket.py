class Bucket:
    bucket_type: str
    transactions: list[any]

    def __init__(self, bucket_type: str, transactions: list[any]) -> None:
        self.bucket_type = bucket_type
        self.transactions = transactions

    def __len__(self) -> int:
        return len(self.transactions)
