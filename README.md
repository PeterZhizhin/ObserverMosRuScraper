# Скрепер для сайта observer.mos.ru
## Инструкция по запуску

1. Найдите виртуалку/VPN из России. Нероссийские IP очень активно банятся даже при малейших попытках что-то скачать.
1. Установите `scrapy`: `pip install scrapy`
1. Запустите скрепинг: `python3 -m scrapy crawl parse_deg -a start_block=0 -a end_block=43360 -o blocks_0_to_43360.jl -s JOBDIR=crawls/blocks0_to_43360 -s CONCURRENT_REQUESTS=128 -s CONCURRENT_REQUESTS_PER_DOMAIN=128 -s CONCURRENT_ITEMS=256`

Аргументы:
* `start_block` -- первый блок который нужно скачать (вместе с транзакциями оттуда)
* `end_block` -- последний блок который нужно скачать (не включая)

Остальные аргументы стандартные для Scrapy, про них можно почитать вот тут: https://docs.scrapy.org/en/latest/topics/settings.html

Важный из них вот этот аргумент:
* `JOBDIR` -- папка, куда сохранять базу уже загруженных запросов, так Scrapy не будет повторно загружать уже загруженные запросы.

Если нужно докачать какие-то блоки, то можно поменять аргументы `start_block`, `end_block`, но передав тот же самый `JOBDIR`.
