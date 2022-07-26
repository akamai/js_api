
(function(win, doc, style, timeout) {
    var STYLE_ID = 'at-body-style';
  
    function getParent() {
      return doc.getElementsByTagName('head')[0];
    }
  
    function addStyle(parent, id, def) {
      if (!parent) {
        return;
      }
  
      var style = doc.createElement('style');
      style.id = id;
      style.innerHTML = def;
      parent.appendChild(style);
    }
  
    function removeStyle(parent, id) {
      if (!parent) {
        return;
      }
  
      var style = doc.getElementById(id);
  
      if (!style) {
        return;
      }
  
      parent.removeChild(style);
    }

    function initFunc() {
        addStyle(getParent(), STYLE_ID, style);
        setTimeout(function() {
            removeStyle(getParent(), STYLE_ID);
        }, timeout);
    }
    window.addEventListener("oneTrustCookieAccepted", function(evt) {
        if(evt.detail.targeting){
            initFunc()
        }
    }, false);

  function getCookie(name) {
      var nameEQ = name + "=";
      var ca = document.cookie.split(';');
      for(var i=0;i < ca.length;i++) {
          var c = ca[i];
          while (c.charAt(0)==' ') c = c.substring(1,c.length);
          if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
      }
      return null;
  }
    
  var cookieCheck = getCookie("OptanonConsent");;
  if(cookieCheck){
      if(cookieCheck.indexOf("C0004%3A1") > 0 ){
          initFunc()
      }
  }
    
  }(window, document, ".akam-target__container {opacity: 0 !important}", 3000));
