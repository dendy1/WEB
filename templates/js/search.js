<script>
    function getFile(filePath) {
        return filePath.substr(filePath.lastIndexOf('\\') + 1);
    }

    if(typeof(String.prototype.trim) === "undefined")
    {
        String.prototype.trim = function()
        {
            String.replace(/(^[ '\^\$\*#&]+)|([ '\^\$\*#&]+$)/g, '')
        };
    }

    function getExtension(fileName) {
        return fileName.split('.').pop();
    }

    var PATHES = '{{ PATHES }}';
    let input = document.querySelector('input');
    input.onkeyup = function () {
        let html = '';

        if (input.value) {
            let search = String(input.value);

            for (path of PATHES) {

                let tempFileName = getFile(path);

                if (search.startsWith("\"") && search.endsWith("\"")) {
                    if (tempFileName === search) {
                        html += '<li>' + path + '</li>'
                    }
                }
                else if (search.startsWith("*")) {
                    let trimmed = search.trim();

                    if (trimmed.startsWith(".")) {
                        if (getExtension(tempFileName) === getExtension(trimmed)) {
                            html += '<li>' + path + '</li>'
                        }
                    }
                    else {
                        if (tempFileName.includes(search)) {
                            html += '<li>' + path + '</li>'
                        }
                    }
                }
            }
        }

        document.querySelector('ul').innerHTML = html;
    }
</script>