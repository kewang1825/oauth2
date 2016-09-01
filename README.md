# OAuth2 workflows

| Component | Description |
| --- | --- |
| myapp | The native app that user can sign in to retrieve the user token A and communicates with mywebapp |
| myserv | The other service that uses server-to-server token to communicate with mywebapp |
| mywebapp | The web service that takes the user token A and convert it to on-behalf-of token B to access O365 graph API |

##myapp  \
##        --> mywebapp --> O365 Graph
##myserv /