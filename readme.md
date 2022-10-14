1. Run to generate the keys
```
openssl ecparam -name prime256v1 -genkey -noout -out vapid_private.pem

openssl ec -in ./vapid_private.pem -outform DER|tail -c +8|head -c 32|base64|tr -d '=' |tr '/+' '_-' >> private_key.txt

openssl ec -in ./vapid_private.pem -pubout -outform DER|tail -c 65|base64|tr -d '=' |tr '/+' '_-' >> public_key.txt
```

2. Run the app

```
python main.py
```
