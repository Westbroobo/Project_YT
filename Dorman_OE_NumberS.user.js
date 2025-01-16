// ==UserScript==
// @name         Dorman_OE_NumberS
// @namespace    http://tampermonkey.net/
// @version      2023.11.29
// @description  rockauto_oe号获取
// @author       Westbroobo
// @match        *://www.dormanproducts.com/p*
// @icon         https://static.dormanproducts.com/images/marketing/homepage/dorman-logo-white.png
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    function selectElementsByXPath(xpath) {
        const elements = [];
        const xpathResult = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);

        for (let i = 0; i < xpathResult.snapshotLength; i++) {
            elements.push(xpathResult.snapshotItem(i));
        }

        return elements;
    }

    window.copyToClipboard = function (text) {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
    }

    const oesArray = [];
    const trs = selectElementsByXPath('//*[@id="productOE"]/div/table/tbody/tr')
    trs.forEach((tr) => {
        let th = document.evaluate('./th', tr, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
        let oe = th.singleNodeValue.innerText.replace(/-/g, '').replace(/ +/g,'');
        oesArray.push(oe);
    });
    var oes = '';
    oesArray.forEach((o) => {
        oes = oes + ';' + o
    });
    const result_oes = oes.slice(1);
    var content = '<table style="background-color: #f4f4f4;display: inline-block; font-size: 16px; text-align: center"><thead style="font-size: 18px; font-weight: bold; background-color: #464646; color: white"><th><div style="text-align: center">OE Numbers</div></th></thead><tbody><td onclick="copyToClipboard(\'' + result_oes + '\')" style="padding: 8px; sans-serif; cursor: pointer; user-select: all; max-height: 100px; max-width: 1000px;overflow: auto; white-space: pre-wrap;">' + result_oes + '</td></tbody></table><br/><br>';
    document.querySelector(".productImgThumb").insertAdjacentHTML("afterend", content);

})();
