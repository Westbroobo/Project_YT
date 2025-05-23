// ==UserScript==
// @name         店铺车型整理(通用)
// @namespace    http://tampermonkey.net/
// @version      2025-04-08
// @description  店铺车型整理
// @author       Westbroobo
// @match        *://itm.ebaydesc.com/itmdesc/*
// @icon         https://i.ebayimg.com/images/g/WAUAAOSwtJtiJsBZ/s-l140.jpg
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

    function findAllIndices(arr, target) {
        return arr.reduce((acc, item, index) => {
            if (item === target) {
                acc.push(index);
            }
            return acc;
        }, []);
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
        var result = [];
        for (var i = 0; i < data.Make_Model.length; i++) {
            let MakeModel = data.Make_Model[i];
            let year = parseInt(data.Year[i]);
            let existingEntry = result.find(function (entry) {
                return entry.MakeModel === MakeModel;
            });

            if (!existingEntry) {
                result.push({
                    MakeModel: MakeModel,
                    years: [year],
                });
            } else {
                existingEntry.years.push(year);
            }
        }
        result.sort((a, b) => a.MakeModel.localeCompare(b.MakeModel));
        var finalResult = [];
        result.forEach((entry) => {
            entry.years = [...new Set(entry.years)];
            entry.years.sort((a, b) => a - b);
            const yearRanges = getYearRanges(entry.years);
            for (let i = 0; i < yearRanges.length; i++) {
                finalResult.push(entry.MakeModel + " " + yearRanges[i]);
            }
        });
        return finalResult;
    }

    function copyToClipboard(text) {
        navigator.clipboard.writeText(text);
    }

    let data = {Make_Model: [], Year: []};
    let xpaths = [
        '//div[@class=\'rightdes\']/div[2]/font[5]/table[1]/tbody/tr',
        '//div[@class=\'rightdes\']/div[2]/table[1]/tbody/tr',
        '//div[@class=\'rightdes\']/div[3]/table[1]/tbody/tr',
        '//div[@class=\'rightdes\']/table[1]/tbody/tr',
        '//div[@class=\'rightdes\']/h1/table[1]/tbody/tr',
        '//table[@class=\'ke-zeroborder\'][1]/tbody/tr',
        '//div[@class=\'x-item-description-child\']/h5/table/tbody/tr'
    ];

    let Vehicle_Informations = [];
    for (let i = 0; i < xpaths.length; i++) {
        let elements = selectElementsByXPath(xpaths[i]);
        if (elements.length > 0) {
            Vehicle_Informations = elements;
            break;
        }
    }

    let menu = Vehicle_Informations[0].innerText.split('\t');
    let count = menu.length;
    let row = 1
    while (count < 5) {
        menu = Vehicle_Informations[row].innerText.split('\t');
        count = menu.length;
        row += 1;
    }
    let make_Indices = findAllIndices(menu, 'Make');
    let model_Indices = findAllIndices(menu, 'Model');
    let year_Indices = findAllIndices(menu, 'Year');
    if (make_Indices.length === 0) {
        make_Indices = findAllIndices(menu, 'Manufacturer')
    }
    if (year_Indices.length === 0) {
        year_Indices = findAllIndices(menu, 'Years')
    }

    let make = '', model = '', years = '';
    for (let i = row; i < Vehicle_Informations.length; i++) {
        if (Vehicle_Informations[i].innerText.includes('\n')) {
        } else {
            let array_vehicles = Vehicle_Informations[i].innerText.split('\t')
            if (array_vehicles.length > 2) {
                for (let j = 0; j < make_Indices.length; j++) {
                    if (array_vehicles.length === count) {
                        make = array_vehicles[make_Indices[j]];
                        model = array_vehicles[model_Indices[j]];
                        years = array_vehicles[year_Indices[j]];
                    } else {
                        model = array_vehicles[model_Indices[j]-1];
                        years = array_vehicles[year_Indices[j]-1];
                    }
                    if (years.includes('-')) {
                        let array_years = years.split('-');
                        let min_year = parseInt(array_years[0]);
                        let max_year = parseInt(array_years[1]);
                        for (let k = min_year; k <= max_year; k++) {
                            data.Make_Model.push(make + ' ' + model);
                            data.Year.push(parseInt(k));
                        }
                    } else {
                        data.Make_Model.push(make + ' ' + model);
                        data.Year.push(parseInt(years));
                    }
                }
            }
        }
    }
    if (data.Year.length === 0){
        let make_Indices = findAllIndices(menu, 'Bezeichnung');
        let model_Indices = findAllIndices(menu, 'Modell');
        let year_Indices = findAllIndices(menu, 'Baujahr');

        for (let i = row; i < Vehicle_Informations.length; i++) {
            if (Vehicle_Informations[i].innerText.includes('\n')) {
            } else {
                let array_vehicles = Vehicle_Informations[i].innerText.split('\t')
                if (array_vehicles.length > 2) {
                    for (let j = 0; j < make_Indices.length; j++) {
                        if (array_vehicles.length === count) {
                            make = array_vehicles[make_Indices[j]];
                            model = array_vehicles[model_Indices[j]];
                            years = array_vehicles[year_Indices[j]];
                        } else {
                            model = array_vehicles[model_Indices[j]-1];
                            years = array_vehicles[year_Indices[j]-1];
                        }
                        if (years.includes('-')) {
                            let array_years = years.split('-');
                            let min_year = parseInt(array_years[0].substr(0, 4));
                            let max_year = parseInt(array_years[1].substr(0, 4));
                            for (let k = min_year; k <= max_year; k++) {
                                data.Make_Model.push(make + ' ' + model);
                                data.Year.push(parseInt(k));
                            }
                        } else {
                            if (model != '') {
                                data.Make_Model.push(make + ' ' + model);
                                data.Year.push(parseInt(years.substr(0, 4)));
                            }
                        }
                    }
                }
            }
        }

    };

    var finalResult = processCarData(data);
    let Vehicle = finalResult.join('\n').replace(/  /g, ' ');

    var tablehtml = `<table style="border: 1px solid #ddd; background-color: #f5f5f5; margin: 0 auto; text-align: center; width: 100%; ">
                          <thead style="background-color: #056A8E; font-size: 15px;">
                              <tr>
                                  <th style="text-align: center; border: 1px solid #dddddd; padding: 8px; color: white; ">Vehicle</th>
                              </tr>
                          </thead>
                          <tbody>
                              <tr>
                                  <td data-result="${Vehicle}" style="padding: 8px; white-space: pre-line; font-size: 14px; border: 1px solid #dddddd; cursor: pointer; user-select: all;">${Vehicle}</td>
                              </tr>
                          </tbody>
                      </table><br></br>`;

    let selectors = [".banner", ".ke-zeroborder", ".x-item-description-child"];
    let inserted = false;
    for (let i = 0; i < selectors.length; i++) {
        let element = document.querySelector(selectors[i]);
        if (element) {
            try {
                element.insertAdjacentHTML("beforebegin", tablehtml);
                inserted = true;
                break;
            } catch (error) {
            }
        }
    }

    const tableCell = document.querySelector('table tbody td');
    if (tableCell) {
        tableCell.addEventListener('click', function() {
            const text = this.dataset.result;
            copyToClipboard(text);

            const range = document.createRange();
            range.selectNodeContents(this);
            const selection = window.getSelection();
            selection.removeAllRanges();
            selection.addRange(range);

            setTimeout(() => {
                selection.removeAllRanges();
            }, 10);
        });
    }
})();
