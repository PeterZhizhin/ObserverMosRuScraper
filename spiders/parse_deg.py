import scrapy
import enum


class UrlType(enum.Enum):
    BLOCKS = 1
    TRANSACTION = 2
    START = 3


def parse_type_from_url(url):
    if url.startswith('https://observer.mos.ru/api/blocks/'):
        return UrlType.BLOCKS
    if url.startswith('https://observer.mos.ru/api/transactions/'):
        return UrlType.TRANSACTION
    if url == 'https://observer.mos.ru':
        return UrlType.START


class ParseDegSpider(scrapy.Spider):
    name = 'parse_deg'
    allowed_domains = ['observer.mos.ru']
    start_urls = ['https://observer.mos.ru']


    def __init__(self, start_block=2000, end_block=2005, folder_to_save_to='results', **kwargs):
        self.start_block = int(start_block)
        self.end_block = int(end_block)
        super().__init__(**kwargs)


    def handle_blocks(self, response):
        block_id = int(response.url.split('/')[-2])

        json_response = response.json()
        json_response['type'] = 'block'
        json_response['block_id'] = block_id
        yield json_response

        tx_hashes_in_block = [payload['hash'] for payload in json_response['payload']]
        tx_urls = [f'https://observer.mos.ru/api/transactions/{tx_hash}' for tx_hash in tx_hashes_in_block]
        yield from response.follow_all(tx_urls, callback=self.parse)


    def handle_transaction(self, response):
        tx_hash_from_url = response.url.split('/')[-1]

        json_response = response.json()
        json_response['type'] = 'transaction'
        json_response['tx_hash_from_url'] = tx_hash_from_url
        yield json_response


    def handle_start(self, response):
        all_blocks = [f'https://observer.mos.ru/api/blocks/{i}/transactions' for i in range(self.start_block, self.end_block)]
        yield from response.follow_all(all_blocks[::-1], callback=self.parse)


    def parse(self, response):
        url_type = parse_type_from_url(response.url)

        if url_type == UrlType.BLOCKS:
            yield from self.handle_blocks(response)
        elif url_type == UrlType.TRANSACTION:
            yield from self.handle_transaction(response)
        elif url_type == UrlType.START:
            yield from self.handle_start(response)
        else:
            raise ValueError('Unknown URL type')
