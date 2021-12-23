// ==UserScript==
// @name         高亮显示本地已有漫画
// @author       LuanZhanKuangGe
// @match        *://exhentai.org/*
// @include			*://exhentai.org/g/*
// @include			*://g.e-hentai.org/g/*
// @require      https://code.jquery.com/jquery-3.2.1.slim.min.js
// @grant        GM_xmlhttpRequest
// ==/UserScript==

(function() {

    //快速搜索种子
    var txt="<a href=\"https://btsow.one/search/"+ $("h1#gj").text() +"\">"+ $("h1#gj").text() +"</a>";
    $("h1#gj").text("")
    $("h1#gj").append(txt);

    GM_xmlhttpRequest({
        method: "GET",
        url: "http://192.168.0.114:8864/manga",
        onload: function (result) {
            let dict = JSON.parse(result.responseText);
            console.log(dict);
            $("div.gl1t").each(function () {
                let div = $(this).children("a").children("div")
                let manga = div.text()

                let artist = manga.split(" ")[0]

                if(dict[artist])
                {
                    console.log(dict[artist]);
                    div.attr("style", "color:#FF0")
                }


            });

        },
        onerror: function (e) {
            //alert("服务未运行")
            console.log(e);
        }
    });
})();