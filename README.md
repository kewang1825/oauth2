# OAuth2 workflows

| Component | Description |
| --- | --- |
| myapp | A native app that user can sign in to retrieve the user token and communicates with mywebapp |
| myserv | A service that uses server-to-server token to communicate with mywebapp |
| mywebapp | The web service that supports on-behalf-of or client-credential workflow to access O365 Graph |

```
myapp  \
        --> mywebapp --> O365 Graph
myserv /
```

# On-behalf-of workflow

![Alt text](/docs/on-behalf-of.jpg?raw=true "On-behalf-of workflow")


# client-credential workflow

![Alt text](/docs/client-credential.jpg?raw=true "On-behalf-of workflow")
