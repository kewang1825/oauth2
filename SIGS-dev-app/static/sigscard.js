function ShowCard(card) {
  // Create an AdaptiveCard instance
  var adaptiveCard = new AdaptiveCards.AdaptiveCard();

  // Set its hostConfig property unless you want to use the default Host Config
  // Host Config defines the style and behavior of a card
  adaptiveCard.hostConfig = new AdaptiveCards.HostConfig({
    fontFamily: "Segoe UI, Helvetica Neue, sans-serif"
    // More host config options
  });

  // Set the adaptive card's event handlers. onExecuteAction is invoked
  // whenever an action is clicked in the card
  adaptiveCard.onExecuteAction = function (action) {
    var signal = action.data == null ? null : action.data["signal"];
    ReactDOM.render(<ShowToken token={signal}/>, document.getElementById('token'));
  }

  // Parse the card payload
  adaptiveCard.parse(card);

  // Render the card to an HTML element:
  return adaptiveCard.render();
}

// Author a card
// In practice you'll probably get this from a service
// see http://adaptivecards.io/samples/ for inspiration
var card = {
    "type": "AdaptiveCard",
    "version": "1.0",
    "body": [
        {
            "type": "Image",
            "url": "http://adaptivecards.io/content/adaptive-card-50.png"
        },
        {
            "type": "TextBlock",
            "text": "Hello **Adaptive Cards!**"
        }
    ],
    "actions": [
        {
            "type": "Action.Submit",
            "title": "Get token",
            "data": {
              "signal": "AppUsage"
            }
        },
        {
            "type": "Action.ShowCard",
            "title": "Comment",
            "card": {
              "type": "AdaptiveCard",
              "body": [
                {
                  "type": "Input.Text",
                  "id": "comment",
                  "isMultiline": true,
                  "placeholder": "Enter your comment"
                }
              ],
              "actions": [
                {
                  "type": "Action.Submit",
                  "title": "OK",
                  "data": {
                    "signal": "CommentAdded"
                  }
                }
              ]
            }
        }
    ]
};

//ReactDOM.render(<ShowCard card={card} />, document.getElementById('adaptivecards'));
document.getElementById('adaptivecards').appendChild(ShowCard(card));

function ShowToken(props) {
  const token = props.token;
  if (token != null) {
    return <h2>{token}</h2>;
  }
  return <h2>Token to be generated here</h2>;
}

ReactDOM.render(<ShowToken />, document.getElementById('token'));
