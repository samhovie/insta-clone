import React from 'react';
import PropTypes from 'prop-types';

class Likes extends React.Component {
  /* Display number of likes and like/unlike button for one post
   *
   * Props:
   * - num_likes
   * - user_likes_post
   * - setLike callback function
   */

  constructor(props) {
    super(props);
    this.toggleLike = this.toggleLike.bind(this);
  }

  toggleLike() {
    const { userLikesPost, setLike } = this.props;
    if (userLikesPost) {
      // Remove user's like from post
      setLike(false);
    } else {
      // Add user's like to post
      setLike(true);
    }
  }

  render() {
    // This line automatically assigns this.state.numLikes to the const variable numLikes
    const { numLikes, userLikesPost } = this.props;

    // Render number of likes
    return (
      <div className="likes">
        <p>
          {numLikes}
          {' '}
          {numLikes !== 1 ? 'likes' : 'like'}
        </p>

        <button type="submit" className="like-unlike-button" onClick={() => this.toggleLike()}>
          {userLikesPost ? 'unlike' : 'like'}
        </button>
      </div>
    );
  }
}

Likes.propTypes = {
  numLikes: PropTypes.number.isRequired,
  userLikesPost: PropTypes.bool.isRequired,
  setLike: PropTypes.func.isRequired,
};

export default Likes;
