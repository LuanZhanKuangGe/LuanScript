// ==UserScript==
// @name         luanScript
// @namespace    http://tampermonkey.net/
// @author       coderLuan
// @match        https://javdb.com/*
// @match        https://www.javlibrary.com/*
// @match        https://www.javbus.com/*
// @match        https://www.141jav.com/*
// @match        https://btsow.cfd/search/*
// @match        https://rule34.xxx/index.php?*
// @match        *://exhentai.org/*
// @include			*://exhentai.org/g/*
// @include			*://g.e-hentai.org/g/*
// @match        https://www.iwara.tv/*
// @require      https://code.jquery.com/jquery-3.2.1.slim.min.js
// @grant        GM_xmlhttpRequest
// @grant        GM_registerMenuCommand
// @grant        GM_getValue
// @grant        GM_setValue
// ==/UserScript==


(async function() {
    GM_xmlhttpRequest({
        method: "GET",
        url: "http://192.168.5.1:2233/",
        onload: function (result) {
            let _text = result.responseText;
            let dict = JSON.parse(result.responseText);

            //btsow链接直转
            if(window.location.host.indexOf("btsow")>-1)
            {
                $("div.data-list").children("div.row").children("a").each(function () {
                    let _new = "magnet:?xt=urn:btih:" + $(this).attr("href").split("/")[6]
                    $(this).attr("href",_new);
                    console.log($(this).attr("href"));
                });
            }

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

            //iwara
            //             function addButton() {
            //                 if ($('div.videoPlayer').length > 0) {
            //                     // 元素加载完毕
            //                     console.log('Video loaded!');
            //                     let username = $('div.page-video__byline__info').children('a.username').children("div").text()
            //                     console.log(username)
            //                     let url = $('button.downloadButton').parent("div").next("div").children("ul").children("li:eq(0)").children("a").attr("href");
            //                     url = url.replace('download=', 'filename='+ '[' + username + ']');

            //                     //url = 'AA' + url + 'ZZ'
            //                     //let new_url = 'Thunder://' + btoa(url);
            //                     $('button.shareButton').addClass('mr-2')
            //                     let new_button = '<div class="dropdown dropdown--bottomLeft"><div class="dropdown"><button class="button downloadButton button button--solid" type="button"><a href="' + url + '" class="">下载</a></button></div></div>'
            //                     $('button.shareButton ').after(new_button)
            //                     clearInterval(intervalId);
            //                 }
            //             }
            function deleteVideo() {
                if ($('div.videoTeaser').length > 0) {
                    //console.log('Video loaded!');
                    $("div.videoTeaser").each(function () {
                        let id2 = $(this).children("a").attr("href").split('/')[2].toLowerCase();
                        //console.log(id2);
                        if(dict["mmd_data"].indexOf(id2)>-1)
                        {
                            $(this).hide()
                            //console.log(id2 + " is hide");
                        }
                        let artist = $(this).children("div").children("div").children("a").attr("href").split('/')[2].toLowerCase();
                        if(dict["mmd_artist"].indexOf(artist)>-1)
                        {
                            $(this).hide()
                        }
//                         let like = $(this).children("a").children("div.likes").children("div").text();
//                         if(like.charAt(like.length-1)!= 'K')
//                         {
//                             if(parseInt(like)<500)
//                             {
//                                 $(this).hide()
//                             }
//                         }
                    });
                }
            }
            if(window.location.host.indexOf("iwara")>-1){
                console.log("iwara");
                if(window.location.href.indexOf("iwara.tv/video")>-1){
                    var intervalId = setInterval(deleteVideo, 1000);
                }
                if(window.location.href.indexOf("iwara.tv/profile")>-1){
                    setInterval(deleteVideo, 1000);
                }
                if(window.location.href.indexOf("iwara.tv/subscriptions")>-1){
                    console.log('loop to hide video');
                    setInterval(deleteVideo, 1000);
                }
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

            let noshowtag = ["【VR】","五十路","六十路","七十路","脱糞"];
            let showtag = ["凌辱", "輪姦", "強姦", "多P"];

            if(window.location.host.indexOf("javlibrary")>-1)
            {
                console.log("javlibrary");
                var id = $("div#video_id").children("table").children("tbody").children("tr").children("td.text").text().trim()
                var db_url1 = 'https://javdb.com/search?q=' + id
                var db_url2 = 'https://www.javbus.com/' + id
                var db_url3 = 'https://btsow.cfd/search/'+ id
                var db_url4 = 'https://www.141jav.com/search/'+ id.replace("-","")
                var db_node = '<div id="video_genres" class="item"><table><tbody><tr><td class="header">外链:</td><td class="text">' +
                    '<span class="genre"><a href="' + db_url2 +' " target = "_blank" rel="category tag">JavBus</a></span>' +
                    '<span class="genre"><a href="' + db_url1 +' " " target = "_blank" rel="category tag">JavDB</a></span>' +
                    '<span class="genre"><a href="' + db_url3 +' " " target = "_blank" rel="category tag">BTSOW</a></span>' +
                    '<span class="genre"><a href="' + db_url4 +' " " target = "_blank" rel="category tag">141JAV</a></span>' +
                    '</td><td class="icon"></td></tr></tbody></table></div>'

                $("div#video_info").append(db_node);

                $("div.video").each(async function () {
                    let _name = $(this).children("a").children("div.id").text()
                    let _title = $(this).children("a").children("div.title").text()

                    for(var actor in dict['jav_id']) {
                        if(dict['jav_id'][actor].indexOf(_name)>-1)
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
                console.log("javbus");
                $("a.movie-box").each(function () {
                    let _id = $(this).children("div.photo-info").children("span").children("date:first").text().trim()
                    let _title = $(this).children("div.photo-info").children("span").text().trim()
                    for(var id in dict['jav_id']) {
                        if(dict['jav_id'][id].indexOf(_id)>-1)
                        {
                            console.log(_id);
                            $(this).children("div.photo-info").hide()
                            //$(this).remove()
                        }
                    }

                    for(var i = 0; i < noshowtag.length; i++)
                        if(_title.indexOf(noshowtag[i])>-1)
                            $(this).remove()
                });

                if(window.location.href.indexOf("actresses")>-1)
                {
                    console.log("javbus actresses");
                    $("a.avatar-box").each(function () {
                        let _name =  $(this).children("div.photo-info").children("span").text()
                        let _url = 'https://javdb.com/search?q=' + _name + '&f=actor'
                        //console.log(_url);
                        $(this).attr("href", _url)
                        _name = _name.replace(/\（.*?\）/g, '' )
                        if(dict['jav_actor'][_name])
                        {
                            var text = '<span>已收藏' + dict['jav_actor'][_name].length +  '部</span>'
                            $(this).children("div.photo-info").append(text);
                            $(this).hide();
                        }
                    });
                }
            }

            if(window.location.host.indexOf("141jav")>-1)
            {
                $("h5.title").each(function () {
                    let _id = $(this).children("a").text().trim()
                    let _url = 'https://www.javlibrary.com/cn/vl_searchbyid.php?keyword=' + _id
                    $(this).children("a").attr("href",_url)
                    $(this).children("a").attr("target","_blank")
                })
            }

            if(window.location.host.indexOf("javdb")>-1)
            {
                console.log("javdb");
                $("div.item").each(function () {
                    let _id = $(this).children("a").children("div.video-title").children("strong").text()
                    let _title = $(this).children("a").children("div.video-title").text()

                    for(var id in dict['jav_id']) {
                        if(dict['jav_id'][id].indexOf(_id)>-1)
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
                    console.log("javdb makers series");
                    $("a.box").each(function () {
                        var url = $(this).attr("href") + "?f=download"
                        $(this).attr("href", url)
                    });
                }

                //显示演员的信息
                if(window.location.href.indexOf("actor")>-1||window.location.href.indexOf("actor_monthly")>-1)
                {
                    console.log("javdb actors actor_monthly");
                    $("div.actor-box").each(function () {
                        var url = $(this).children("a").attr("href") + "?t=s,d"
                        console.log(url);
                        $(this).children("a").attr("href", url)
                        var names = $(this).children("a").attr("title").split(", ")

                        for(var name in names) {
                            if(dict['jav_actor'][names[name]])
                            {
                                console.log(names[name]);
                                var tag = '<strong>已收藏' + dict['jav_actor'][names[name]].length +  '部</strong>'
                                $(this).children("a").children("strong").after(tag)

                            }
                        }
                    });

                    {
                        var names1 = $("div.section-title").children("h2").children("span.actor-section-name").text().split(", ")
                        var names2 = $("div.section-title").children("h2").children("span.section-meta:first").text().split(", ")
                        var names = names1.concat(names2)
                        for(var name in names) {
                            if(dict['jav_actor'][names[name]])
                            {
                                console.log(names[name]);
                                var tag = $("div.section-title").children("h2").children("span.section-meta:last").text() + " 已收藏"  + dict['jav_actor'][names[name]].length +  "部"
                                $("div.section-title").children("h2").children("span.section-meta:last").text(tag)
                            }
                        }

                    }

                    $("div.actor-tags").children("div.content").removeClass("collapse")
                    $("div.actor-tags").children("div.content").children("a.is-outlined").each(function () {
                        for(var i = 0; i < showtag.length; i++)
                            if($(this).text().indexOf(showtag[i])>-1)
                                $(this).addClass("is-info");
                    });
                }

            }
        },
        onerror: function (e) {
            alert(e);
        }
    });

})();