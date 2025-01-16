// ==UserScript==
// @name         ebay默认语言
// @namespace    http://tampermonkey.net/
// @version      2024-12-05
// @description  语言默认英文
// @author       Westbroobo
// @match        https://www.ebay.com/itm/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=ebay.com
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    var current_Url = window.location.href;

    if (current_Url.includes('_ul=EN')) {
        return;
    } else {
        var new_Url = current_Url + '&_ul=EN';
        window.location.href = new_Url;
    }
})();

