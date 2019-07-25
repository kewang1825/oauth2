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
    const element = <h2>{signal}</h2>
    ReactDOM.render(element, document.getElementById('signal'));

    var token = document.getElementById('token').innerText;

    if (signal == null) {
        $.getJSON($SCRIPT_ROOT + '/getsignals?token=' + token, null, function(data) {
            $('#result').text(JSON.stringify(data, null, 2));
        });
    } else {
        $.post($SCRIPT_ROOT + '/postsignal?signal=' + signal + '&token=' + token, function(data) {
            $('#result').text(data);
        });
    }
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
            "type": "Action.OpenUrl",
            "title": "Get Signals",
        },
        {
            "type": "Action.Submit",
            "title": "I used this app",
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
