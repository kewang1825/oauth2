// Author a card
// In practice you'll probably get this from a service
// see http://adaptivecards.io/samples/ for inspiration
var myCard = {
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
            "type": "Action.Http",
            "title": "Get Signals",
            "method": "GET",
            "url": "/api/getsignals"
        },
        {
            "type": "Action.Http",
            "title": "Learn more",
            "url": "https://aka.ms/sigs",
            "signal": "BrowserUsage"
        },
        {
            "type": "Action.Http",
            "title": "Open the App",
            "signal": "AppUsage"
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
                    },
                    {
                        "type": "ActionSet",
                        "spacing": "small",
                        "actions": [
                            {
                                "type": "Action.Http",
                                "title": "OK",
                                "url": "https://messagecardplaygroundfn.azurewebsites.net/api/HttpPost?code=zJaYHdG4dZdPK0GTymwYzpaCtcPAPec8fTvc2flJRvahwigYWg3p0A==&message=The comment was added successfully",
                                "signal": "CommentAdded",
                            }
                        ]
                    }
                ]
            }
        }
    ]
};

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
    adaptiveCard.onExecuteAction = function (action) {};

    // Parse the card payload
    adaptiveCard.parse(card);

    // Render the card to an HTML element:
    return adaptiveCard.render();
}

document.getElementById('adaptivecards').appendChild(ShowCard(myCard));
