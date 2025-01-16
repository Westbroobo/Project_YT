// ==UserScript==
// @name         eBay车型爬虫240207(无限速)
// @namespace    http://tampermonkey.net/
// @version      2024-02-07
// @description  提取车型表整理成make+model+year形式
// @author       Westbroobo
// @match        *://www.ebay.com/itm/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=ebay.com
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
     fetch('https://api.ipify.org?format=json')
        .then(response => response.json())
        .then(data => console.log('当前请求的IP地址：', data.ip))
        .catch(error => console.error('获取IP地址时出错：', error));
    console.log('当前的User Agent：', navigator.userAgent);
    let HTMLCollection_item = document.getElementsByClassName('ux-layout-section__textual-display ux-layout-section__textual-display--itemId');
    let HTMLCollection_vehicle_number = document.getElementsByClassName('textual-display motors-compatibility-table__details-text');
    let item = HTMLCollection_item[0].innerText.slice(17);
    let vehicle_number = HTMLCollection_vehicle_number[0].innerText.slice(29);
    vehicle_number = parseFloat(vehicle_number.substr(0, vehicle_number.length - 11));
    let page = Math.ceil(vehicle_number/20);
    const data = JSON.stringify({
        'scopedContext': {
            'catalogDetails': {
                'itemId': item,
                'categoryId': '33590',
                'marketplaceId': 'EBAY-US'
            }
        }
    });
    let vehicle_data = { Make_Model: [], Year: [] };
    for (var i = 0; i < page; i++) {
        let xhr = new XMLHttpRequest();
        let url = 'https://www.ebay.com/g/api/finders?module_groups=PART_FINDER&referrer=VIEWITEM&offset=' + i*20 + '&module=COMPATIBILITY_TABLE';
        xhr.withCredentials = true;
        xhr.open('POST', url);
        xhr.setRequestHeader('authority', 'www.ebay.com');
        xhr.setRequestHeader('accept', 'application/json');
        xhr.setRequestHeader('accept-language', 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6');
        xhr.setRequestHeader('cache-control', 'max-age=0');
        xhr.setRequestHeader('content-type', 'application/json');
        xhr.setRequestHeader('x-ebay-answers-request', 'pageci=800a0d21-b709-46c7-bd66-cb8c6ff5da68,parentrq=81000a8d18d0a45e7634ac67ffee61b2');
        xhr.setRequestHeader('x-ebay-c-correlation-session', 'operationId=4429486');
        xhr.setRequestHeader('x-ebay-c-tracking-config', 'viewTrackingEnabled=true,perfTrackingEnabled=true,navTrackingEnabled=true,navsrcTrackingEnabled=true,swipeTrackingEnabled=false,showDialogTrackingEnabled=true');
        xhr.onload = function() {
            let response = JSON.parse(xhr.response);
            let rows = response.modules.COMPATIBILITY_TABLE.paginatedTable.rows
            rows.forEach(row =>{
                let year = row.cells[0].textSpans[0].text
                let make = row.cells[1].textSpans[0].text
                let model = row.cells[2].textSpans[0].text
                let make_model = make + ' ' + model
                vehicle_data.Make_Model.push(make_model);
                vehicle_data.Year.push(year);
                if (vehicle_data.Year.length === vehicle_number) {
                    var result = [];
                    function findEntry(array, makeModel) {
                        return array.find(function (entry) {
                            return entry.makeModel === makeModel;
                        });
                    }
                    for (var j = 0; j < vehicle_data.Make_Model.length; j++) {
                        var makeModel = vehicle_data.Make_Model[j];
                        var year2 = parseInt(vehicle_data.Year[j]);
                        var existingEntry = findEntry(result, makeModel);
                        if (!existingEntry) {
                            result.push({
                                makeModel: makeModel,
                                minYear: year2,
                                maxYear: year2,
                            });
                        } else {
                            if (year2 < existingEntry.minYear) {
                                existingEntry.minYear = year2;
                            }
                            if (year2 > existingEntry.maxYear) {
                                existingEntry.maxYear = year2;
                            }
                        }
                    }
                    result.sort((a, b) => a.makeModel.localeCompare(b.makeModel));
                    var finalresult = result.map(function (entry) {
                        if (entry.minYear === entry.maxYear) {
                            return entry.makeModel + " " + entry.minYear;
                        } else {
                            return entry.makeModel + " " + entry.minYear + "-" + entry.maxYear;
                        }
                    });
                    console.log(vehicle_data);
                    console.log(finalresult);
                    var tablehtml = '<table style="border: 1px solid #ddd; background-color: #f5f5f5; margin: 0 auto; font-size: 16px; text-align: center"><thead style="font-size: 18px; font-weight: bold; background-color: #007bff; color: white"><tr><th><div style="text-align: center">Make_Model_Year</div></th></tr></thead><tbody>';
                    finalresult.forEach(function(part) {
                        tablehtml += '<tr><td style="padding: 8px;">' + part + '</td></tr>';
                    });
                    tablehtml += '</tbody></table><br/><br>';
                    document.querySelector(".motors-compatibility-table-wrapper").insertAdjacentHTML("beforebegin", tablehtml);
                };
            })
        };
        xhr.send(data);
    }
})();