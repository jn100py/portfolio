import React from 'react';
import PropTypes from 'prop-types';


class ListItem extends React.Component {

  render() {
      return (
          <li key="{this.props.key}">{this.props.section_title + '   ' + this.props.number_words.toString()}</li>
      );
  }
}


class DocumentStats extends React.Component {
  constructor(props) {

    super(props);
    this.state = {
        indices: Array(this.props.titles.length).fill(0), 
        titles: this.props.titles,
        contents: this.props.contents
    };
  }

  static getDerivedStateFromProps(nextProps) {
    // A component is updated whenever there is a change in the component's state or props

    const indicesNew = [...Array(nextProps.titles.length).keys()];

    return {
        indices: indicesNew,
        titles: nextProps.titles,
        contents: nextProps.contents
    };
  }

  calculateNumber(index) {
  
    if (this.state.contents[index]) {

        return this.props.contents[index].join("").split(" ").length;
    
    }

    return 0;

  }

  render() {
      return (
            <>
                <p>Number of words per section</p>
                <ul>
                    {this.state.indices.map((index) =>  <ListItem key={index}
                                                                  section_title={this.state.titles[index]}
                                                                  number_words={this.calculateNumber(index)}
                                                                  />
                     )}
                </ul>
            </>
      );
  }
}


ListItem.propTypes = {
    key: PropTypes.string,
    section_title: PropTypes.string,
    number_words: PropTypes.number,
};

DocumentStats.propTypes = {
    indices: PropTypes.array,
    titles: PropTypes.array,
    contents: PropTypes.array,
};


export default DocumentStats;

