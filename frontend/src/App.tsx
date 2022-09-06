import './App.css';
import useSWR, { Fetcher } from 'swr';

function NewTweetForm() {
  return (
    <form action="/tweets/add/" method="POST">
      <p><label htmlFor="new_tweet">New tweet message:</label></p>
      <textarea id="new_tweet" name="new_tweet" rows={4} cols={50}></textarea>
      <br />
      <input type="submit" value="Submit" />
    </form>
  );
}

type TweetsProps = {
  tweets: Tweet[]
}

function Tweets(props: TweetsProps) {
  const { tweets } = props;

  let items = [];

  for (let tweet of tweets) {
    let user = tweet.user;
    let message = tweet.message;
    let postTime = tweet.post_time;

    let item = (<li><p> <a href="{% url 'profile' tweet.user.username %}">@{user}</a> on {postTime}: {message}</p></li>);

    items.push(item);
  }
  return (
    <ul>
      {items}
    </ul>
  );
}

function App() {

  const {data, error} = useSWR("/tweets/api/all", allTweets);

  if (!data) {
    return (
      <h1>Loading</h1>
    );
  }

  return (
    <div>
      <h1>Tweets account page</h1>
      <h2>@{data[0].user}</h2>
      <h3>Latest messages</h3>

      <NewTweetForm />
      <Tweets tweets={data} />

      <p><a href="{% url 'logout' %}">Log Out</a></p>
    </div>
  );
}

export default App;

interface Tweet {
  user: string;
  message: string;
  post_time: string;
}


const allTweets = (path: string) : Promise<Tweet[]> => fetch(`http://localhost:8000${path}`).then((res) => res.json()); 


