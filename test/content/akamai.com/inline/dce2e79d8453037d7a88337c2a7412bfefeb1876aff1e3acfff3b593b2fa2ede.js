
function OptanonWrapper() {
  OneTrust.InsertScript('/etc.clientlibs/akamai/clientlibs/clientlib-oneconsent.js', 'head', null, null, '2');
  const acceptBtn = document.getElementById("onetrust-accept-btn-handler"); const cookieSettingsBtn = document.getElementById("onetrust-pc-btn-handler"); const declineBtn = document.getElementById("onetrust-reject-all-handler"); const btnContainer = document.getElementById("onetrust-button-group"); btnContainer.insertBefore(acceptBtn, cookieSettingsBtn); console.log(btnContainer, acceptBtn)
}
