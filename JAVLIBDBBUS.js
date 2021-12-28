// ==UserScript==
// @name         突出显示本地已经存在的视频
// @match        https://javdb.com/*
// @match        http://www.javlibrary.com/*
// @match        https://www.javbus.com/*
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

            if(window.location.host.indexOf("javlibrary")>-1)
            {
                $("div.video").each(function () {
                    let _name = $(this).children("a").children("div.id").text()
                    let _title = $(this).children("a").children("div.title").text()

                    if(dict["av"].indexOf(_name)>-1)
                    {
                        $(this).children("a").children("div.id").hide()
                        $(this).children("a").children("div.title").hide()
                        //$(this).remove()
                    }
                    if(_title.indexOf("【VR】")>-1)
                    {
                        $(this).remove()
                    }
                });
            }

            if(window.location.host.indexOf("javbus")>-1)
            {
                $("a.movie-box").each(function () {
                    let _name = $(this).children("div.photo-info").children("span").children("date:first").text()
                    let _title = $(this).children("div.photo-info").children("span").text()

                    console.log(_title);

                    if(dict["av"].indexOf(_name)>-1)
                    {
                        $(this).children("div.photo-info").hide()
                        //$(this).remove()
                    }
                    if(_title.indexOf("【VR】")>-1)
                    {
                        $(this).remove()
                    }
                });
            }

            if(window.location.host.indexOf("javdb")>-1)
            {
                $("div.grid-item").each(function () {
                    let _name = $(this).children("a").children("div.uid").text()
                    let _title = $(this).children("a").children("div.video-title").text()

                    if(dict["av"].indexOf(_name)>-1)
                    {
                        $(this).children("a").children("div.uid").hide()
                        $(this).children("a").children("div.video-title").hide()
                        $(this).children("a").children("div.meta").hide()
                        $(this).children("a").children("div.tags").hide()
                        //$(this).remove()
                    }
                    if(_title.indexOf("【VR】")>-1)
                    {
                        $(this).remove()
                    }
                });
            }

        },
        onerror: function (e) {
            console.log(e);
        }
    });

})();