// ==UserScript==
// @name         Kindoo Plugin
// @namespace    http://martykch.com
// @version      2.0
// @description  Send Haodoo books to Kindle by Kindoo
// @author       You
// @match        http://www.haodoo.net/*
// @require http://code.jquery.com/jquery-latest.js
// @grant   GM_getValue
// @grant   GM_setValue
// @grant   GM_addStyle
// ==/UserScript==


(function() {
    'use strict';

    var Kindoo = {

        config: {
            email: "ko19950314@gmail.com",
            host: "http://localhost:8000/haodoo/"
        },

        initHtmlComp: function(){
            $("a").each(function(i, k){
                if($(this).attr('href')){
                    var parms = $(this).attr('href').match(/\?M=(?:book|share)&P=(.*)/gi);
                    if(parms !== null && $(this).html().match(/<img.*>/gi) == null){
                        console.log(parms);
                        $(this).after('<button class="btn" data-targetid="'+ parms[0] +'">+</button>');
                    }
                }
            });

            $(".btn").click(function(){
                Kindoo.submitRequest($(this).data("targetid"));
            });
        },

        submitRequest: function(targetId){
            $.post(Kindoo.config.host, {"email": Kindoo.config.email, "targetId": targetId}).success(function(m){
                console.log(m);
            }).error(function(){
                console.log("error");
            });
            console.log("damn", targetId);
        }

    };

    Kindoo.initHtmlComp();
})();
