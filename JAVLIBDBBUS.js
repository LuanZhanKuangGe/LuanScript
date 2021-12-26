// ==UserScript==
// @name         突出显示本地已经存在的视频
// @match        https://javdb.com/*
// @icon         https://www.google.com/s2/favicons?domain=javdb.com
// @require      https://code.jquery.com/jquery-3.2.1.slim.min.js
// @grant        GM_xmlhttpRequest
// ==/UserScript==

(function() {

    GM_xmlhttpRequest({
        method: "GET",
        url: "http://192.168.0.114:8864/av",
        onload: function (result) {
            let _text = result.responseText;
            let dict = JSON.parse(result.responseText);

            $("div.grid-item").each(function () {
                let _name = $(this).children("a").children("div.uid").text()
                let _title = $(this).children("a").children("div.video-title").text()

                if(dict["av"].indexOf(_name)>-1)
                {
                    $(this).children("a").children("div.uid").hide()
                    $(this).children("a").children("div.video-title").hide()
                    $(this).children("a").children("div.meta").hide()
                    $(this).children("a").children("div.tags").hide()
                }
            });
        },
        onerror: function (e) {
            console.log(e);
        }
    });

})();