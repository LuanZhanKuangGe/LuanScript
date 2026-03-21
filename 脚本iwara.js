// ==UserScript==
// @name         iwaraScript
// @namespace    http://tampermonkey.net/
// @author       coderLuan
// @match        https://www.iwara.tv/*
// @require      https://code.jquery.com/jquery-3.2.1.slim.min.js
// @grant        GM_xmlhttpRequest
// @grant        GM_registerMenuCommand
// @grant        GM_getValue
// @grant        GM_setValue
// ==/UserScript==


(async function() {

    let shwow_artist = GM_getValue('artist');
    console.log(shwow_artist);

    if(shwow_artist){
        GM_registerMenuCommand("隐藏已关注作者", () => {
            GM_setValue('artist', !shwow_artist);
            location.reload();
        });
    }
    else{
        GM_registerMenuCommand("显示已关注作者", () => {
            GM_setValue('artist', !shwow_artist);
            location.reload();
        });
    }
    
    let shwow_unhot = GM_getValue('hot');
    console.log(shwow_unhot);

    if(shwow_unhot){
        GM_registerMenuCommand("隐藏冷门视频", () => {
            GM_setValue('hot', !shwow_unhot);
            location.reload();
        });
    }
    else{
        GM_registerMenuCommand("显示冷门视频", () => {
            GM_setValue('hot', !shwow_unhot);
            location.reload();
        });
    }


    GM_xmlhttpRequest({
        method: "GET",
        url: "http://192.168.5.1:2233/iwara",
        onload: function (result) {
            let _text = result.responseText;
            let dict = JSON.parse(result.responseText);
            function deleteVideo() {
                if ($('div.videoTeaser').length > 0) {
                    //console.log('Video loaded!');
                    $("div.videoTeaser").each(function () {
                        let id2 = $(this).children("a").attr("href").split('/')[2].toLowerCase();
                        if(dict["mmd_data"].indexOf(id2)>-1)
                        {
                            $(this).hide()
                        }

                        let artist = $(this).children("div").children("div").children("a").attr("href").split('/')[2].toLowerCase();
                        if(!shwow_artist&&dict["mmd_artist"].indexOf(artist)>-1)
                        {
                            $(this).hide()
                        }

                        let like = $(this).children("a").children("div.likes").children("div").text();
                        if(!shwow_unhot&&like.charAt(like.length-1)!= 'K')
                        {
                            if(parseInt(like)<500)
                            {
                                $(this).hide()
                            }
                        }
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

        },
        onerror: function (e) {
            alert(e);
        }
    });

})();