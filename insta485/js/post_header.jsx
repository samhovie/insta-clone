import React from 'react';
import moment from 'moment';
import PropTypes from 'prop-types';

const PostHeader = ({
  timestamp,
  ownerUsername,
  ownerPageURL,
  ownerImgURL,
  postPageURL,
}) => (
  <header className="post-header">
    <a href={ownerPageURL}>
      <img src={ownerImgURL} alt={ownerUsername} />
      <p>{ownerUsername}</p>
    </a>

    <a href={postPageURL}>
      {moment.utc(timestamp).fromNow()}
    </a>
  </header>
);

PostHeader.propTypes = {
  timestamp: PropTypes.string.isRequired,
  ownerUsername: PropTypes.string.isRequired,
  ownerPageURL: PropTypes.string.isRequired,
  ownerImgURL: PropTypes.string.isRequired,
  postPageURL: PropTypes.string.isRequired,
};

export default PostHeader;
