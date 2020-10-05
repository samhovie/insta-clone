import React from 'react';
import PropTypes from 'prop-types';

class Likes extends React.Component {
  /* Display number of likes and like/unlike button for one post
   * Reference on forms https://facebook.github.io/react/docs/forms.html
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = { numLikes: 0 };
  }

  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    const { url } = this.props;

    // Call REST API to get number of likes
    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          numLikes: data.likes_count,
        });
      })
      .catch((error) => console.log(error));
  }

  render() {
    // This line automatically assigns this.state.numLikes to the const variable numLikes
    const { numLikes } = this.state;

    // Render number of likes
    return (
      <div className="likes">
        <p>
          {numLikes}
          {' '}
          like
          {numLikes !== 1 ? 's' : ''}
        </p>
      </div>
    );
  }
}

Likes.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Likes;
