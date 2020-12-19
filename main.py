from elasticsearch import Elasticsearch
from elasticsearch import ConnectionError
import queries
import notifier
import sys

list_url_ip = []
list_url_referrer = []
log_paths = []

indexes = {
    'r8x': 'c6442970-6811-11ea-b349-a52564ef3cef',
    'rscq': 'c35b19f0-66b6-11ea-b349-a52564ef3cef',
    'rsrf': '3a241ef0-7338-11ea-a2d2-b1d588dee884',
    'r6s': '297c9900-dd38-11ea-963c-51c506745496',
    'travelask': '5a0508e0-dd6b-11ea-963c-51c506745496',
    'rsck': '551a9be0-f0dc-11ea-963c-51c506745496'
}
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


def search(index, type_of_query, res_size=10000):
    try:
        result = es.search(
            index=f"{index}-*",
            body=type_of_query,
            size=res_size
        )
    except ConnectionError:
        print("Error connecting to elasticsearch")
        sys.exit(1)

    return result


def critical_count_of_5xx(result):
    return result['hits']['total']['value'] > 20


def critical_count_of_4xx(result):
    return result['hits']['total']['value'] > 500


def check_5xx():
    code = '5xx'
    global log_paths
    for idx in indexes:
        res = search(idx, queries.get_5xx_query())
        if critical_count_of_5xx(res):
            for hit in res['hits']['hits']:
                log_paths.append(hit["_source"]["log"]["file"]["path"])
            log_paths = list(dict.fromkeys(log_paths))
            for log in log_paths:
                target = search(idx, queries.get_5xx_target(log))
                err_count = target['hits']['total']['value']
                if err_count < 20 or log == '/data/logs/skylet.ru.access.log':
                    continue
                for url in target['hits']['hits']:
                    urls_ip = {}
                    additional_info = [
                        url["_source"]["response_code"],
                        url["_source"]["user_agent"],
                        url["_source"]["referrer"],
                        url["_source"]["remote_ip"]
                    ]
                    urls_ip[url["_source"]["url"]] = additional_info
                    list_url_ip.append(urls_ip)
                final_urls_ips = []
                final_urls_ips.append(list_url_ip[0])
                final_urls_ips.append(list_url_ip[round(len(list_url_ip) / 2)])
                final_urls_ips.append(list_url_ip[-1])
                notifier.send_message(log_path=log, server=idx, urls=final_urls_ips, count=err_count, code=code, top5_urls='')
                final_urls_ips.clear()
                list_url_ip.clear()
            log_paths.clear()


def check_4xx():
    code = '4xx'
    global log_paths
    for idx in indexes:
        res = search(idx, queries.get_4xx_query())
        if critical_count_of_4xx(res):
            for hit in res['hits']['hits']:
                log_paths.append(hit["_source"]["log"]["file"]["path"])
            log_paths = list(dict.fromkeys(log_paths))
            for log in log_paths:
                target = search(idx, queries.get_4xx_target(log))
                top5 = search(idx, queries.get_4xx_top5(log))
                err_count = target['hits']['total']['value']
                if err_count < 100:
                    continue
                for url in target['hits']['hits']:
                    urls_referrer = {}
                    additional_info = [
                        url["_source"]["response_code"],
                        url["_source"]["user_agent"],
                        url["_source"]["referrer"],
                        url["_source"]["remote_ip"]
                    ]
                    urls_referrer[url["_source"]["url"]] = additional_info
                    list_url_referrer.append(urls_referrer)
                final_urls_ips = []
                final_urls_ips.append(list_url_referrer[0])
                final_urls_ips.append(list_url_referrer[round(len(list_url_referrer) / 2)])
                final_urls_ips.append(list_url_referrer[-1])
                notifier.send_message(log_path=log, server=idx, urls=final_urls_ips, count=err_count, code=code, top5_urls=top5['aggregations']['2']['buckets'])
                list_url_referrer.clear()
            log_paths.clear()


if __name__ == '__main__':
    check_5xx()
    check_4xx()
