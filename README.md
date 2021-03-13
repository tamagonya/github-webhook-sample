# Github Webhook Sample

Sample script for Github's webhook repository creation event receiver.

This sample script updates branch projection setting and creates issue when webhook event for repository creation event is detected.

## Prerequisites

- Python 3.6 or higher
- Packages
   - Requests: https://pypi.org/project/requests/
   - Flask: https://pypi.org/project/Flask/

## Getting Started

1. Prepare project with Requests and Flask packages
2. Modify TOKEN in app.py
3. Deploy app.py to your project
4. Execute app.py. Webhook event endpoint looks like followings;

    `http://localhost:port/webhook`

5. Configure Github webhook settings with launched webhook event endpoint

   - Setting up a webhook https://docs.github.com/en/developers/webhooks-and-events/creating-webhooks#setting-up-a-webhook
   - Configuring your server to receive payloads: https://docs.github.com/en/developers/webhooks-and-events/configuring-your-server-to-receive-payloads

## References

Github Webhook: https://docs.github.com/en/developers/webhooks-and-events/about-webhooks


 