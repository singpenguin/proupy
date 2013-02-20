var xmlHttp;

function ding_cai_clickHandler(n)
{
	var thisurl = location.href;
	var url="/set_ding_cai/";
	pid = thisurl.substring(thisurl.lastIndexOf("/")+1, thisurl.length);
	var saveid = GetCookie("diggid");
	if(saveid != null){
		var saveids = saveid.split(",");
		var hasid = false;
		saveid = "";
		j = 1;
		for(i=saveids.length-1;i>=0;i--){
			if(saveids[i]==pid && hasid) continue;
			else {
				if(saveids[i]==pid && !hasid) hasid = true;
				saveid += (saveid="" ? saveids[i] : ","+saveids[i]);
				j++;
				if(j==20 && hasid) break;
				if(j==19 && !hasid) break;
			}
		}
		if(hasid) {alert("您已经顶过该帖啦！"); return;}
		else saveid += ","+pid;
		SetCookie("diggid", saveid, 1);
	}else {
		SetCookie("diggid", pid, 1);
	}
	xmlHttp = GetXmlHttpObject();
	if(xmlHttp == null){
		alert("您的浏览器不支持AJAX!");
		return;
	}
	url = url+pid+"/"+n;
	xmlHttp.onreadystatechange=stateChanged;
	xmlHttp.open("GET",url,true);
	xmlHttp.send(null);
}

function GetXmlHttpObject()
{
  var xmlHttp=null;
  try{
    xmlHttp=new XMLHttpRequest();
  }catch (e){
    try{
      xmlHttp=new ActiveXObject("Msxml2.XMLHTTP");
    }catch (e){
      xmlHttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
  }
  return xmlHttp;
}

function stateChanged() 
{
  if (xmlHttp.readyState==4){ 
		if(xmlHttp.responseText == 1){
			document.getElementById("a_ding").innerHTML=parseInt(document.getElementById("a_ding").innerHTML) + 1;
		}else if (xmlHttp.responseText == 0){
			document.getElementById("a_cai").innerHTML=parseInt(document.getElementById("a_cai").innerHTML) + 1;
		}
  }
}
function GetCookie(c_name)
{
	if (document.cookie.length > 0){
		c_start = document.cookie.indexOf(c_name + "=")
		if (c_start != -1){
			c_start = c_start + c_name.length + 1;
			c_end   = document.cookie.indexOf(";",c_start);
			if (c_end == -1){
				c_end = document.cookie.length;
			}
			return unescape(document.cookie.substring(c_start,c_end));
		}
	}
	return null
}
function SetCookie(c_name,value,expiredays)
{
	var exdate = new Date();
	exdate.setDate(exdate.getDate() + expiredays);
	document.cookie = c_name + "=" +escape(value) + ((expiredays == null) ? "" : ";expires=" + exdate.toGMTString()); 
}

function VerifyMessage() {
	var strName=document.getElementById("name").value;
	var strEmail=document.getElementById("email").value;
	var strMessage=document.getElementById("message").value;

	if(strName==""){
		return false;
	}else{
		re = new RegExp("^[.A-Za-z0-9\u4e00-\u9fa5]+$");
		if (!re.test(strName)){
			return false;
		}
	}
	if(strEmail==""){
		return false;
	}else{
		re = new RegExp("^[\\w-]+(\\.[\\w-]+)*@[\\w-]+(\\.[\\w-]+)+$");
		if (!re.test(strEmail)){
			return false;
		}
	}
	if(strMessage==""){
		return false;
	}
}