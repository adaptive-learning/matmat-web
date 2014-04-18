if (!String.prototype.format) {
  String.prototype.format = function() {
    /* format functionality for strings */
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) {
      return typeof args[number] != 'undefined'
        ? args[number]
        : match
      ;
    });
  };
}

function openPopup(url, next) {
    /* Open popup to Google or Facebook auth */

    var w = 700;
    var h = 500;
    var left = 100;
    var top = 100;

    var settings = 'height=' + h + ',width=' + w + ',left=' + left + ',top=' + top + ',resizable=yes,scrollbars=yes,toolbar=no,menubar=no,location=yes,directories=no,status=yes';
    url += "?next=" + next;

    window.open(url, name, settings)
}


function closePopupAndUpdateOpener(url){
    /* Close popup window (Google or Facebook auth) and reload main window */

    if (window.opener) {
        window.opener.location.href=url;
        window.close();
    }
}


function getURLParameter(name) {
  return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null
}