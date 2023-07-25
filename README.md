# Yes, This is a Warcrime

This project is not associated with the primary MLP r/place 2023 efforts whatsoever. It only makes use of the publicly available templates. 

**It is exclusively a personal endeavour**

### misc terminal commands:

`python main.py -p [username] [password] -t [token] -am token`

`python main.py -p [username] [password] -t [token] -am token -nsp`

`python main.py -t eyJhbGciOiJSUzI1NiIsImtpZCI6IlNIQTI1NjpzS3dsMnlsV0VtMjVmcXhwTU40cWY4MXE2OWFFdWFyMnpLMUdhVGxjdWNZIiwidHlwIjoiSldUIn0.eyJzdWIiOiJ1c2VyIiwiZXhwIjoxNjkwMjk3NjczLjA3MDUzMywiaWF0IjoxNjkwMjExMjczLjA3MDUzMywianRpIjoiblZ1bW9UOEdncUtjTWYzLV9PSEQwSTFzWkthUWtBIiwiY2lkIjoiOXRMb0Ywc29wNVJKZ0EiLCJsaWQiOiJ0Ml9samV1b2hreCIsImFpZCI6InQyX2xqZXVvaGt4IiwibGNhIjoxNjQ5MDg5NzQyODczLCJzY3AiOiJlSnhra2RHTzlDQUloZC1GYTVfZ2Y1VV9tNDFWT2tOV3BRSHNaTjUtWXl1ZEpudlZBLWRUNGZRX1lJMVVJTUJHQkFGaVN0eWJRWUFrbURPWlFnRE1ORHByaVNRUTRFbHFMRzhJUUJtYmtRMVphTWNhVzN3Z0JLaWNFN2VWSHBjMm9hVWJpNTRkdjZweUxqeXBPVWZsM05qbUxXeFA5RE1icTAycFdOWlRtY1IxcFhRV0xfb1pPOVMzOXVVel9TYTBSOE9LcXZHQm95TVk4X0haV01aaUd2ZnhucHIwWkYwd3E3M0xRV3BmNnJHNzlrV1QwREs0X1J4dnZEYVRHWEplbXA3Ul90MzFTLWpBUGNfTDlOcUJHYXY3WHJydFdidF8xUTVVemlqUldKejROQnk1Y3ZrZXZ3VGJOZWxmNDNaa0xMNFpjZE1iZm1zNk9uSng0dENuOGZVYkFBRF9fMThTMkZFIiwicmNpZCI6Im5ISVpud1lVc2l6LTg2eVdpVjFoeFdYNU1kWlp0dXBDaDFrS3JiU1BZRUEiLCJmbG8iOjJ9.ml4cEIpMEmiw-B1DFUh_FDA5h5xawAhiTN4_Qzw6AxrPPiAUWS8UzhnA-QGJ0mLxw5SKU0NfR-8cWjTRtKyipbXwg8tvDp6cDJ_gYsNF1dWW7V5jiOnMhIDuM18YbytwRq2kFU5sXlvq87-WVkmuepWICI7t-Bsd42miMPIPKrqmsMq-38D8lc6U-WaXaxcjrOkbfJz9csbpIjfVGcIafRmMkqDaFJ22kAlgOYFKMsYi3RIPo071vxnZfXV5nDKwSf7d90EfR8uxsPZ_o2usn8ql1_rpc7capMKFBqCm8JD5uDlg3qdgBO-dmWH9Ajf2omI6aOns8BQptYH14ilSug -am token -nsp`

``


## Portainer Commands

CMD

`'-t' '[token]' '-am' 'token'`

`'-t' '[token]' '-am' 'token' '-dt' '[time]'`

`'-t' '[token]' '-am' 'token' '-nsp' '-nm' '-ovst'` (status checker mode with no mask and no termination)

ENV

`HTTP_PROXY`

`HTTPS_PROXY`

## Exit Codes
`0-9` - **Errors that mean an account ban / ratelimit / authentication issue:**
- `0`- Full ratelimit ban 
- `1`- Web socket auth refused
- `2`- Placing user auth error
- `4`- Login auth error

`10-19` - **Expected errors:**
- `10` - Time limit
- `11` - Keyboard interrupt 
- `12` - External time limit (cfg)
 
`20-29` - **Code / input errors:**
- `20` - No token provided
- `21` - Auth credentials not provided

`30-39` - **Misc errors, revivable:**
- `30` - Non 200 pixel placement code
- `31` - Non-error pixel placement response
- `32` - Errors related to config loading

`40-49` - **Other errors that should not be reattempted, but will result in a restart anyway:**
- `40` - Template size change *(disabled after top left corner reached)*

`69` - Successful execution and early exit, for debug purposes only.

`137` - Portainer Specific, container manually stopped via Portainer.

~~ Max attempts of 1. ~~