window.onload = function() {
		var fileInput = document.getElementById('fileInput');
		var fileDisplayArea = document.getElementById('fileDisplayArea');

		fileInput.addEventListener('change', function(e) {
			var file = fileInput.files[0];

			if (file.name.match('.(tpl|txt)')) {
				var reader = new FileReader();

				reader.onload = function(e) {
					fileDisplayArea.innerText = reader.result;
				}

				reader.readAsText(file);
			} else {
				fileDisplayArea.innerText = "Not a supported file!";
			}
		}
        );
        //var pre = document.getElementsByTagName('pre'),
        //pl = pre.length;
        //for (var i = 0; i < pl; i++) {
        //    pre[i].innerHTML = '<span class="line-number"></span>' + pre[i].innerHTML + '<span class="cl"></span>';
        //    var num = pre[i].innerHTML.split(/\n/).length;
        //    for (var j = 0; j < num; j++) {
        //        var line_num = pre[i].getElementsByTagName('span')[0];
        //        line_num.innerHTML += '<span>' + (j + 1) + '</span>';
        //    }
        //};
}