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


function closePopupAndUpdateOpener(url)
{
    if (window.opener) {
        window.opener.location.href=url;
        window.close();
    }
}