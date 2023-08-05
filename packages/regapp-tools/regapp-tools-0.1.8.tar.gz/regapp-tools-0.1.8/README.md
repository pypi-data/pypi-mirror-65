# regapp-tools

These is a collection of (python for the moment) tools for regapp.

Main goal of this package is to have them easily installable via:

```
    pip install regapp-tools
```

The initial tools are:

- subiss-to-unix that allows finding a user that was registered via OIDC
  in regapp. Examples:

  - `subiss-to-unix <sub>@<iss>`
  - `subiss-to-unix 6c611e2a-2c1c-487f-9948-c058a36c8f0e@https://login.helmholtz-data-federation.de/oauth2`

- ssh-key-retriever (there is a go version in an rpm package available
  elsewhere). This one is for retrieving ssh-keys that users have
  registered in reg-app. Examples:

  - `ssh-key-retriever <username>`

