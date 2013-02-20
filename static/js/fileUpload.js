function fileSelected() {
	//判断当前浏览器是否支持File API
	if(window.File && window.FileList && window.FileReader){
		var file = document.getElementById("fileToUpload").files[0];
		var filesize = 0;
		if(file.size > 1024*1024)
			filesize = (Math.round(file.size * 100 / (1024*1024)) / 100).toString() + "MB";
		else
			filesize = (Math.round(file.size * 100 / 1024) / 100).toString() + "KB";
	}else{
		
	}
	document.getElementById("fileName").innerHTML = "名字: " + file.name;
	document.getElementById("fileSize").innerHTML = "大小: " + filesize;
	//document.getElementById("fileType").innerHTML = "类型: " + file.type;
	document.getElementById("progressNumber").innerHTML = "";
}
function uploadFile(){
	var fd = new FormData();
	fd.append("FileData", document.getElementById("fileToUpload").files[0]);
	fd.append("FileName", document.getElementById("fileToUpload").files[0].name);
	fd.append("FileSize", document.getElementById("fileToUpload").files[0].size);
	var xhr = new XMLHttpRequest();
	xhr.upload.addEventListener("progress", uploadProgress, false);
	xhr.addEventListener("load", uploadComp, false);
	xhr.addEventListener("error", uploadFailed, false);
	xhr.addEventListener("abort", uploadCanceled, false);
	xhr.open("POST", "/admin/upload");
	xhr.send(fd);
	document.getElementById("btnUpload").disabled = true;
}

function uploadProgress(evt){	
	if(evt.lengthComputable){
		var per = Math.round(evt.loaded * 100 / evt.total);
		document.getElementById("progressNumber").innerHTML = "上传状态：" + per.toString() + "%";
	}else{
		
	}
}
function uploadComp(evt){
	document.getElementById("progressNumber").innerHTML = "上传状态：成功";
	document.getElementById("btnUpload").disabled = false;
}
function uploadFailed(evt){
	document.getElementById("progressNumber").innerHTML = "上传状态：失败" ;
	document.getElementById("btnUpload").disabled = false;
}
function uploadCanceled(evt){
	document.getElementById("progressNumber").innerHTML = "上传状态：被取消";
	document.getElementById("btnUpload").disabled = false;
}