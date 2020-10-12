import React from 'react';
import PropTypes from 'prop-types';
import PostHeader from './post_header';
import PostContent from './post_content';
import Likes from './likes';
import Comments from './comments';

class Post extends React.Component {
  /* Display entire Insta485 post: header, image, likes, comments
  *
  * Props:
  * - post_id
  * - url for api endpoint for post data
  *
  * State:
  * - post_data
  * - likes_data
  */

  constructor(props) {
    super(props);
    this.state = {
      postData: {
        age: '',
        img_url: '',
        owner: '',
        owner_img_url: '',
        owner_show_url: '',
        post_show_url: '',
        url: '',
      },
      likesData: {
        logname_likes_this: false,
        likes_count: 0,
        postid: 0,
        url: '',
      },
    };
    this.setLike = this.setLike.bind(this);
  }

  componentDidMount() {
    const { url, postid } = this.props;
    const likesURL = `/api/v1/p/${postid}/likes/`;

    fetch(url, { credentials: 'same-origin', method: 'GET' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        const postData = data;
        const { likesData } = this.state;

        this.setState({ postData, likesData });
      })
      .catch((error) => console.log(error));

    fetch(likesURL, { credentials: 'same-origin', method: 'GET' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        const { postData } = this.state;
        const likesData = data;
        likesData.logname_likes_this = likesData.logname_likes_this === 1;

        this.setState({ postData, likesData });
      })
      .catch((error) => console.log(error));
  }

  // add_like should be a boolean - if true will add, if false will remove
  setLike(addLike) {
    const { postData, likesData } = this.state;
    const method = addLike ? 'POST' : 'DELETE';

    // Add/remove like
    fetch(likesData.url, { credentials: 'same-origin', method })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
      })
      .catch((error) => console.log(error));

    // Update state
    if (addLike) {
      likesData.likes_count += 1;
      likesData.logname_likes_this = true;
    } else {
      likesData.likes_count -= 1;
      likesData.logname_likes_this = false;
    }

    this.setState({ postData, likesData });
  }

  render() {
    const { postid } = this.props;
    const { postData, likesData } = this.state;
    const commentsURL = `/api/v1/p/${postid}/comments/`;

    return (
      <div className="post">
        <PostHeader
          timestamp={postData.age}
          ownerUsername={postData.owner}
          ownerPageURL={postData.owner_show_url}
          ownerImgURL={postData.owner_img_url}
          postPageURL={postData.post_show_url}
        />
        <PostContent
          postImgURL={postData.img_url}
          userLikesPost={likesData.logname_likes_this}
          setLike={this.setLike}
        />
        <Likes
          numLikes={likesData.likes_count}
          userLikesPost={likesData.logname_likes_this}
          setLike={this.setLike}
        />
        <Comments url={commentsURL} />
      </div>
    );
  }
}

Post.propTypes = {
  postid: PropTypes.number.isRequired,
  url: PropTypes.string.isRequired,
};

export default Post;
