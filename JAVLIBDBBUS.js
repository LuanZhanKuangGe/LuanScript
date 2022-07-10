// ==UserScript==
// @name         突出显示本地已经存在的视频
// @match        https://javdb.com/*
// @match        https://www.javlibrary.com/*
// @match        https://www.javbus.com/*
// @require      https://code.jquery.com/jquery-3.2.1.slim.min.js
// @grant        GM_xmlhttpRequest
// @grant        GM_registerMenuCommand
// @grant        GM_getValue
// @grant        GM_setValue
// ==/UserScript==

(function() {

    GM_registerMenuCommand("Jav大图", () => {
        var javbp = GM_getValue("javbp")
        if(javbp=="true")GM_setValue("javbp", "false")
        if(javbp=="false")GM_setValue("javbp", "true")
        location.reload()
    });

    GM_xmlhttpRequest({
        method: "GET",
        url: "http://127.0.0.1:8864/av",
        onload: function (result) {
            let _text = result.responseText;
            let dict = JSON.parse(result.responseText);

            let noshowtag = ["【VR】","五十路","脱糞"];

            if(window.location.host.indexOf("javlibrary")>-1)
            {
                var id = $("div#video_id").children("table").children("tbody").children("tr").children("td.text").text().trim()
                var db_url = 'https://javdb.com/search?q=' + id
                var db_node = '<div id="video_genres" class="item"><table><tbody><tr><td class="header">外链:</td><td class="text"><span class="genre"><a href="' + db_url +' " rel="category tag">JavDB</a></span></td><td class="icon"></td></tr></tbody></table></div>'
                $("div#video_info").append(db_node);

                $("div.video").each(async function () {
                    let _name = $(this).children("a").children("div.id").text()
                    let _title = $(this).children("a").children("div.title").text()

                    for(var actor in dict) {
                        if(dict[actor].indexOf(_name)>-1)
                        {
                            $(this).children("a").children("div.id").hide()
                            $(this).children("a").children("div.title").hide()
                            //$(this).remove()
                        }
                    }
                    for(var i = 0; i < noshowtag.length; i++)
                        if(_title.indexOf(noshowtag[i])>-1)
                            $(this).remove()

                    //Jav大预览图
                    var javbp = await GM_getValue("javbp")
                    if(javbp=="true"){
                        let _pic = $(this).children("a").children("img").attr("src")
                        $(this).children("a").children("img").attr("src", _pic.replace("ps.jpg","pl.jpg"))
                        $(this).children("a").children("img").attr("width", "90%")
                        $(this).children("a").children("img").attr("height", "90%")
                        $(this).attr("style", "width:600px;height: 405px;")
                        $(this).children("a").children("div.id").text($(this).children("a").children("div.id").text() + " " + _title.slice(0,30))
                        $(this).children("a").children("div.title").remove()
                    }

                })
            }

            if(window.location.host.indexOf("javbus")>-1)
            {
                $("a.movie-box").each(function () {
                    let _name = $(this).children("div.photo-info").children("span").children("date:first").text()
                    let _title = $(this).children("div.photo-info").children("span").text()

                    for(var actor in dict) {
                        if(dict[actor].indexOf(_name)>-1)
                        {
                            $(this).children("div.photo-info").hide()
                            //$(this).remove()
                        }
                    }

                    for(var i = 0; i < noshowtag.length; i++)
                        if(_title.indexOf(noshowtag[i])>-1)
                            $(this).remove()
                });
            }

            if(window.location.host.indexOf("javdb")>-1)
            {
                $("div.item").each(function () {
                    let _name = $(this).children("a").children("div.video-title").children("strong").text()
                    let _title = $(this).children("a").children("div.video-title").text()

                    for(var actor in dict) {
                        if(dict[actor].indexOf(_name)>-1)
                        {
                            $(this).children("a").children("div.uid").hide()
                            $(this).children("a").children("div.video-title").hide()
                            $(this).children("a").children("div.meta").hide()
                            $(this).children("a").children("div.tags").hide()
                            //$(this).remove()
                        }
                    }

                    for(var i = 0; i < noshowtag.length; i++)
                        if(_title.indexOf(noshowtag[i])>-1)
                            $(this).remove()
                });

                //显示片商的信息
                if(window.location.href.indexOf("makers")>-1||window.location.href.indexOf("series")>-1)
                {
                    $("a.box").each(function () {
                        var url = $(this).attr("href") + "?f=download"
                        $(this).attr("href", url)
                    });
                }

                //显示演员的信息
                if(window.location.href.indexOf("actors")>-1||window.location.href.indexOf("actor_monthly")>-1)
                {
                    $("div.actor-box").each(function () {
                        var url = $(this).children("a").attr("href") + "?t=d"
                        $(this).children("a").attr("href", url)
                        var names = $(this).children("a").attr("title").split(", ")
                        for(var name in names) {
                            if(dict[names[name]])
                            {
                                var tag = '<strong>已收藏' + dict[names[name]].length +  '部</strong>'

                                $(this).children("a").children("strong").after(tag)
                            }
                        }
                    });

                    {
                        var names1 = $("div.section-title").children("h2").children("span.actor-section-name").text().split(", ")
                        var names2 = $("div.section-title").children("h2").children("span.section-meta:first").text().split(", ")
                        var names = names1.concat(names2)
                        for(var name in names) {
                            if(dict[names[name]])
                            {
                                var tag = $("div.section-title").children("h2").children("span.section-meta:last").text() + " 已收藏"  + dict[names[name]].length +  "部"
                                $("div.section-title").children("h2").children("span.section-meta:last").text(tag)
                            }
                        }

                    }
                }
            }

        },
        onerror: function (e) {
            alert(e);
        }
    });

})();