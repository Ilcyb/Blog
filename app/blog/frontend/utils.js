function getQueryStrings() {
    var url = location.search; //获取url中"?"符后的字串
     var theRequest = new Object();
     if (url.indexOf("?") != -1) {
        var str = url.substr(1);
        strs = str.split("&");
        for(var i = 0; i < strs.length; i ++) {
           theRequest[strs[i].split("=")[0]]=unescape(strs[i].split("=")[1]);
        }
     }
     return theRequest;
}

function goNotFoundPage() {
    window.location.href = '/404.html';
}