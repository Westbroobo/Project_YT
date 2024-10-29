import zipfile

username = 't12843555897085'
password = '0jp3brru'
tunnel_host = 'b397.kdltps.com'
tunnel_port = 15818

def get_Proxy_Requests():
    return {'http': f'http://{username}:{password}@{tunnel_host}:{tunnel_port}',
            'https': f'http://{username}:{password}@{tunnel_host}:{tunnel_port}'}

def get_Proxy_Selenium():
    manifest_json = '''{"version": "1.0.0",
                                "manifest_version": 2,
                                "name": "Chrome Proxy",
                                "permissions": ["proxy",
                                                "tabs",
                                                "unlimitedStorage",
                                                "storage",
                                                "<all_urls>",
                                                "webRequest",
                                                "webRequestBlocking"],
                                "background": {"scripts": ["background.js"]},
                                "minimum_chrome_version": "22.0.0"}'''

    background_js = f'''var config = {{mode: "fixed_servers",
                                               rules: {{singleProxy: {{scheme: "http",
                                                                       host: "{tunnel_host}",
                                                                       port: {tunnel_port}}},
                                               bypassList: ["foobar.com"]}}}};

                                chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

                                function callbackFn(details) {{
                                    return {{authCredentials: {{username: "{username}",
                                                                password: "{password}"}}}};}}

                                chrome.webRequest.onAuthRequired.addListener(callbackFn,
                                                                             {{urls: ["<all_urls>"]}},
                                                                             ['blocking']);'''

    with zipfile.ZipFile('./vimm_chrome_proxyauth_plugin.zip', 'w') as zp:
        zp.writestr('manifest.json', manifest_json)
        zp.writestr('background.js', background_js)

    return './vimm_chrome_proxyauth_plugin.zip'



