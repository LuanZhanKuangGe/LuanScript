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
    var txt="<a href=\"https://btsow.rest/search/"+ $("h1#gj").text() +"\">"+ $("h1#gj").text() +"</a>";
    $("h1#gj").text("")
    $("h1#gj").append(txt);

    GM_xmlhttpRequest({
        method: "GET",
        url: "http://192.168.0.114:8864/manga",
        onload: function (result) {
            let dict = JSON.parse(result.responseText);
            $("div.gl1t").each(function () {
                let div = $(this).children("a").children("div")


                let artist = div.text().split(" ")[0]
                let manga = div.text().split(" ")[1]

                let haveArist = 0;
                let haveManga = 0;
                let haveDLver = 0;
                let haveChinese = 0;

                if(dict[artist])
                {
                    haveArist=1
                    for(var i = 0; i < dict[artist].length; i++) {

                        let name = dict[artist][i].split(" ")[0]
                        if( name == manga)
                        {
                            haveManga = 1
                            if(dict[artist][i].indexOf("[DL版]") != -1)
                            {
                                haveDLver = 1
                            }
                            if(dict[artist][i].indexOf("[中国翻訳]") != -1)
                            {
                                haveChinese =1
                            }
                        }
                    }

                    if(haveArist||haveManga||haveDLver||haveChinese)
                    {
                        let tag = '<div class="gl6t">'
                        if(haveArist)
                            tag +=' <div class="gt" style="color:#f1f1f1;border-color:#1357df;background:radial-gradient(#1357df,#3377FF) !important" title="female:double penetration">♡作者</div>'
                        if(haveManga)
                            tag += '<div class="gt" style="color:#f1f1f1;border-color:#1357df;background:radial-gradient(#1357df,#3377FF) !important" title="female:double penetration">♡内容</div>'
                        if(haveDLver)
                            tag += '<div class="gt" style="color:#f1f1f1;border-color:#1357df;background:radial-gradient(#1357df,#3377FF) !important" title="female:double penetration">♡DL版</div>'
                        if(haveChinese)
                            tag += '<div class="gt" style="color:#f1f1f1;border-color:#1357df;background:radial-gradient(#1357df,#3377FF) !important" title="female:double penetration">♡翻訳</div>'
                        tag += '</div>'
                        $(this).children("div.gl3t").after(tag)
                    }
                    if(haveManga)
                    {
                        div.attr("style", "color:#0FF")
                        if((!haveDLver)&&div.text().indexOf("[DL版]") != -1)
                            div.attr("style", "color:#FF0")
                        if((!haveDLver)&&div.text().indexOf("[中国翻訳]") != -1)
                            div.attr("style", "color:#FF0")
                    }
                }
            });

        },
        onerror: function (e) {
            console.log("服务未运行")
            console.log(e);
        }
    });
})();