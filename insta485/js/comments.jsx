import React from 'react';
import PropTypes from 'prop-types';
import CommentForm from './comment_form';

class Comments extends React.Component {
  /* Display number of likes and like/unlike button for one post
   *
   * Props:
   * - url for api endpoint for comment data
   *
   * State:
   * - comments - list of dicts
   */

  constructor(props) {
    super(props);
    this.state = {
      comments: [
        {
          comment_id: 0,
          comment_owner: '',
          comment_owner_page_url: '',
          comment_text: '',
        },
      ],
    };
    this.updateComments = this.updateComments.bind(this);
  }

  componentDidMount() {
    const { url } = this.props;

    fetch(url, { credentials: 'same-origin', method: 'GET' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      }).then((data) => {
        // Transform JSON data into list of dicts with relevant data
        const comments = [];
        data.comments.forEach((datum) => {
          const comment = {
            comment_id: datum.commentid,
            comment_owner: datum.owner,
            comment_owner_page_url: datum.owner_show_url,
            comment_text: datum.text,
          };
          comments.push(comment);
        });

        this.setState({ comments });
      })
      .catch((error) => console.log(error));
  }

  updateComments(value) {
    // If submission is empty, don't do anything
    if (value === '') {
      return;
    }

    const { url } = this.props;
    const body = {
      text: value,
    };

    // Post the comment
    fetch(
      url,
      {
        credentials: 'same-origin',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      },
    )
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState((prevState) => {
          const { comments } = prevState;
          comments.push({
            comment_id: data.commentid,
            comment_owner: data.owner,
            comment_owner_page_url: data.owner_show_url,
            comment_text: data.text,
          });
          return ({ comments });
        });
      })
      .catch((error) => console.log(error));
  }

  render() {
    const { url } = this.props;
    const { comments } = this.state;
    const commentItems = comments.map((commentData) => (
      <li key={commentData.comment_id}>
        <a href={commentData.comment_owner_page_url}>
          {commentData.comment_owner}
        </a>
        <p>
          {commentData.comment_text}
        </p>
      </li>
    ));

    return (
      <div className="comments">
        <ul>{commentItems}</ul>
        <CommentForm url={url} updateComments={this.updateComments} />
      </div>
    );
  }
}

Comments.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Comments;
