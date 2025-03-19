// ==UserScript==
// @name         原厂信息整理
// @namespace    http://tampermonkey.net/
// @version      2025.03.19
// @description  原厂信息整理
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
// @match        *://www.isuzupartscenter.com/oem-parts/*
// @match        *://www.suzukicarparts.com/oem-parts/*
// @match        *://www.sunsetporscheparts.com/oem-parts/*
// @match        *://www.mercedesbenzpartsstore.com/oem-parts/*
// @icon         https://d354nuoz4t18d4.cloudfront.net/b386922f390fb1fe8a94c5e73280e85b/images/image-favicon.ico
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    let URL = window.location.origin + window.location.pathname;
    let OE = '';
    let Replaces = '';
    let SKU_Element = document.getElementsByClassName('list-value sku-display');
    let SKU = SKU_Element[0].innerText;
    let Replaces_Element = document.getElementsByClassName('product-superseded-list');
    if(Replaces_Element.length === 0) {
        OE = SKU
    } else {
        Replaces = Replaces_Element[0].innerText.replace('Replaces:\t','').replace(', ',';');
        OE = SKU + ';' + Replaces
    }

    let productDataElement = document.getElementById('product_data');
    let jsonText = productDataElement .textContent;
    let productData = JSON.parse(jsonText);
    let fitments = productData.fitment;

    let data = { Make_Model: [], Year: [], Engine:[], Make__Model:[], Make_Model_Year:[] };
    fitments.forEach((fitment) => {
        const year = fitment.year;
        const engines_all = fitment.engines.join(', ');
        const make_model = fitment.make + ' ' + fitment.model;
        const make_model2 = fitment.make + '#' + fitment.model;
        const make_model_year = fitment.make + '#' + fitment.model + ' ' + fitment.year;
        data.Make_Model.push(make_model);
        data.Year.push(year);
        data.Engine.push(engines_all);
        data.Make__Model.push(make_model2);
        data.Make_Model_Year.push(make_model_year);
    });

    window.copyToClipboard = function (text) {
        const textarea = document.createElement('textarea');
        const value = text.replace(/, /g, ';').replace(/,/g, '\n').replace(/#/g, ' ');
        textarea.value = value.replace(/;/g, ', ');
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
    }

    window.copyToClipboard_2 = function (text) {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
    }

    function getUniqueEngines(engineStr) {
        const array_engine = engineStr.split(', ').sort();
        const uniqueEngines = [...new Set(array_engine)];
        return uniqueEngines.join(', ');
    }

    function getYearRanges(years) {
        const yearRanges = [];
        let start = 0;
        for (let i = 0; i < years.length; i++) {
            if (i === years.length - 1) {
                if (start === i) {
                    yearRanges.push(years[i].toString());
                } else {
                    yearRanges.push(years[start] + '-' + years[i]);
                }
                break;
            }
            if (years[i + 1] - years[i] === 1) {
                continue;
            } else {
                if (start === i) {
                    yearRanges.push(years[i].toString());
                } else {
                    yearRanges.push(years[start] + '-' + years[i]);
                }
                start = i + 1;
            }
        }
        return yearRanges;
    }

    function processCarData(data) {
        var result1 = [];
        for (var i = 0; i < data.Make__Model.length; i++) {
            let makeModel = data.Make__Model[i];
            let engine = data.Engine[i];
            let year = parseInt(data.Year[i]);
            let existingEntry = result1.find(function (entry) {
                return entry.makeModel === makeModel;
            });

            if (!existingEntry) {
                result1.push({
                    makeModel: makeModel,
                    years: [year],
                    engine: engine
                });
            } else {
                existingEntry.years.push(year);
                existingEntry.engine = existingEntry.engine + ', ' + engine;
            }
        }
        result1.sort((a, b) => a.makeModel.localeCompare(b.makeModel));
        var finalResult1 = [];
        result1.forEach((entry) => {
            const engine_integration = getUniqueEngines(entry.engine);
            entry.years.sort((a, b) => a - b);
            const yearRanges = getYearRanges(entry.years);

            if (yearRanges.length === 1 || yearRanges.includes('-')) {
                finalResult1.push(entry.makeModel + "#" + yearRanges[0] + "#" + engine_integration);
            } else if (yearRanges.length > 1) {
                yearRanges.forEach((yearRange) => {
                    if (yearRange.includes('-')){
                        let array_year = yearRange.split('-')
                        let engine_integration2 = [];
                        for (let i = parseInt(array_year[0]); i <= parseInt(array_year[1]); i++) {
                            const m_m_y = entry.makeModel + ' '+ i
                            const index_ = data.Make_Model_Year.indexOf(m_m_y);
                            engine_integration2.push(data.Engine[index_])
                        };
                        engine_integration2 = engine_integration2.join(', ').split(', ');
                        let engine_integration = [...new Set(engine_integration2)];
                        engine_integration = engine_integration.join(', ');
                        finalResult1.push(entry.makeModel + "#" + yearRange + "#" + engine_integration);
                    } else {
                        const index = data.Make_Model_Year.indexOf(entry.makeModel + ' '+ yearRange);
                        const engine_integration_1 = data.Engine[index];
                        finalResult1.push(entry.makeModel + "#" + yearRange + "#" + engine_integration_1);
                    }
                });
            }
        });
        return finalResult1;
    }

    function processCarData2(data) {
        var result2 = [];
        for (var i = 0; i < data.Make_Model.length; i++) {
            let makeModel = data.Make_Model[i];
            let year = parseInt(data.Year[i]);
            let existingEntry = result2.find(function (entry) {
                return entry.makeModel === makeModel;
            });
            if (!existingEntry) {
                result2.push({
                    makeModel: makeModel,
                    years: [year],
                });
            } else {
                existingEntry.years.push(year);
            }
        }

        result2.sort((a, b) => a.makeModel.localeCompare(b.makeModel));
        var finalResult2 = [];
        result2.forEach((entry) => {
            entry.years.sort((a, b) => a - b);
            const yearRanges = getYearRanges(entry.years);
            if (yearRanges.length === 1) {
                finalResult2.push(entry.makeModel + " " + yearRanges[0]);
            } else if (yearRanges.length > 1) {
                yearRanges.forEach((yearRange) => {
                    finalResult2.push(entry.makeModel + " " + yearRange);
                });
            }
        });
        return finalResult2;
    }

    var processedData = processCarData(data);
    var processedData2 = processCarData2(data);

    var engineData = [...new Set(data.Engine.sort())].join(', ');
    var copyengineData = [...new Set(engineData.split(', '))].sort();
    engineData = copyengineData.join('\n');

    let Vehicle = processedData2.join('\n');

    let list_make = [];
    let list_model = [];
    let list_engine = [];
    let list_year = [];
    processedData.forEach(data => {
        let separated_data = data.split("#");
        list_make.push(separated_data[0]);
        list_model.push(separated_data[1]);
        list_year.push(separated_data[2]);
        list_engine.push(separated_data[3]);
    });

    var tablehtml1 = `<div class="tablehtml1">
                         <table style="border-collapse: collapse; width: 100%; margin: 0 auto;">
                             <thead style="background-color: #E0E0E0;">
                                 <tr>
                                     <th onclick="copyToClipboard('${processedData}')" style="border: 1px solid #dddddd; padding: 8px; text-align: center; cursor: pointer; user-select: all;">Make</th>
                                     <th onclick="copyToClipboard('${processedData}')" style="border: 1px solid #dddddd; padding: 8px; text-align: center; cursor: pointer; user-select: all;">Model</th>
                                     <th onclick="copyToClipboard('${processedData}')" style="border: 1px solid #dddddd; padding: 8px; text-align: center; cursor: pointer; user-select: all;">Year</th>
                                     <th onclick="copyToClipboard('${processedData}')" style="border: 1px solid #dddddd; padding: 8px; text-align: center; cursor: pointer; user-select: all;">Engine & Transmission</th>
                                 </tr>
                            </thead><tbody>`;

    for (let i = 0; i < list_make.length; i++) {
        tablehtml1 += "<tr><td style='border: 1px solid #dddddd; padding: 8px; text-align: center;'>" + list_make[i] +
                      "</td><td style='border: 1px solid #dddddd; padding: 8px; text-align: center;'>" + list_model[i] +
                      "</td><td style='border: 1px solid #dddddd; padding: 8px; text-align: center;'>" + list_year[i] +
                      "</td><td style='border: 1px solid #dddddd; padding: 8px; text-align: center;'>" + list_engine[i] + "</td></tr>";
    };
    tablehtml1 += "</tbody></table></div>";
    document.querySelector(".product-fitment-module").insertAdjacentHTML("beforebegin", tablehtml1);

    var tablehtml2 = `<table style="border: 1px solid #ddd; background-color: #f5f5f5; margin: 0 auto; text-align: center; width: 100%; ">
                          <thead style="background-color: #E0E0E0; font-size: 15px;">
                              <tr>
                                  <th onclick="copyToClipboard('${processedData2}')" style="text-align: center; border: 1px solid #dddddd; padding: 8px; cursor: pointer; user-select: all;">Make_Model_Year</th>
                                  <th onclick="copyToClipboard('${copyengineData}')" style="text-align: center; border: 1px solid #dddddd; padding: 8px; cursor: pointer; user-select: all;">Engine & Transmission</th>
                              </tr>
                          </thead>
                          <tbody>`;

    tablehtml2 += '<tr><td style="padding: 8px; white-space: pre-line; line-height: 1.7; font-size: 15px;border: 1px solid #dddddd;">' + Vehicle + '</td>';
    tablehtml2 += '<td style="padding: 8px; white-space: pre-line; line-height: 1.7; font-size: 15px;border: 1px solid #dddddd;">' + engineData + '</td></tr>';
    tablehtml2 += '</tbody></table><br/><br>';
    document.querySelector(".tablehtml1").insertAdjacentHTML("beforebegin", tablehtml2);

    var tablehtml3 = `<table style="border: 1px solid #ddd; background-color: #f5f5f5; margin: 0 auto; text-align: center; width: 100%;">

                          <tr>
                              <td style=" border: 1px solid #dddddd;; padding: 8px; text-align: center; font-weight: bold; font-size: 13px;">SKU</td>
                              <td onclick="copyToClipboard_2('${SKU}')" style=" border: 1px solid #ddd; padding: 8px; text-align: center; font-size: 12.5px; cursor: pointer; user-select: all;">${SKU}</td>
                          </tr>
                          <tr>
                              <td style=" border: 1px solid #dddddd;; padding: 8px; text-align: center; font-weight: bold;; font-size: 13px;">Replaces</td>
                              <td onclick="copyToClipboard_2('${Replaces}')" style=" border: 1px solid #ddd; padding: 8px; text-align: center; font-size: 12.5px; cursor: pointer; user-select: all;">${Replaces}</td>
                          </tr>
                          <tr>
                             <td style=" border: 1px solid #dddddd;; padding: 8px; text-align: center; font-weight: bold;; font-size: 13px;">OE</td>
                             <td onclick="copyToClipboard_2('${OE}')" style=" border: 1px solid #ddd; padding: 8px; text-align: center; font-size: 12.5px; cursor: pointer; user-select: all;">${OE}</td>
                          </tr>
                          <tr>
                              <td style=" border: 1px solid #dddddd;; padding: 8px; text-align: center; font-weight: bold;; font-size: 13px;">URL</td>
                              <td onclick="copyToClipboard_2('${URL}')" style=" border: 1px solid #ddd; padding: 8px; text-align: center; font-size: 12.5px; cursor: pointer; user-select: all;">${URL}</td>
                          </tr>
                      </table>`;
    document.querySelector(".product-badges").insertAdjacentHTML("afterend", tablehtml3);

    function scrollToTop() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }
})();
