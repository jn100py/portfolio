import React from 'react';
import ReactDOM from 'react-dom';
import PropTypes from 'prop-types';

import './index.css';
import { TextImportLocal, TextDownload } from './text_import.js'
import DocumentStats from './statistics.js';


import { useState, useRef, useEffect, useContext, createContext } from "react";


function Section(props) {

    let [showtext, setShowText] = useState(false);
    let [hasFocus, setHasFocus] = useState(false);
    let [highlight, setHighlight] = useState("");


    const update = () => {

        showtext ? setShowText(false) : setShowText(true);

    }


    let query = useContext(Context).query;
    let newdoc = useContext(Context).docSwitchCurrent;
    let currentSectionTitle = useContext(Context).sectionTitleCurrent;



    if (newdoc === 1 && showtext === true && props.key !== 0) {

        setShowText(false); // always close when loading a new document

    }

    if (newdoc === 1 && showtext === false && props.key === 0) {

        setShowText(true);

    }

    if (currentSectionTitle === props.title && hasFocus === false) {

        setHasFocus(true);
        setShowText(true);

    }

    if (currentSectionTitle !== props.title && hasFocus === true) {

        setHasFocus(false);
        setShowText(false);

    }



    if (highlight === "" && props.text && query){

        if (query.charAt(0) !== "_") {

            if (props.text && props.text.join("").toLowerCase().includes(query.toLowerCase())) {

                setHighlight(query.toLowerCase());

            }

        } else {

            //whole word search

            var regexStr = "".concat('\\b', query.toLowerCase().replace(/_/g, ""), '\\b');
            var regex = new RegExp(regexStr);

            if (props.text && regex.test(props.text.join("").toLowerCase()) === true) {

                setHighlight(query.toLowerCase().replace(/_/g, ""));

            }
        }
    }

    if (query === "" && highlight !== "") {

        setHighlight("");

    }



    var buttonname = highlight !== "" ? "".concat(props.title, "*") : props.title;

    var text2Show = showtext && props.text ? props.text.join(" \n") : "";
    if (text2Show !== "" && highlight !== "") {

        var string2HighLight = new RegExp("(".concat(highlight, ")"), 'gi');
        text2Show = text2Show.replace(string2HighLight, "<mark>$1</mark>");

    }

    return (
      <>
        <button
          className="section_button"
          type="button"
          onClick={update}
        >{buttonname}</button>
        <p className="section" dangerouslySetInnerHTML={{__html: text2Show}} />
      </>
    );
}
  // See also:  https://blog.logrocket.com/using-dangerouslysetinnerhtml-in-a-react-application/


function Document(props) {

      return (
      <>
            {props.sectionIndices.map((i) => <Section key={i} title={props.sectionTitles[i]} text={props.sectionTexts[i]} />)}
      </>
    );

}


function Search(props) {

  const [query, setQuery] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    props.setQueryDv(query);
    setQuery("");
  }


  return (
    <form onSubmit={handleSubmit}>
      <label>Search text
        <br/>
        <input id='search_text'
               value={query}
               type="text"
               onChange={(e) => setQuery(e.target.value)}
        />
      </label><br/>
      <input type="submit" value='Submit' />

      <button
        type="button"
        onClick={() => alert("Hints:\nType _<word>_ to search whole word (for example _Nederland_)\nA part of a word can also be used in a query.\nUse an empty string to reset the search results.")}
      >?</button>

    </form>
  );

}


const Context = createContext();

function DocumentViewer() {

    const [sectionTitles, setSectionTitles] = useState([]);
    const [sectionTexts, setSectionTexts] = useState([]);
    const [sectionTitlePointerIndex, setSectionTitlePointerIndex] = useState(-1);
    const [query, setQuery] = useState("");
    let docSwitch = useRef(0);


    let sectionIndices = [...Array(sectionTitles.length).keys()]

    const setDocument = (titles, texts) => {

        docSwitch.current = 1;
        setQuery("");
        setSectionTitles(titles);
        setSectionTexts(texts);
        setSectionTitlePointerIndex(-1);

      };

    const setQueryDV = (queryIn) => {

        setQuery(queryIn);

    };


    useEffect(() => {

        docSwitch.current = 0;

    }, [sectionTitles]);


    let props = {titles: sectionTitles, contents: sectionTexts};
    let propsSearch = {setQueryDv: setQueryDV};

    let contextValues = {
        'sectionTitleCurrent': sectionTitles[sectionTitlePointerIndex],
        'query': query,
        'docSwitchCurrent': docSwitch.current
    };


    return (
    <>
      <div style={{display: "grid", gridTemplateColumns: "0.01% 9.99% 65% 25%", gridGap: 20}}>
        <div>
        </div>
        <div>

          <TextImportLocal setDocument={setDocument}/>
          <br />

          <TextDownload setDocument={setDocument}/>
          <br />

          <Search {...propsSearch} />
          <br />

          <button
            type="button"
            onClick={() => setSectionTitlePointerIndex(sectionTitlePointerIndex === -1 ? -1 : sectionTitlePointerIndex - 1)}
          >Previous</button>
          <button
            type="button"
            onClick={() => setSectionTitlePointerIndex(sectionTitlePointerIndex === sectionTitles.length - 1 ? sectionTitles.length - 1 : sectionTitlePointerIndex + 1)}
          >Next</button>
          <button
           type="button"
           onClick={() => alert("Click Next to open the next section. A section can also be opened by clicking on its title.")}
         >?</button>

        </div>
        <div id="middlecolumn">
          <Context.Provider value={contextValues}>
          <Document
            sectionTitles={sectionTitles}
            sectionTexts={sectionTexts}
            sectionIndices={sectionIndices}
          />
          </Context.Provider>

        </div>
        <div>

          <h4>Document Statistics</h4>
          <DocumentStats {...props} />
          <br />

        </div>
      </div>
    </>
    );
}


Section.propTypes = {
    key: PropTypes.number,
    title: PropTypes.string,
    text: PropTypes.string,
};

Document.propTypes = {
    sectionTitles: PropTypes.array,
    sectionTexts: PropTypes.array,
    sectionIndices: PropTypes.array,
};


Search.propTypes = {
    setQueryDv: PropTypes.func,
};


ReactDOM.render(<DocumentViewer />, document.getElementById('root'));

