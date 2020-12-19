import pyshorteners
import datetime
import main


def get_kibana_url(index: str, log: str) -> str:
    now = datetime.datetime.now()
    delta = now - datetime.timedelta(minutes=15)

    gte = now.strftime('%Y-%m-%dT%H:%M:%S')
    lte = delta.strftime('%Y-%m-%dT%H:%M:%S')

    enc_log = log.replace('/', '%2F')

    long_url = f"https://kibana.rscq.ru/s/{index}/app/kibana#/discover?_g=(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:'{lte}',to:'{gte}'))&_a=(columns:!(url,referrer,user_agent),filters:!(),index:'{main.indexes[index]}',interval:auto,query:(language:kuery,query:'response_code%20%3E%3D%20500%20and%20log.file.path%20:%20%22{enc_log}%22'),sort:!(!('@timestamp',desc)))"

    s = pyshorteners.Shortener()
    return s.tinyurl.short(long_url)
