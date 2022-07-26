
    (function () {
      function onDocumentReady() {
        var akamaiPageData = JSON.parse("{\x22info\x22:{\x22assets\u002Dpdf\x22:[],\x22assets\u002Dvideo\x22:[],\x22language\x22:\x22en\x22,\x22pageName\x22:\x22English\x22}}");
        if(userCountryCode == null){
          akamaiPageData.info.countrycode = 'US';
        } else {
        akamaiPageData.info.countrycode = userCountryCode;
        }
        var jsonString = JSON.stringify(akamaiPageData);
        window.adobeDataLayer = window.adobeDataLayer || [];
        adobeDataLayer.push({
          page: JSON.parse("{\x22page\u002Db06720fb57\x22:{\x22@type\x22:\x22core\/wcm\/components\/page\/v2\/page\x22,\x22repo:modifyDate\x22:\x222022\u002D07\u002D12T15:54:40Z\x22,\x22dc:title\x22:\x22English\x22,\x22xdm:template\x22:\x22\/conf\/akamai\/settings\/wcm\/templates\/page\u002Dcontent\x22,\x22xdm:language\x22:\x22en\x22,\x22xdm:tags\x22:[],\x22repo:path\x22:\x22\/content\/akamai\/en.html\x22}}"),
          event: 'cmp:show',
          eventInfo: {
            path: 'page.page\u002Db06720fb57'
          },
          akamaiPage: JSON.parse(jsonString)
        });
      }
      if (document.readyState !== 'loading') {
        onDocumentReady();
      } else {
        document.addEventListener('DOMContentLoaded', onDocumentReady);
      }
    })();
  