import React from 'react';
import PropTypes from 'prop-types';

class CommentForm extends React.Component {
  /** Form for submitting comments on post
   *
   * Props:
   * - updateComments callback to update comment state
   *
   * State:
   * - value of the text in the form
   */

  constructor(props) {
    super(props);
    this.state = {
      value: '',
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({
      value: event.target.value,
    });
  }

  handleSubmit(event) {
    const { updateComments } = this.props;
    const { value } = this.state;
    updateComments(value);
    this.setState({
      value: '',
    });
    event.preventDefault();
  }

  render() {
    const { value } = this.state;
    return (
      <form
        className="comment-form"
        onSubmit={(event) => this.handleSubmit(event)}
      >
        <input
          type="text"
          value={value}
          onChange={(event) => this.handleChange(event)}
        />
        <input type="submit" style={{ visibility: 'hidden' }} />
      </form>
    );
  }
}

CommentForm.propTypes = {
  updateComments: PropTypes.func.isRequired,
};

export default CommentForm;
