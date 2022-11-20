var http = require('http');
var fs = require('fs');
var url = require('url');


function getAllFilesFromFolder (dir) {

    var results = [];

    fs.readdirSync(dir).forEach(function (dirItemName) {

        var filePath = dir + '/' + dirItemName;
        var stat = fs.statSync(filePath);

        if (stat && stat.isDirectory()) {

            results = results.concat(getAllFilesFromFolder(filePath));

        } else {
        
            fileName = filePath.split('/').pop();
            results.push(fileName);

        }

    });

    return results;

};


http.createServer(function (request, result) {

    var urlData = url.parse(request.url, true);

    if (urlData.pathname === '/texts_titles') {

        var filenames = getAllFilesFromFolder("./texts");

        result.writeHead(200, {"Access-Control-Allow-Origin": "*"},
                              {'Content-Type': 'application/json'});
        result.write(JSON.stringify({"data" : filenames.join(",")}));

        return result.end();


    } else {

        var pathTextFile = "./texts".concat(urlData.pathname, '.txt');

        fs.readFile(pathTextFile, 'utf8', function (err, data) {

            result.writeHead(200, {"Access-Control-Allow-Origin": "*"},
                                  {'Content-Type': 'application/json'});
            result.write(JSON.stringify({"data" : data}));

            return result.end();

        });

    }
}).listen(8080);

