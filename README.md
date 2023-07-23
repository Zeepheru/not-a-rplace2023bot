# Yes, This is a Warcrime
misc terminal commands:

`python main.py -p [username] [password] -t [token] -am token`

`python main.py -p [username] [password] -t [token] -am token -nsp`

`python main.py -t eyJhbGciOiJSUzI1NiIsImtpZCI6IlNIQTI1NjpzS3dsMnlsV0VtMjVmcXhwTU40cWY4MXE2OWFFdWFyMnpLMUdhVGxjdWNZIiwidHlwIjoiSldUIn0.eyJzdWIiOiJ1c2VyIiwiZXhwIjoxNjkwMjA5NzI5Ljc4NzQ0LCJpYXQiOjE2OTAxMjMzMjkuNzg3NDQsImp0aSI6InlfSFk5UzEzYkd5c3dLSmV6NnZVU1pLYS1lM3FaUSIsImNpZCI6Ijl0TG9GMHNvcDVSSmdBIiwibGlkIjoidDJfbGpldW9oa3giLCJhaWQiOiJ0Ml9samV1b2hreCIsImxjYSI6MTY0OTA4OTc0Mjg3Mywic2NwIjoiZUp4a2tkR085Q0FJaGQtRmE1X2dmNVVfbTQxVk9rTldwUUhzWk41LVl5dWRKbnZWQS1kVDRmUV9ZSTFVSU1CR0JBRmlTdHliUVlBa21ET1pRZ0RNTkRwcmlTUVE0RWxxTEc4SVFCbWJrUTFaYU1jYVczd2dCS2ljRTdlVkhwYzJvYVViaTU0ZHY2cHlManlwT1VmbDNOam1MV3hQOURNYnEwMnBXTlpUbWNSMXBYUVdMX29aTzlTMzl1VXpfU2EwUjhPS3F2R0JveU1ZOF9IWldNWmlHdmZ4bnByMFpGMHdxNzNMUVdwZjZyRzc5a1dUMERLNF9SeHZ2RGFUR1hKZW1wN1JfdDMxUy1qQVBjX0w5TnFCR2F2N1hycnRXYnRfMVE1VXppalJXSno0TkJ5NWN2a2V2d1RiTmVsZjQzWmtMTDRaY2RNYmZtczZPbkp4NHRDbjhmVWJBQURfXzE4UzJGRSIsInJjaWQiOiI2OUpRVFc3aGRIajFrbFJzU1B0cThpMnRQdXRaZV9UWExhWWRKUWlRaE1VIiwiZmxvIjoyfQ.moba4LN5gpF83n1mlKxuzYZlNZZR3fQ-HOBJh-zuJKvRUsbK1ZGZPL4c-y_1_3B8w6si6pQlyoOwb2w4CuEdiNOLSDLIFbUsndtDtr5O0Xu2874Wl5gx4lV657KQxbnwgePGwrTIdKIwihq6p4Vq3-3hdFSMmiPvHjnN_BKuGZh4FhJ0cFR3RmpH0BbWTDeAi6ftAYVbzxt-6FU9-bX6ZrGi6jIjDyuiFiigu7GYKKXbsJ3Ukgha9n80TZz9fNVgOfQr9FqQG0KGO3Hk29RkeBvcVr0aQgc-Yly7NCi_4SqSC7XK75EXXRXQZ79mPrCvxMzyZlALn_dCsi16qvPHmw -am token -nsp`

``


## Portainer Commands

CMD

`-t [token] -am token`

`-t [token] -am token -dt [time]`

ENV

`HTTP_PROXY`

`HTTPS_PROXY`

## Exit Codes
`0` - **Errors that mean an account ban / ratelimit / authentication issue:**
- Full ratelimit ban 
- Web socket auth refused
- Placing user auth error
- Login auth error

`0` - **(Non-critical) Non-restart exit codes:**
- Time limit

`1-9` - **Expected errors:**
- `1` - Keyboard interrupt

`10-19` - **Code / input errors:**
- `10` - No token provided
- `11` - Auth credentials not provided

`20-29` - **Misc errors, revivable:**
- `20` - Non 200 pixel placement code
- `21` - Non-error pixel placement response

`30-39` - **Other errors that should not be reattempted, but will result in a restart anyway:**
- `30` - Template size change *(disabled after top left corner reached)*


Max attempts of **1**. 