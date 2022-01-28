// ==UserScript==
// @name         R34体验增强
// @match        https://rule34.xxx/*
// @require      https://code.jquery.com/jquery-3.2.1.slim.min.js
// @grant        GM_xmlhttpRequest
// ==/UserScript==

(async function() {
    'use strict';

    GM_xmlhttpRequest({
        method: "GET",
        url: "http://192.168.0.114:8864/3d",
        onload: function (result) {
            let _text = result.responseText;
            let dict = JSON.parse(result.responseText);

            if(window.location.href.indexOf("id=")!=-1&&window.location.href.indexOf("pid=")==-1&&window.location.href.indexOf("page=favorites")==-1)
            {
                let id = $("title").text().split("|")[1];
                id = id.replace(/\s*/g,"");

                $("h4.image-sublinks").append(" | ");

                let link = "<a href=\"#\" onclick=\"post_vote('"+id+"', 'up'); addFav('"+id+"'); return false;\">Add to favorites</a>"
                $("h4.image-sublinks").append(link);
            }
            if(window.location.href.indexOf("tags=")!=-1)
            {
                $("span.thumb").each(function () {
                    let id = $(this).children("a").attr("id").split("p")[1];

                    if(dict["data"].indexOf(id)==-1){
                        let link = "<a href=\"#\" onclick=\"post_vote('"+id+"', 'up'); addFav('"+id+"'); return false;\">Favorites</a>"
                        $(this).children("a").append(link);
                    }
                    else
                    {
                        $(this).hide()
                    }

                });
            }

        },
        onerror: function (e) {
            console.log(e);
        }
    });
})();