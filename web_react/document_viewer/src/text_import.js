import React from 'react';
import PropTypes from 'prop-types';
import $ from 'jquery'

import {parseData} from './string_functions.js';
import configData from "./config.json";


function TextDownload(props) {

    function addOption(name) {

        var optionText = name;
        var optionValue = name;

        $('#texts_options').append(`<option value="${optionValue}">${optionText}</option>`);

    }

    function parse(dataIn, urlPart) {

        if (urlPart === "/texts_titles") {

            var fileNameData = dataIn.data;
            fileNameData.split(',').forEach(fileNameAndExt => {

                var fileName = fileNameAndExt.split('.')[0];
                addOption(fileName);

            });

            $('#read_ttitles').css('visibility', "hidden");

        } else {

            var fileContents = dataIn.data;
            let result = parseData(fileContents);
            let titles = result.titles;
            let textBodies = result.textBodies;
            props.setDocument(titles, textBodies);

        }
    }

    const fetchData = (urlPart) => {
        var url = ''.concat(configData.SERVER_URL, urlPart);
        fetch(url)
           .then(response => response.json())
           .then(json => parse(json, urlPart))
           .catch(err => console.log('Request Failed', err));  // Catch errors

    };

    const readTextTitles = () => {

        var urlPart = "/texts_titles";
        fetchData(urlPart);

    };

    const readSelectedText = () => {

        var fileNameSelectedText = document.getElementById("texts_options").value;
        var urlPart = ''.concat('/', fileNameSelectedText);

        fetchData(urlPart);

    };


    return (
      <>
        <div>

            <form>
              <label>Download text</label>
              <select name="texts" id="texts_options">
              </select>
            </form>

            <button
                id="read_ttitles"
                type="button"
                onClick={() => readTextTitles()}
              >Read text_titles</button>
            <button
                type="button"
                onClick={() => readSelectedText()}
              >Read Selected Text</button>

        </div>
      </>
    );

}


function TextImportLocal(props) {

    const inputElementOnchange = () => {

      const inputElement = document.getElementById("inputElement");
      const file = inputElement.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = (e) => {
        // e.target points to the reader

        const fileContents = e.target.result;

        let result = parseData(fileContents);
        let titles = result.titles;
        let textBodies = result.textBodies;
        props.setDocument(titles, textBodies);

      }
      reader.onerror = (e) => {
        const error = e.target.error;
        console.error(`Error occured while reading ${file.name}`, error);
      }
      reader.readAsText(file);

      }

    return (
        <form>
          <label>Load text
            <br />
            <input 
              id="inputElement"
              type="file" 
              onChange={(e) => inputElementOnchange(e.target.value)}
            />
          </label>
        </form>
    );

}


TextDownload.propTypes = {
    setDocument: PropTypes.func,
};

TextImportLocal.propTypes = {
    setDocument: PropTypes.func,
};

export {TextImportLocal, TextDownload};

