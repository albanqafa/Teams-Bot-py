# Teams-Bot-py
Microsoft Teams Bot in Python

This is an "old-school" style bot for Microsoft Teams

It uses the msal library to authenticate with Azure via an App Registration to read channel messages using Microsoft's Graph API for Teams, and sends messages with the "Incoming Webhook" addon for the channel you want to send to.

Azure Requirements:

The Azure App Registration requires the following Application-Level (not Delegated) permissions for the app to read channel messages (maybe a bit less than this) -

![image](https://user-images.githubusercontent.com/37601993/220479533-a2d07b37-b82a-487d-8dd3-2f2e6dc5ece0.png)

Listing Teams Channel messages via Graph API is a "Protected API" -

https://learn.microsoft.com/en-us/graph/teams-protected-apis

You will likely need to request access to protected API's and get your App Registration accepted for this to work -

https://forms.office.com/pages/responsepage.aspx?id=v4j5cvGGr0GRqy180BHbR1ax4zKyZjVBmutzKVo1pVtURTVXM0wzSldCTjVERDlYRE1WWktQRDhURCQlQCN0PWcu
