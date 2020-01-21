Very simple HTTP server in python for logging and checking requests
## Usage:
```
git clone https://github.com/keedhost/json-validator.git
cd json-validator
chmod +x json-validator
./check_jsnon_valid.py [<port>]
```
By default the server starts without SSL. If you want to start https server, you shoud set variable `SECURED = True` in the script and generate the sertificates:
```
sed -i 's/SECURED\ =\ False/SECURED\ =\ True/g' check_jsnon_valid.py
openssl req -x509 -newkey rsa:2048 -keyout ./cert/key.pem -out ./cert/cert.pem -days 365
```
**Warning:** you should enter correct CN while the certs generating. So, you also can enter IP as CN.

### Example:

Start server on the port `5000` on the Linux system with IP 172.24.201.82:
```
./check_jsnon_valid.py 5000
```
Send JSON data from the client and start JSON validation.
For correct JSON:
```
curl -s -d '{"key1":"value1", "key2":"value2"}' -H "Content-Type: application/json" -X POST -k http://172.24.201.82:5000 -v
```
For invalid JSON:
```
$ curl -s -d "{'age':100 }" -H "Content-Type: application/json" -X POST -k http://172.24.201.82:5000 -v
```
