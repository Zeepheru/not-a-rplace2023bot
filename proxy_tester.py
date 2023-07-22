import requests

proxies_text = """https://changzeehang:uTQrpFgM0e@193.43.119.137:50100
https://changzeehang:uTQrpFgM0e@185.248.50.212:50100
https://changzeehang:uTQrpFgM0e@185.248.50.10:50100
https://changzeehang:uTQrpFgM0e@193.43.119.248:50100
https://changzeehang:uTQrpFgM0e@185.248.50.7:50100
https://changzeehang:uTQrpFgM0e@185.248.50.103:50100
https://changzeehang:uTQrpFgM0e@185.248.50.158:50100
https://changzeehang:uTQrpFgM0e@185.248.50.175:50100
https://changzeehang:uTQrpFgM0e@193.43.119.238:50100
https://changzeehang:uTQrpFgM0e@193.43.119.244:50100
https://changzeehang:uTQrpFgM0e@193.43.119.132:50100
https://changzeehang:uTQrpFgM0e@193.43.119.149:50100
https://changzeehang:uTQrpFgM0e@193.43.119.145:50100
https://changzeehang:uTQrpFgM0e@185.248.50.2:50100
https://changzeehang:uTQrpFgM0e@185.248.50.47:50100
https://changzeehang:uTQrpFgM0e@185.248.50.216:50100
https://changzeehang:uTQrpFgM0e@185.248.50.222:50100
https://changzeehang:uTQrpFgM0e@185.248.50.155:50100
https://changzeehang:uTQrpFgM0e@193.43.119.128:50100
https://changzeehang:uTQrpFgM0e@193.43.119.165:50100
https://changzeehang:uTQrpFgM0e@185.248.50.210:50100
https://changzeehang:uTQrpFgM0e@185.248.50.112:50100
https://changzeehang:uTQrpFgM0e@185.248.50.85:50100
https://changzeehang:uTQrpFgM0e@193.43.119.69:50100
https://changzeehang:uTQrpFgM0e@193.43.119.29:50100"""

proxies_text_2 = """socks5://193.43.119.137:50101
socks5://185.248.50.212:50101
socks5://185.248.50.10:50101
socks5://193.43.119.248:50101
socks5://185.248.50.7:50101
socks5://185.248.50.103:50101
socks5://185.248.50.158:50101
socks5://185.248.50.175:50101
socks5://193.43.119.238:50101
socks5://193.43.119.244:50101
socks5://193.43.119.132:50101
socks5://193.43.119.149:50101
socks5://193.43.119.145:50101
socks5://185.248.50.2:50101
socks5://185.248.50.47:50101
socks5://185.248.50.216:50101
socks5://185.248.50.222:50101
socks5://185.248.50.155:50101
socks5://193.43.119.128:50101
socks5://193.43.119.165:50101
socks5://185.248.50.210:50101
socks5://185.248.50.112:50101
socks5://185.248.50.85:50101
socks5://193.43.119.69:50101
socks5://193.43.119.29:50101"""

def main():
    def test_connection(proxy = None):
        url = 'https://httpbin.org/get'
        if not proxy:
            r = requests.get(url)
            # print(r.status_code)
        else:
            # print(proxy)
            try:
                r = requests.get(url, proxies={"https":proxy, "http":proxy}, timeout=5)
                return r.status_code
            except:
                return False

    proxies = proxies_text_2.splitlines()
    test_connection()
    n = 0
    for proxy in proxies:
        resp = test_connection(proxy=proxy)
        if resp == False:
            print(f"Error connecting through {proxy}")
            continue

        n += 1

    print(f"{n}/{len(proxies)} Functional")

if __name__ == "__main__":
    main()

