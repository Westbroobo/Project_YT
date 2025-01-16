// ==UserScript==
// @name         rockauto逆向辅助
// @namespace    http://tampermonkey.net/
// @version      2023.11.22
// @description  rockauto_oe号获取
// @author       Westbroobo
// @match        *://www.rockauto.com/en/*
// @match        *://www.rockauto.com*
// @icon         https://www.rockauto.com/favicon.ico
// @grant        none
// ==/UserScript==

(function () {
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

    let list_part = document.getElementsByClassName('listing-final-partnumber  as-link-if-js');
    function processOEs() {
        const bodies = selectElementsByXPath('//*[@class="nobmp"]/tbody').slice(2);
        const oesArray = [];
        //const srcsArray = [];
        bodies.forEach((body) => {
            const id = body.id;
            if (id != '') {
                const xpath_oe = '//*[@id="' + id + '"]/tr[1]/td[1]/span[2]';
                const xpath_src = '//*[@id="inlineimg_thumb' + id.slice(16) +'"]';
                const oes = document.evaluate(xpath_oe, body, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
                const srcs = document.evaluate(xpath_src, body, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
                if (oes.singleNodeValue) {
                    const oe = oes.singleNodeValue.innerText.trim();
                    oesArray.push(oe);
                } else {
                    oesArray.push('');
                }
                /*if (srcs.singleNodeValue) {
                    const src = srcs.singleNodeValue.currentSrc.trim();
                    srcsArray.push(src);
                }*/
            }
        });

        for (let i = 0; i < list_part.length; i++) {
            if (oesArray[i] !== undefined) {
                let OEM = oesArray[i].replace(/, /g, ';');
                let part_number = list_part[i].textContent
                let spanHTML = `<span onclick="copyToClipboard('${OEM}')" class="add" style="background-color: #E3D2D2; border: 1px solid #ddd; border-radius: 4px; padding: 8px; display: inline-block; margin-top: 10px; font-family: Arial, sans-serif; font-size: 12px; color: #333; cursor: pointer; user-select: all; max-height: 100px; max-width: 1000px;overflow: auto; white-space: pre-wrap;">${OEM}</span>`;
                let existingSpan = list_part[i].nextElementSibling;
                if (existingSpan && existingSpan.classList.contains('add')) {
                    existingSpan.remove();
                }
                list_part[i].insertAdjacentHTML('afterend', spanHTML);
                list_part[i].innerHTML = '<span onclick="copyToClipboard(\'' + part_number + '\')" style="user-select: all;">' + part_number + '</span>';
            }
        }

        /*
        let list_img = document.getElementsByClassName('listing-inline-image listing-inline-image-thumb listing-inline-image-border');
        for (let i = 0; i < list_img.length; i++) {
            if (srcsArray[i] !== undefined) {
                let srcHTML = `<a class="img" style="background-color: #f4f4f4; border: 1px solid #ddd; border-radius: 4px; padding: 8px; display: inline-block; margin-top: 10px; font-family: Arial, sans-serif; font-size: 2px; color: #333; cursor: pointer; user-select: all; max-height: 100px; max-width: 1000px;overflow: auto; white-space: pre-wrap;">${srcsArray[i]}</a>`;
                let existinga = list_img[i].nextElementSibling;
                if (existinga && existinga.classList.contains('img')) {
                    existinga.remove();
                }
                list_img[i].insertAdjacentHTML('afterend', srcHTML);
            }
        }*/

        let list_oe = document.getElementsByClassName('add');
        let part_repeat_Array = generatePartRemainArray(oesArray, list_part);
        for (let i = 0; i < part_repeat_Array.length; i++) {
            let part_remain = part_repeat_Array[i].slice(1);
            let divHTML = `<div class="add2" style="background-color: #7CCFD2; border: 1px solid #ddd; border-radius: 4px; padding: 8px; display: inline-block; margin-top: 10px; font-family: Arial, sans-serif; font-size: 12px; color: #333; max-height: 100px; max-width: 1000px; overflow: auto;">${part_remain}</div>`;
            let existingSpan = list_oe[i].nextElementSibling;
                if (existingSpan && existingSpan.classList.contains('add2')) {
                    existingSpan.remove();
                }
            list_oe[i].insertAdjacentHTML('afterend', divHTML);
        }
    }

    function generatePartRemainArray(oesArray, list_part) {
        const part_repeat_Array = [];
        const array_list_part = Array.from(list_part);

        for (let i = 0; i < oesArray.length; i++) {
            let part_repeat = '';
            if (oesArray[i] === '') {
                part_repeat_Array.push(part_repeat);
            } else {
                const list_part_remain = [...array_list_part.slice(0, i), ...array_list_part.slice(i + 1)];
                const oesArray_remain = [...oesArray.slice(0, i), ...oesArray.slice(i + 1)];
                for (let j = 0; j < oesArray_remain.length; j++) {
                    const k = oesArray[i] + ';' + oesArray_remain[j];
                    const bothArray = k.replace(/, /g, ';').split(';');
                    const uniqueBothArray = [...new Set(bothArray)];
                    const both = uniqueBothArray.join(', ');
                    if (k.length !== both.length && k.length+1 !== both.length) {
                        let p = list_part_remain[j].outerText;
                        part_repeat = part_repeat + ';' + p;
                    }
                }
                const part_repeats = part_repeat.split(';');
                const part_reapeats_Array = [...new Set(part_repeats)];
                part_repeat = part_reapeats_Array.join(';');
                part_repeat_Array.push(part_repeat);
            }
        }
        return part_repeat_Array;
    }

    function observeTitleChange() {
        const observer = new MutationObserver(() => {
            processOEs();
        });

        observer.observe(document.querySelector('title'), {
            subtree: true,
            characterData: true,
            childList: true
        });
    }

    processOEs();
    observeTitleChange();
})();

