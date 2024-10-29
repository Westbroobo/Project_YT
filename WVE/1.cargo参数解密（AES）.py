"""
Filename:1.cargo参数解密（AES）.py
Author: Westbroobo
Date: 2024/9/4
"""

import execjs
import pandas as pd

df = pd.read_excel('./WVE_partno.xlsx')
Part_Number = df['Part Number'].tolist()

js_code = """
    function _interopRequireDefault(obj) {
        return obj && obj.__esModule ? obj : {
            "default": obj
        };
    }
    var _cryptoJs = _interopRequireDefault(require("crypto-js"));
    function getEncryptedParams(params) {
        var ciphertext = _cryptoJs.default.AES.encrypt(params, 'WkFenfbPU83k9X86EPQISy/M7po=').toString();
        var encodedCiphertext = encodeURIComponent(ciphertext);
        return encodedCiphertext;
    }
"""

part_ls = []
cargo_ls = []
for part_number in Part_Number:
    param = 'lookup=partdetailfull&partno=' + part_number + "&id=WELLS2182"
    context = execjs.compile(js_code)
    cargo = context.call('getEncryptedParams', param)
    # url = 'https://www.showmethepartsdb2.com/bin/ShowMeConnect.exe?cargo=' + cargo
    part_ls.append(part_number)
    cargo_ls.append(cargo)

df = pd.DataFrame(columns=['Part_Number', 'cargo'])
df['Part_Number'] = part_ls
df['cargo'] = cargo_ls
df.to_excel('./WVE_cargo.xlsx', index=False)



