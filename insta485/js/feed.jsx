import React from 'react';
import PropTypes from 'prop-types';
import InfiniteScroll from 'react-infinite-scroll-component';
import Post from './post';

class Feed extends React.Component {
  /*
    Props:
    - url for rest api to retrieve post info

    State:
    - next url to retrieve posts from
    - posts list containing post_ids and post urls
  */

  constructor(props) {
    super(props);
    this.state = {
      next: '',
      posts: [],
    };
    this.fetchPosts = this.fetchPosts.bind(this);
  }

  componentDidMount() {
    const { url } = this.props;
    const [navigation] = performance.getEntriesByType('navigation');
    console.log(navigation);

    if (navigation.type !== 'reload' && window.history.state !== null) {
      this.setState(window.history.state);
    } else {
      fetch(url, { credentials: 'same-origin', method: 'GET' })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          this.setState({
            next: data.next,
            posts: data.results,
          });
        })
        .catch((error) => console.log(error));
    }
  }

  fetchPosts() {
    const { next, posts } = this.state;

    if (next === '') return;

    fetch(next, { credentials: 'same-origin', method: 'GET' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        const newPosts = posts.concat(data.results);
        this.setState({
          next: data.next,
          posts: newPosts,
        });
        window.history.replaceState({
          next: data.next,
          posts: newPosts,
        }, '');
      })
      .catch((error) => console.log(error));
  }

  render() {
    const { next, posts } = this.state;
    const postItems = posts.map((postData) => (
      <Post key={postData.postid} url={postData.url} postid={postData.postid} />
    ));

    return (
      <InfiniteScroll
        dataLength={postItems.length}
        next={this.fetchPosts}
        hasMore={next !== ''}
        loader={<h4>Loading...</h4>}
      >
        {postItems}
      </InfiniteScroll>
    );
  }
}

Feed.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Feed;
