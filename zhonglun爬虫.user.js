// ==UserScript==
// @name         zhonglun爬虫
// @namespace    http://tampermonkey.net/
// @version      2023.09.15
// @description  爬虫
// @author       Westbroobo
// @match        *://www.zhonglun.com/zyry.html?*
// @icon         https://www.zhonglun.com/Template/cn/images/favicon.ico
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    function scrollToBottom() {
        window.scrollTo(0, document.body.scrollHeight);
    }

    const data = { Name: [], Url: [] };
    let currentPage = 1; // 当前页数

    function selectElementsByXPath(xpath) {
        const elements = [];
        const xpathResult = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);

        for (let i = 0; i < xpathResult.snapshotLength; i++) {
            elements.push(xpathResult.snapshotItem(i));
        }

        return elements;
    }

    function extractData() {
        const lis = selectElementsByXPath('/html/body/div[1]/div[5]/div/div[3]/div/ul/li');
        lis.forEach((li) => {
            const t = li.textContent;
            const name = t.split('\n')[5];
            const a = li.querySelector('a');
            const url = 'https://www.zhonglun.com'+ a.getAttribute('href');
            data.Name.push(name);
            data.Url.push(url);
        });
    }

    function scrollAndExtract() {
        scrollToBottom();
        setTimeout(() => {
            extractData();
            const nextPageButton = document.querySelector('body > div.lm_box > div.warp > div > div.news_main.yr_list.SYCms_Tem_PageList_15 > div > div > div > span.PEnd > a');
            if (nextPageButton && currentPage<3) { //根据需要自定义滚动次数或条件
                nextPageButton.click();
                currentPage++;
                setTimeout(scrollAndExtract, 2000);
            } else {
                console.log(`数据提取完成，共 ${currentPage} 页`);
                let json_content = JSON.stringify(data);
                // console.log(json_content);

                let blob_data = new Blob([json_content], {type: 'text/plain'});
                let blob_url = URL.createObjectURL(blob_data);
                let blob_link = document.createElement('a');
                blob_link.href = blob_url;
                blob_link.download = 'catalogue.txt';
                blob_link.click();
                URL.revokeObjectURL(blob_url);

            }
        }, 2000); // 等待一段时间以确保内容加载完成
    }

    scrollAndExtract();
})();