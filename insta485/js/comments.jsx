import React from 'react';
import PropTypes from 'prop-types';

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
        }
      ],
    }
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
      let comments = [];
      data.comments.forEach((datum) => {
        let comment = {
          comment_id: datum.commentid,
          comment_owner: datum.owner,
          comment_owner_page_url: datum.owner_show_url,
          comment_text: datum.text,
        }
        comments.push(comment);
      });

      this.setState({
        comments: comments,
      });
    })
    .catch((error) => console.log(error));
  }

  // comment_data should be json parsed response of POST request to
  // /api/v1/p/<post_id>/comments/
  updateComments(comment_data) {
    let comments  = this.state.comments.slice();
    comments.push({
      comment_id: comment_data.commentid,
      comment_owner: comment_data.owner,
      comment_owner_page_url: comment_data.owner_show_url,
      comment_text: comment_data.text,
    });

    this.setState({
      comments: comments,
    });
  }

  render() {
    const { url } = this.props;
    const { comments } = this.state;
    const comment_items = comments.map((comment_data) => {
      return (
        <li key={comment_data.comment_id}>
          <a href={comment_data.comment_owner_page_url}> {comment_data.comment_owner} </a>
          <p> {comment_data.comment_text} </p>
        </li>
      );
    });

    return (
      <div className="comments">
        <ul>{comment_items}</ul>
        <CommentForm url={url} updateComments={this.updateComments} />
      </div>
    )
  }
}


class CommentForm extends React.Component {
  /** Form for submitting comments on post
   * 
   * Props:
   * - url for api endpoint to submit comment
   * - callback to update comment state
   * 
   * State:
   * - value of the text in the form
   */

  constructor(props) {
    super(props);
    this.state = {
      value: '',
    }
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({
      value: event.target.value,
    });
  }

  handleSubmit(event) {
    // If submission is empty, don't do anything
    if (this.state.value === '') {
      return;
    }
    
    const { url } = this.props;
    const body = {
      text: this.state.value,
    }

    // Post the comment
    fetch(
      url, 
      {
        credentials: 'same-origin',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(body),
      }
    )
    .then((response) => {
      if (!response.ok) throw Error(response.statusText);
      return response.json();
    })
    .then((data) => {
      // Update comments with data in post response
      this.props.updateComments(data);
    })
    .catch((error) => console.log(error));

    // After comment is submitted, clear form
    this.setState({
      value: '',
    });

    event.preventDefault();
  }

  render() {
    const { value } = this.state;
    return (
      <form className="comment-form" onSubmit={(event) => this.handleSubmit(event)}>
        <input
          type="text"
          value={value}
          onChange={(event) => this.handleChange(event)}
        />
        <input type="submit"></input>
      </form>
    );
  }
}

Comments.propTypes = {
  url: PropTypes.string.isRequired,
};

CommentForm.propTypes = {
  url: PropTypes.string.isRequired,
  updateComments: PropTypes.func.isRequired,
};

export default Comments;
