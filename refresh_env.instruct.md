# 1. Open this URL in your browser to get your Authorization Code:
# Expected: You are redirected to YOUR_REDIRECT_URI with a query parameter ?code=YOUR_AUTHORIZATION_CODE

| ==  == |
https://id.twitch.tv/oauth2/authorize?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI&scope=user:read:email+user:read:broadcast+channel:read:subscriptions+chat:read+chat:edit&force_verify=true
                                                                   ^^^^^^^^^^^^^^              ^^^^^^^^^^^^^^^^^
auth code ===> http://localhost/?code=[CODE]

# 2. Exchange the Authorization Code for tokens:

client | ==  == |
secret | ==  == |
auth   | ==  == |
redirt | ==  == |
# note, only works in cmd
curl -X POST "https://id.twitch.tv/oauth2/token" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "code=YOUR_AUTHORIZATION_CODE" \
  -d "grant_type=authorization_code" \
  -d "redirect_uri=YOUR_REDIRECT_URI"
# Expected output (JSON):
# {
#   "access_token": "ACCESS_TOKEN",
#   "refresh_token": "REFRESH_TOKEN",
#   "expires_in": 3600,
#   "scope": "user:read:email user:read:broadcast channel:read:subscriptions chat:read chat:edit",
#   "token_type": "bearer"
# }

# 3. Refresh your tokens:

refresh | ==  == |
client  | ==  == |
secret  | ==  == |
# note, only works in cmd
curl -X POST "https://id.twitch.tv/oauth2/token" \
  -d "grant_type=refresh_token" \
  -d "refresh_token=YOUR_REFRESH_TOKEN" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET"
# Expected output (JSON):
# {
#   "access_token": "NEW_ACCESS_TOKEN",
#   "refresh_token": "NEW_REFRESH_TOKEN",
#   "expires_in": 3600,
#   "scope": "user:read:email user:read:broadcast channel:read:subscriptions chat:read chat:edit",
#   "token_type": "bearer"
# }

# 4. Validate your Access Token:

access | ==  == |
# note, only works in cmd
curl -X GET "https://id.twitch.tv/oauth2/validate" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
# Expected output (JSON):
# {
#   "client_id": "YOUR_CLIENT_ID",
#   "login": "USERNAME",
#   "scopes": ["user:read:email", "user:read:broadcast", "channel:read:subscriptions", "chat:read", "chat:edit"],
#   "user_id": "USER_ID",
#   "expires_in": 3600
# }
