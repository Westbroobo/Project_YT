// ==UserScript==
// @name         原厂车型描述2023
// @namespace    http://tampermonkey.net/
// @version      2024.09.12
// @description  原厂车型整理
// @author       Westbroobo
// @match        *://www.oemfordpart.com/oem-parts/*
// @match        *://www.subaruparts.com/oem-parts*
// @match        *://www.hyundaioempartsdirect.com/oem-parts*
// @match        *://www.mazda-parts.com/oem-parts*
// @match        *://www.lexusoeparts.com/oem-parts*
// @match        *://www.oemgenuineparts.com/oem-parts*
// @match        *://www.moparpartsproonline.com/oem-parts/*
// @match        *://www.gmpartsdirect.com/oem-parts/*
// @match        *://www.kiaparts.com/oem-parts/*
// @match        *://www.hondapartsonline.net/oem-parts*
// @match        *://www.vwpartsvortex.com/oem-parts*
// @match        *://www.genuineaudiparts.com/oem-parts/audi*
// @match        *://www.bmwpartsdirect.com/oem-parts/bmw*
// @match        *://www.getbmwparts.com/oem-parts/*
// @match        *://www.minipartsdirect.com/oem-parts/mini*
// @match        *://www.volvowholesaleparts.com/oem-parts*
// @match        *://www.oemacuraparts.com/oem-parts/acura*
// @match        *://www.oemacuraparts.com/oem-parts/honda*
// @match        *://www.myswedishparts.com/oem-parts/volvo*
// @match        *://www.mitsubishiparts.com/oem-parts/*
// @match        *://www.mercedesbenzpartscenter.com/oem-parts/*
// @match        *.oempartsonline.com/oem-parts/*
// @match        *://www.jaguarparts.com/oem-parts/*
// @match        *://mbparts.mbusa.com/oem-parts/*
// @match        *://www.group1autoparts.com/oem-parts/*
// @icon         https://static.runoob.com/images/c-runoob-logo.ico
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    window.scrollTo(0, document.body.scrollHeight);
    const data = { Make_Model: [], Make_Model_Engine: [], Year: [], Engine:[], Make__Model:[] };
    const xpath_hidden_1 = document.querySelector('#layout_product > div > div > div:nth-child(4) > div > div > div > div > div:nth-child(4) > div > div > div > a');
    const xpath_hidden_2 = document.querySelector('#layout_product > div > div > div:nth-child(4) > div > div > div > div > div:nth-child(3) > div > div > div > a');
    const xpath_hidden_3 = document.querySelector('#layout_product > div > div > div:nth-child(4) > div > div > div > div > div:nth-child(3) > div:nth-child(2) > div > div > div > a');
    const xpath_hidden_4 = document.querySelector('#layout_product > div > div > div:nth-child(4) > div > div > div > div > div:nth-child(4) > div:nth-child(2) > div.product-fitment-module > div > div > a');

    function selectElementsByXPath(xpath) {
        const elements = [];
        const xpathResult = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);

        for (let i = 0; i < xpathResult.snapshotLength; i++) {
            elements.push(xpathResult.snapshotItem(i));
        }

        return elements;
    }

    function extractData_1() {
        const trs = selectElementsByXPath('//*[@id="layout_product"]/div/div/div[4]/div/div/div/div/div[4]/div/div/div/table/tbody/tr');
        trs.forEach((tr) => {
            const text = tr.outerText;
            const td = text.split('\t');
            const year = td[0];
            const engines_all = td[4].split(', ');
            const make_model = td[1] + ' ' + td[2];
            const make_model2 = td[1] + '+' + td[2];
            var engine_result = ''
            engines_all.forEach(e =>{
                const engines_separated = e.split(" ");
                if (!engine_result.includes(engines_separated[0] + ' ' + engines_separated[1])){
                    engine_result += '/' + engines_separated[0] + ' ' + engines_separated[1];
                }
            })
            if (engine_result.includes('Electric')){
                engine_result = engine_result.replace(' undefined', '');
            } else{
                engine_result = engine_result.slice(1);
            };
            const make_model_engine = td[1] + '+' + td[2] + '+' + engine_result;
            data.Make_Model_Engine.push(make_model_engine);
            data.Make_Model.push(make_model);
            data.Year.push(year);
            data.Engine.push(engine_result);
            data.Make__Model.push(make_model2);
        });
    }

    function extractData_2() {
        const trs = selectElementsByXPath('//*[@id="layout_product"]/div/div/div[4]/div/div/div/div/div[3]/div/div/div/table/tbody/tr');
        trs.forEach((tr) => {
            const text = tr.outerText;
            const td = text.split('\t');
            const year = td[0];
            const engines_all = td[4].split(', ');
            const make_model = td[1] + ' ' + td[2];
            const make_model2 = td[1] + '+' + td[2];
            var engine_result = ''
            engines_all.forEach(e =>{
                const engines_separated = e.split(" ");
                if (!engine_result.includes(engines_separated[0] + ' ' + engines_separated[1])){
                    engine_result += '/' + engines_separated[0] + ' ' + engines_separated[1];
                }
            })
            if (engine_result.includes('Electric')){
                engine_result = engine_result.replace(' undefined', '');
            } else{
                engine_result = engine_result.slice(1);
            };
            const make_model_engine = td[1] + '+' + td[2] + '+' + engine_result;
            data.Make_Model_Engine.push(make_model_engine);
            data.Make_Model.push(make_model);
            data.Year.push(year);
            data.Engine.push(engine_result);
            data.Make__Model.push(make_model2);
        });
    }

    function extractData_3() {
        const trs = selectElementsByXPath('//*[@id="layout_product"]/div/div/div[4]/div/div/div/div/div[3]/div[2]/div/div/div/table/tbody/tr');
        trs.forEach((tr) => {
            const text = tr.outerText;
            const td = text.split('\t');
            const year = td[0];
            const engines_all = td[4].split(', ');
            const make_model = td[1] + ' ' + td[2];
            const make_model2 = td[1] + '+' + td[2];
            var engine_result = ''
            engines_all.forEach(e =>{
                const engines_separated = e.split(" ");
                if (!engine_result.includes(engines_separated[0] + ' ' + engines_separated[1])){
                    engine_result += '/' + engines_separated[0] + ' ' + engines_separated[1];
                }
            })
            if (engine_result.includes('Electric')){
                engine_result = engine_result.replace(' undefined', '');
            } else{
                engine_result = engine_result.slice(1);
            };
            const make_model_engine = td[1] + '+' + td[2] + '+' + engine_result;
            data.Make_Model_Engine.push(make_model_engine);
            data.Make_Model.push(make_model);
            data.Year.push(year);
            data.Engine.push(engine_result);
            data.Make__Model.push(make_model2);
        });
    }

    function extractData_4() {
        const trs = selectElementsByXPath('//*[@id="layout_product"]/div/div/div[4]/div/div/div/div/div[4]/div[2]/div/div/div/table/tbody/tr');
        trs.forEach((tr) => {
            const text = tr.outerText;
            const td = text.split('\t');
            const year = td[0];
            const engines_all = td[4].split(', ');
            const make_model = td[1] + ' ' + td[2];
            const make_model2 = td[1] + '+' + td[2];
            var engine_result = ''
            engines_all.forEach(e =>{
                const engines_separated = e.split(" ");
                if (!engine_result.includes(engines_separated[0] + ' ' + engines_separated[1])){
                    engine_result += '/' + engines_separated[0] + ' ' + engines_separated[1];
                }
            })
            if (engine_result.includes('Electric')){
                engine_result = engine_result.replace(' undefined', '');
            } else{
                engine_result = engine_result.slice(1);
            };
            const make_model_engine = td[1] + '+' + td[2] + '+' + engine_result;
            data.Make_Model_Engine.push(make_model_engine);
            data.Make_Model.push(make_model);
            data.Year.push(year);
            data.Engine.push(engine_result);
            data.Make__Model.push(make_model2);
        });
    }

    if (xpath_hidden_1) {
        xpath_hidden_1.click();
        extractData_1();
    } else if (xpath_hidden_2) {
        xpath_hidden_2.click();
        extractData_2();
    } else if (xpath_hidden_3) {
        xpath_hidden_3.click();
        extractData_3();
    }else if (xpath_hidden_4) {
        xpath_hidden_4.click();
        extractData_4();
    }

    extractData_1();
    extractData_2();
    extractData_3();
    extractData_4();
/*
    function processCarData(data) {
        var result1 = [];
        for (var i = 0; i < data.Make_Model_Engine.length; i++) {
            var makeModel = data.Make_Model[i];
            var makeModelEngine = data.Make_Model_Engine[i];
            var year = parseInt(data.Year[i]);
            var existingEntry = result1.find(function (entry) {
                return entry.makeModelEngine === makeModelEngine;
            });

            if (!existingEntry) {
                result1.push({
                    makeModelEngine: makeModelEngine,
                    minYear: year,
                    maxYear: year,
                });
            } else {
                if (year < existingEntry.minYear) {
                    existingEntry.minYear = year;
                }
                if (year > existingEntry.maxYear) {
                    existingEntry.maxYear = year;
                }
            }
        }
        result1.sort((a, b) => a.makeModelEngine.localeCompare(b.makeModelEngine));
        var finalResult1 = result1.map(function (entry) {
            if (entry.minYear === entry.maxYear) {
                return entry.makeModelEngine + "+" + entry.minYear;
            } else {
                return entry.makeModelEngine + "+" + entry.minYear + "-" + entry.maxYear;
            }
        });
        return finalResult1;
    }*/

    function processCarData(data) {
        var result1 = [];
        for (var i = 0; i < data.Make__Model.length; i++) {
            var makeModel = data.Make__Model[i];
            var engine = data.Engine[i];
            var year = parseInt(data.Year[i]);
            var existingEntry = result1.find(function (entry) {
                return entry.makeModel === makeModel;
            });

            if (!existingEntry) {
                result1.push({
                    makeModel: makeModel,
                    minYear: year,
                    maxYear: year,
                    engine: engine
                });
            } else {
                if (year < existingEntry.minYear) {
                    existingEntry.minYear = year;
                    existingEntry.engine = existingEntry.engine + '/' + engine
                }
                if (year > existingEntry.maxYear) {
                    existingEntry.maxYear = year;
                    existingEntry.engine = existingEntry.engine + '/' + engine
                }
            }
        }
        result1.sort((a, b) => a.makeModel.localeCompare(b.makeModel));
        var finalResult1 = result1.map(function (entry) {
            const array_engine = entry.engine.split('/').sort();
            var engine_integration = '';
            array_engine.forEach((e) => {
                if (engine_integration.includes(e)){
                    engine_integration = engine_integration;
                } else{
                    engine_integration = engine_integration + '/' + e;
                }
            })
            if (entry.minYear === entry.maxYear) {
                return entry.makeModel + "+" + engine_integration.slice(1) + "+" + entry.minYear;
            } else {
                return entry.makeModel + "+" + engine_integration.slice(1) + "+" + entry.minYear + "-" + entry.maxYear;
            }
        });
        return finalResult1;
    }


    function processCarData2(data) {
        var result2 = [];
        for (var i = 0; i < data.Make_Model.length; i++) {
            var makeModel = data.Make_Model[i];
            var year = parseInt(data.Year[i]);
            var existingEntry2 = result2.find(function (entry) {
                return entry.makeModel === makeModel;
            });

            if (!existingEntry2) {
                result2.push({
                    makeModel: makeModel,
                    minYear: year,
                    maxYear: year,
                });
            } else {
                if (year < existingEntry2.minYear) {
                    existingEntry2.minYear = year;
                }
                if (year > existingEntry2.maxYear) {
                    existingEntry2.maxYear = year;
                }
            }
        }

        result2.sort((a, b) => a.makeModel.localeCompare(b.makeModel));
        var finalResult2 = result2.map(function (entry) {
            if (entry.minYear === entry.maxYear) {
                return entry.makeModel + " " + entry.minYear;
            } else {
                return entry.makeModel + " " + entry.minYear + "-" + entry.maxYear;
            }
        });

        return finalResult2;
    }

    var processedData = processCarData(data);
    var processedData2 = processCarData2(data);
    const list_make = [];
    const list_model = [];
    const list_engine = [];
    const list_year = [];
    processedData.forEach(data => {
        const separated_data = data.split("+");
        list_make.push(separated_data[0]);
        list_model.push(separated_data[1]);
        list_year.push(separated_data[3]);
        list_engine.push(separated_data[2]);
    });

    var tablehtml1 = '<div class="tablehtml1" style="text-align: center !important;"><table style="border-collapse: collapse; width: 70%; margin: 0 auto;"><thead style="background-color: #f2f2f2; text-align: center;"><tr><th style="border: 1px solid #dddddd; padding: 8px;">Make</th><th style="border: 1px solid #dddddd; padding: 8px;">Model</th><th style="border: 1px solid #dddddd; padding: 8px;">Year</th><th style="border: 1px solid #dddddd; padding: 8px;">Engine</th></tr></thead><tbody>';
    for (let i = 0; i < list_make.length; i++) {
        tablehtml1 += "<tr><td style='border: 1px solid #dddddd; text-align: left; padding: 8px;'>" + list_make[i] + "</td><td style='border: 1px solid #dddddd; text-align: left; padding: 8px;'>" + list_model[i] + "</td><td style='border: 1px solid #dddddd; text-align: left; padding: 8px;'>" + list_year[i] + "</td><td style='border: 1px solid #dddddd; text-align: left; padding: 8px;'>" + list_engine[i] + "</td></tr>";
    };
    tablehtml1 += "</tbody></table></div>";
    document.querySelector(".product-fitment-module").insertAdjacentHTML("beforebegin", tablehtml1);

    var tablehtml2 = '<table style="border: 1px solid #ddd; background-color: #f5f5f5; margin: 0 auto; font-size: 16px; text-align: center"><thead style="font-size: 18px; font-weight: bold; background-color: #007bff; color: white"><tr><th><div style="text-align: center">Make_Model_Year</div></th></tr></thead><tbody>';
    processedData2.forEach(function(item) {
        tablehtml2 += '<tr><td style="padding: 8px;">' + item + '</td></tr>';
    });
    tablehtml2 += '</tbody></table><br/><br>';
    document.querySelector(".tablehtml1").insertAdjacentHTML("beforebegin", tablehtml2);
    function scrollToTop() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }
scrollToTop();

})();