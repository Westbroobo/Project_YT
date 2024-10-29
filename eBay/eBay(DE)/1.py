"""
Filename:3-1.fetch_vehicle1.py
Author: Westbroobo
Date: 2024/9/3
"""
import requests

cookies = {
    '__uzma': '6a946330-6f4e-4e0f-bf5b-7f2dc59681cc',
    '__uzmb': '1723596762',
    '__uzme': '9627',
    'cid': 'rtGJxMGrMTP6DvvZ%231787088840',
    '__ssds': '2',
    '__uzmaj2': 'cf401a82-2290-4762-bbff-c170c7639448',
    '__uzmbj2': '1723596775',
    '__uzmlj2': '1wFi4POLMnfGxtNJi/brATI9MbTWgWJarlSEdiFQoi8=',
    '_gcl_au': '1.1.1206382020.1724034475',
    '_pin_unauth': 'dWlkPU1EVTJaR1ZoT1RndE9ETXdZaTAwWmpSaUxXSXdNRGt0WVRnMk1tTXlaRFJqTlRZNA',
    '_fbp': 'fb.1.1724034477258.158101776588160977',
    'shs': 'BAQAAAZGG1Rg0AAaAAVUAD2idM4MyMjE4NjUxOTQxMDAzLDIhloZ2mR8IZTgTl6aj38ALmhL8EA**',
    'AMP_MKTG_f93443b04c': 'JTdCJTdE',
    '__gsas': 'ID=50a8dc273da81240:T=1725323526:RT=1725323526:S=ALNI_MaQMDqM4jlYWxEvg0dJdoR3wg-H0Q',
    '__ssuzjsr2': 'a9be2cd8e',
    'ak_bmsc': 'BF476594CFFF701C9AA91197C90583BD~000000000000000000000000000000~YAAQlVcyuLJnv7ORAQAAE4rTthj+PcMcQx38BVxZ8YGIJLPQ6ZEuKmVZC/hH7De5bz8OpygU7C1v260mOn1r7c0dOLWYRL3WACeE3XRYYZOB3L+YrsyAjjUdYWROOH0lmKv3urz9qlateP2M8lyY6YeWBLXmqx4ZgD+eNoi4CY3TBqjSaWovAED2T3zCXJKvfBZNOORunt2kaaLMGuv7Xukep1ltiZ/Ao/mdBjjGA4bzX6HyvynkB/oqhBc+JCjFzWHPOxdAwuUyOgp155krz6ez9rdhwXkMVz5dd7VD7qC39/dn/kBGAfF3zBmbXY6r9mT0PVJhwE08lEHQrOUpnr9h+b+3mQkcVkJIPsHPtmuadEeFnIZSQOtkB4DlvqH3UE+qgaA=',
    'utag_main__sn': '9',
    'utag_main_ses_id': '1725352052747%3Bexp-session',
    'utag_main__ss': '0%3Bexp-session',
    '_uetsid': 'cf7d206069cf11ef9cf043a45a3e33a7|1lmnoy3|2|fov|0|1707',
    '_uetvid': 'af91df805dd211ef9a188581b088cdb8|1238edk|1725352684945|2|1|bat.bing.com/p/insights/c/e',
    '__uzmcj2': '3883919937322',
    '__uzmdj2': '1725352782',
    '__uzmfj2': '7f6000d11bb8f3-0099-435f-9279-b809986d0d4517235967755241756007108-b1ff535434ae4b05199',
    '__deba': '9xUzzMmIDQpxF_hROW4vkOEylFZDXiSvD4-cpYf60rsWEf_7IhLDZNZxfRW17gfjJGGSn4EAAKx72GOtZsqSrsfIp8YWLdGXVxFwpDOIJvrxA4VJ0ODuMtxWoLO0ACc5bAieeLuHEc8rx6cup6vwEw==',
    '__uzmc': '7793937392683',
    '__uzmd': '1725352784',
    '__uzmf': '7f6000d11bb8f3-0099-435f-9279-b809986d0d4517235967620891756022327-34409e2c96a74ca7373',
    'utag_main__se': '4%3Bexp-session',
    'utag_main__st': '1725354647603%3Bexp-session',
    'utag_main__pn': '4%3Bexp-session',
    'cto_bundle': 'MZbpnV9QemhwcVY2QUN1UkVONW85NlNqWlAlMkZMODN4bm5USUV0a2xhc0MlMkZ4ckFtbFJMWElaeTZYYjFQRENwSDBPVU9tejZhalVIYUFZaWdqNDl6bzF6Wm45Y3B0NmZDJTJGT1N6ajhJSmJiWVBMdCUyRjJxJTJCbU16cjRpbFNOdW5zM0tTbjVzb3VwJTJGZXdjR2hBQVlXelpxeXNuRldtSmclM0QlM0Q',
    '__gads': 'ID=5b30965c3a097cc4:T=1725325695:RT=1725352950:S=ALNI_Ma8Miyz8jcu8d1osoulNDLcU8s4-w',
    '__gpi': 'UID=00000eea9fba1122:T=1725325695:RT=1725352950:S=ALNI_MbLQEiGoFpmv444j9G6vnYFDJNYhg',
    's': 'CgADuAI9m2B3XMwZodHRwczovL3d3dy5lYmF5LmRlL3NjaC9pLmh0bWw/X2Zyb209UjQwJl90cmtzaWQ9cDIzMzQ1MjQubTU3MC5sMTMxMyZfbmt3PUV4aGF1c3QrTWFuaWZvbGQrJl9zYWNhdD0wJl9vZGt3PTE3MTQxNzQyMDAmX29zYWNhdD0wJkxIX1ByZWZMb2M9MQcA+AAgZtgd1zRlNWY2MmJjMTkxMGFjNmEwNjBhM2EwOWZmZjkxMWEwzhnLdQ**',
    'totp': '1725353635894.WANjekdMWcGem27SE+ck+HsQ5ikmItyKe63gqdvD53uSaRFp4kefHI7Ot35kK+ZchsIgzYdEZymS9Sj+NaJC2w==.6PdnjPVoBdQ8gZtGMBX3gYxJfbKcKwz6ijbgFZe4m7s',
    'AMP_f93443b04c': 'JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI2NDhiNTk4ZS1jMmEyLTQyMGYtYjViMC0zNTk4NTBkZWRiNmElMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzI1MzQxNjg4MDU4JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTcyNTM1MzY0Nzg2MyUyQyUyMmxhc3RFdmVudElkJTIyJTNBNDc3JTJDJTIycGFnZUNvdW50ZXIlMjIlM0ExNTElN0Q=',
    'dp1': 'bu1p/eWFuZy0xMDE0OTQ*6a9935af^kms/in6a9935af^pbf/%230000e000e0000000808000000068b8022f^u1f/yangteng6a9935af^tzo/-1e066d6da67^expt/000172359687002767ac9a06^bl/US6a9935af^',
    'ns1': 'BAQAAAZBR14g6AAaAAKUADWi4Ai8yMzYyODgzMzM1LzA7Zg9du2eSfRLnJ3cD8tQYnMvw9OI*',
    'nonsession': 'BAQAAAZBR14g6AAaAAAQAC2idM4N5YW5nLTEwMTQ5NAAQAAtouAIveWFuZy0xMDE0OTQAMwAOaLgCLzkxNzEwLTU0MTcsVVNBAEAAC2i4Ai95YW5nLTEwMTQ5NACcADhouAIvblkrc0haMlByQm1kajZ3Vm5ZK3NFWjJQckEyZGo2TUhsb0NwQUpPQm9nbWRqNng5blkrc2VRPT0AnQAIaLgCLzAwMDAwMDAxAMoAIGqZNa80ZTVmNjJiYzE5MTBhYzZhMDYwYTNhMDlmZmY5MTFhMADLAANm1tW3MTcyAWQAB2qZNa8jMDAwMDhhQbxtxho/ZordzpaHG3B7F0S5+VA*',
    'ebay': '%5Ejs%3D1%5Edv%3D66d6ca2b%5Esbf%3D%23000000%5E',
    'bm_sv': '535AED344C69638D2EE0F0E8A6F34C2A~YAAQVlcyuBccu5eRAQAAcF4XtxhkNYQMT0L9Ff7hGwzy6U0dKMAzDjGF3PnZ+TR1EkgN8brnXdrjvXM7Lb0yNkgY0FHocsoTQUCcczbdwRWrfZL40JP3u+oE5Z7/yaohfgpmX7r8bEYVgSTKtH3cVa1Sy6fCE/0ZL4N68yrwoZJX4mBkkKp4UUHns9ilJ2Smtd/+3PV0BLyTPJPb+rKnlm1RYnFJtOKnn741q5KShX24LlAktatKMTBjAOTEMg==~1',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    # 'cookie': '__uzma=6a946330-6f4e-4e0f-bf5b-7f2dc59681cc; __uzmb=1723596762; __uzme=9627; cid=rtGJxMGrMTP6DvvZ%231787088840; __ssds=2; __uzmaj2=cf401a82-2290-4762-bbff-c170c7639448; __uzmbj2=1723596775; __uzmlj2=1wFi4POLMnfGxtNJi/brATI9MbTWgWJarlSEdiFQoi8=; _gcl_au=1.1.1206382020.1724034475; _pin_unauth=dWlkPU1EVTJaR1ZoT1RndE9ETXdZaTAwWmpSaUxXSXdNRGt0WVRnMk1tTXlaRFJqTlRZNA; _fbp=fb.1.1724034477258.158101776588160977; shs=BAQAAAZGG1Rg0AAaAAVUAD2idM4MyMjE4NjUxOTQxMDAzLDIhloZ2mR8IZTgTl6aj38ALmhL8EA**; AMP_MKTG_f93443b04c=JTdCJTdE; __gsas=ID=50a8dc273da81240:T=1725323526:RT=1725323526:S=ALNI_MaQMDqM4jlYWxEvg0dJdoR3wg-H0Q; __ssuzjsr2=a9be2cd8e; ak_bmsc=BF476594CFFF701C9AA91197C90583BD~000000000000000000000000000000~YAAQlVcyuLJnv7ORAQAAE4rTthj+PcMcQx38BVxZ8YGIJLPQ6ZEuKmVZC/hH7De5bz8OpygU7C1v260mOn1r7c0dOLWYRL3WACeE3XRYYZOB3L+YrsyAjjUdYWROOH0lmKv3urz9qlateP2M8lyY6YeWBLXmqx4ZgD+eNoi4CY3TBqjSaWovAED2T3zCXJKvfBZNOORunt2kaaLMGuv7Xukep1ltiZ/Ao/mdBjjGA4bzX6HyvynkB/oqhBc+JCjFzWHPOxdAwuUyOgp155krz6ez9rdhwXkMVz5dd7VD7qC39/dn/kBGAfF3zBmbXY6r9mT0PVJhwE08lEHQrOUpnr9h+b+3mQkcVkJIPsHPtmuadEeFnIZSQOtkB4DlvqH3UE+qgaA=; utag_main__sn=9; utag_main_ses_id=1725352052747%3Bexp-session; utag_main__ss=0%3Bexp-session; _uetsid=cf7d206069cf11ef9cf043a45a3e33a7|1lmnoy3|2|fov|0|1707; _uetvid=af91df805dd211ef9a188581b088cdb8|1238edk|1725352684945|2|1|bat.bing.com/p/insights/c/e; __uzmcj2=3883919937322; __uzmdj2=1725352782; __uzmfj2=7f6000d11bb8f3-0099-435f-9279-b809986d0d4517235967755241756007108-b1ff535434ae4b05199; __deba=9xUzzMmIDQpxF_hROW4vkOEylFZDXiSvD4-cpYf60rsWEf_7IhLDZNZxfRW17gfjJGGSn4EAAKx72GOtZsqSrsfIp8YWLdGXVxFwpDOIJvrxA4VJ0ODuMtxWoLO0ACc5bAieeLuHEc8rx6cup6vwEw==; __uzmc=7793937392683; __uzmd=1725352784; __uzmf=7f6000d11bb8f3-0099-435f-9279-b809986d0d4517235967620891756022327-34409e2c96a74ca7373; utag_main__se=4%3Bexp-session; utag_main__st=1725354647603%3Bexp-session; utag_main__pn=4%3Bexp-session; cto_bundle=MZbpnV9QemhwcVY2QUN1UkVONW85NlNqWlAlMkZMODN4bm5USUV0a2xhc0MlMkZ4ckFtbFJMWElaeTZYYjFQRENwSDBPVU9tejZhalVIYUFZaWdqNDl6bzF6Wm45Y3B0NmZDJTJGT1N6ajhJSmJiWVBMdCUyRjJxJTJCbU16cjRpbFNOdW5zM0tTbjVzb3VwJTJGZXdjR2hBQVlXelpxeXNuRldtSmclM0QlM0Q; __gads=ID=5b30965c3a097cc4:T=1725325695:RT=1725352950:S=ALNI_Ma8Miyz8jcu8d1osoulNDLcU8s4-w; __gpi=UID=00000eea9fba1122:T=1725325695:RT=1725352950:S=ALNI_MbLQEiGoFpmv444j9G6vnYFDJNYhg; s=CgADuAI9m2B3XMwZodHRwczovL3d3dy5lYmF5LmRlL3NjaC9pLmh0bWw/X2Zyb209UjQwJl90cmtzaWQ9cDIzMzQ1MjQubTU3MC5sMTMxMyZfbmt3PUV4aGF1c3QrTWFuaWZvbGQrJl9zYWNhdD0wJl9vZGt3PTE3MTQxNzQyMDAmX29zYWNhdD0wJkxIX1ByZWZMb2M9MQcA+AAgZtgd1zRlNWY2MmJjMTkxMGFjNmEwNjBhM2EwOWZmZjkxMWEwzhnLdQ**; totp=1725353635894.WANjekdMWcGem27SE+ck+HsQ5ikmItyKe63gqdvD53uSaRFp4kefHI7Ot35kK+ZchsIgzYdEZymS9Sj+NaJC2w==.6PdnjPVoBdQ8gZtGMBX3gYxJfbKcKwz6ijbgFZe4m7s; AMP_f93443b04c=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI2NDhiNTk4ZS1jMmEyLTQyMGYtYjViMC0zNTk4NTBkZWRiNmElMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzI1MzQxNjg4MDU4JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTcyNTM1MzY0Nzg2MyUyQyUyMmxhc3RFdmVudElkJTIyJTNBNDc3JTJDJTIycGFnZUNvdW50ZXIlMjIlM0ExNTElN0Q=; dp1=bu1p/eWFuZy0xMDE0OTQ*6a9935af^kms/in6a9935af^pbf/%230000e000e0000000808000000068b8022f^u1f/yangteng6a9935af^tzo/-1e066d6da67^expt/000172359687002767ac9a06^bl/US6a9935af^; ns1=BAQAAAZBR14g6AAaAAKUADWi4Ai8yMzYyODgzMzM1LzA7Zg9du2eSfRLnJ3cD8tQYnMvw9OI*; nonsession=BAQAAAZBR14g6AAaAAAQAC2idM4N5YW5nLTEwMTQ5NAAQAAtouAIveWFuZy0xMDE0OTQAMwAOaLgCLzkxNzEwLTU0MTcsVVNBAEAAC2i4Ai95YW5nLTEwMTQ5NACcADhouAIvblkrc0haMlByQm1kajZ3Vm5ZK3NFWjJQckEyZGo2TUhsb0NwQUpPQm9nbWRqNng5blkrc2VRPT0AnQAIaLgCLzAwMDAwMDAxAMoAIGqZNa80ZTVmNjJiYzE5MTBhYzZhMDYwYTNhMDlmZmY5MTFhMADLAANm1tW3MTcyAWQAB2qZNa8jMDAwMDhhQbxtxho/ZordzpaHG3B7F0S5+VA*; ebay=%5Ejs%3D1%5Edv%3D66d6ca2b%5Esbf%3D%23000000%5E; bm_sv=535AED344C69638D2EE0F0E8A6F34C2A~YAAQVlcyuBccu5eRAQAAcF4XtxhkNYQMT0L9Ff7hGwzy6U0dKMAzDjGF3PnZ+TR1EkgN8brnXdrjvXM7Lb0yNkgY0FHocsoTQUCcczbdwRWrfZL40JP3u+oE5Z7/yaohfgpmX7r8bEYVgSTKtH3cVa1Sy6fCE/0ZL4N68yrwoZJX4mBkkKp4UUHns9ilJ2Smtd/+3PV0BLyTPJPb+rKnlm1RYnFJtOKnn741q5KShX24LlAktatKMTBjAOTEMg==~1',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-full-version': '"128.0.6613.114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}

params = {
    '_from': 'R40',
    '_trksid': 'p2334524.m570.l1313',
    '_nkw': 'Exhaust Manifold ',
    '_sacat': '0',
    '_odkw': '1714174200',
    '_osacat': '0',
    'LH_PrefLoc': '1',
}

response = requests.get('https://www.ebay.de/sch/i.html', params=params, cookies=cookies, headers=headers)
print(response.text)