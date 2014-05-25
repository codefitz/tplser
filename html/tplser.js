window.onload = function() {
		var fileInput = document.getElementById('fileInput');
		var fileDisplayArea = document.getElementById('fileDisplayArea');
        var inputFileNameToSaveAs = document.getElementById('inputFileNameToSaveAs');

		fileInput.addEventListener('change', function(e) {
			var file = fileInput.files[0];
            var filename = file.name;

			if (file.name.match('.(tpl|txt)')) {
				var reader = new FileReader();

				reader.onload = function(e) {
					fileDisplayArea.textContent = reader.result;
                    inputFileNameToSaveAs.value = filename;
				}

				reader.readAsText(file);
			} else {
				fileDisplayArea.innerText = "Not a supported file!";
			}
		}
        );
}