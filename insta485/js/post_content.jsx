import React from 'react';
import PropTypes from 'prop-types';

class PostContent extends React.Component {
  /*
  Props:
  - post_img_url
  - user_likes_post
  - setLike callback function
  */

  constructor(props) {
    super(props);
    this.likePost = this.likePost.bind(this);
  }

  likePost() {
    const { userLikesPost, setLike } = this.props;
    if (userLikesPost) {
      return;
    }
    setLike(true);
  }

  render() {
    const { postImgURL } = this.props;
    return (
      <picture className="post-content" onDoubleClick={() => this.likePost()}>
        <img src={postImgURL} alt="post-content" />
      </picture>
    );
  }
}

PostContent.propTypes = {
  postImgURL: PropTypes.string.isRequired,
  userLikesPost: PropTypes.bool.isRequired,
  setLike: PropTypes.func.isRequired,
};

export default PostContent;
