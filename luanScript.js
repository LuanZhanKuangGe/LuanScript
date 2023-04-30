// ==UserScript==
// @name         luanScript
// @namespace    http://tampermonkey.net/
// @author       coderLuan
// @match        https://rule34.xxx/index.php?*
// @match        *://exhentai.org/*
// @include			*://exhentai.org/g/*
// @include			*://g.e-hentai.org/g/*
// @require      https://code.jquery.com/jquery-3.2.1.slim.min.js
// @grant        GM_xmlhttpRequest
// ==/UserScript==

(async function() {
    GM_xmlhttpRequest({
        method: "GET",
        url: "http://192.168.5.1:2233/",
        onload: function (result) {
            let _text = result.responseText;
            let dict = JSON.parse(result.responseText);

            //rule34
            if(window.location.host.indexOf("rule34")>-1){
                $("span.thumb").each(function () {
                    let id = $(this).children("a").attr("id").split("p")[1];
                    console.log("rule34 video found : " + id)
                    if(dict["rule34_data"].indexOf(id)>-1)
                    {
                        $(this).hide()
                    }
                });
            }

            //exhentai
            if(window.location.host.indexOf("exhentai")>-1){
                //种子转磁链
                $("div#torrentinfo").children("div").children("form").each(function () {
                    let _url = $(this).children("div").children("table").children("tbody").children("tr:eq(2)").children("td").children("a").attr("href");
                    console.log(_url);
                    _url = _url.substring(_url.lastIndexOf('torrent')-1,_url.lastIndexOf('torrent')-40-1);
                    _url = "magnet:?xt=urn:btih:"+ _url
                    console.log(_url);
                    $(this).children("div").children("table").children("tbody").children("tr:eq(2)").children("td").children("a").attr("href",_url);
                    $(this).children("div").children("table").children("tbody").children("tr:eq(2)").children("td").children("a").removeAttr("onclick")
                });

                //快速搜索种子
                var txt="<a href=\"https://btsow.boats/search/"+ $("h1#gj").text() +"\">"+ $("h1#gj").text() +"</a>";
                $("h1#gj").text("")
                $("h1#gj").append(txt);

                //快速显示作者单行本
                $("div#taglist").children("table").children("tbody").children("tr").each(function(){
                    if ($(this).children("td:eq(0)").text() == "artist:")
                    {
                        let artist = $(this).children("td:eq(1)").children("div").children("a").text()
                        let url = '/?f_search=tankoubon%24+artist%3A"' + artist.replace(" ","+") + '%24'
                        let node = '<div class="gt" style="opacity:1.0"><a href='+ url +'> tankoubon</a></div>'
                        $(this).children("td:eq(1)").children("div:first").after(node)
                    }
                });

                //显示已有的漫画信息
                $("div.gl1t").each(function () {
                    let div = $(this).children("a").children("div")

                    let artist = div.text().split(" ")[0]
                    let manga = div.text().split(" ")[1]

                    let haveArist = 0;
                    let haveManga = 0;
                    let haveDLver = 0;
                    let haveChinese = 0;

                    if(dict['manga'][artist])
                    {
                        haveArist=1
                        for(var i = 0; i < dict['manga'][artist].length; i++) {

                            let name = dict['manga'][artist][i].split(" ")[0]
                            name = name.replace(/\【.*?\】/g, '' )
                            if( name == manga)
                            {
                                haveManga = 1
                                if(dict['manga'][artist][i].indexOf("[DL版]") != -1)
                                {
                                    haveDLver = 1
                                }
                                if(dict['manga'][artist][i].indexOf("[中国翻訳]") != -1)
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
            }
        },
        onerror: function (e) {
            alert(e);
        }
    });

})();