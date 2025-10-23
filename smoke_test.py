import json, urllib.request, urllib.error, urllib.parse, sys
BASE='http://127.0.0.1:8000'

def post(path, data, token=None):
    url = BASE+path
    b = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=b, headers={'Content-Type':'application/json'})
    if token: req.add_header('Authorization','Bearer '+token)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.getcode(), json.load(resp)
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.load(e)
        except:
            return e.code, {'error': e.reason}
    except Exception as e:
        return None, {'error': str(e)}

print('1) Register...')
code, data = post('/api/register', {'nome':'TesteUser','email':'teste@example.com','senha':'senha123','dataNascimento':'2000-01-01'})
print(code, data)
if code and code>=200 and code<300:
    token = data.get('token')
else:
    # try login in case already exists
    code, data = post('/api/login', {'email':'teste@example.com','senha':'senha123'})
    print('login fallback', code, data)
    token = data.get('token') if data and isinstance(data, dict) else None

print('\n2) If have token, GET /api/profile')
if token:
    import urllib.request
    req=urllib.request.Request(BASE+'/api/profile')
    req.add_header('Authorization','Bearer '+token)
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            print(r.getcode(), json.load(r))
    except Exception as e:
        print('profile error', e)
else:
    print('no token, skipping profile')

print('\n3) Post a comment (requires token)')
if token:
    code,data = post('/api/comments', {'book_title':'A Culpa é das Estrelas','comment':'Ótimo livro','rating':5}, token=token)
    print(code,data)
else:
    print('no token, skipping comment')
