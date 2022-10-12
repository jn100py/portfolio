const parseData = (fileContents) => {

    const titlePattern = '#.*';
    const lines = fileContents.split("\n");

    let titles = [];
    let textBody = [];
    let textBodies = [];

    for (let i = 0; i < lines.length; i++) {

        let line = lines[i];
        let isTitle = line.match(titlePattern) ? true : false;

        if (isTitle) { 

            let title = line.substr(1, line.length).trim();
            titles.push(title);

            if (textBody.length === 0) {
                continue;
            }

            textBodies.push(textBody);
            textBody = [];

        } else {

            textBody.push(line);

        }
    }

    if (textBody.length > 0) {
        textBodies.push(textBody);
    }

    return {titles, textBodies};

};

export {parseData};

