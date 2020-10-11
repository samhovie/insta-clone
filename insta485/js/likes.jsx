import React from 'react';
import PropTypes from 'prop-types';

class Likes extends React.Component {
  /* Display number of likes and like/unlike button for one post
   * 
   * Props:
   * - url for api endpoint for like data
   * 
   * State:
   * - post_id
   * - numLikes
   * - userDidLike
   */

  constructor(props) {
    super(props);
    this.state = {
      num_likes: 0,
      user_likes_post: false,
    };
  }

  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    const { url } = this.props;

    // Call REST API to get number of likes
    fetch(url, { credentials: 'same-origin', method: 'GET' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          num_likes: data.likes_count,
          user_likes_post: data.logname_likes_this === 1,
        });
      })
      .catch((error) => console.log(error));
  }

  toggleLike() {
    const { url } = this.props;
    const num_likes = this.state.num_likes;
    const user_likes_post = this.state.user_likes_post;
    const method = user_likes_post ? 'DELETE' : 'POST';
    
    // Add/remove like
    fetch(url, { credentials: 'same-origin', method: method })
    .then((response) => {
      if (!response.ok) throw Error(response.statusText);
    })
    .catch((error) => console.log(error));

    // Update state
    this.setState({
      num_likes: (user_likes_post) ? (num_likes - 1) : (num_likes + 1),
      user_likes_post: !user_likes_post,
    });
  }

  render() {
    // This line automatically assigns this.state.numLikes to the const variable numLikes
    const { num_likes } = this.state;
    const { user_likes_post } = this.state;
    
    // Render number of likes
    return (
      <div className="likes">
        <p>
          {num_likes}
          {' '}
          {num_likes !== 1 ? 'likes' : 'like'}
        </p>

        <button className="like-unlike-button" onClick={() => this.toggleLike()}>
          {user_likes_post ? 'unlike' : 'like'}
        </button>
      </div>
    );
  }
}

Likes.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Likes;
