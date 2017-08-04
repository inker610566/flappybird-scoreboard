from aiohttp import web
import json
import pathlib
import json

RANK_PATH = pathlib.Path(__file__).parent/'rank.txt'

def jsonify(**kargs):
    return web.Response(body=json.dumps(kargs), content_type='application/json');

def allow_cors(func):
    async def wrapper(request):
        r = await func(request)
        r.headers.add("Access-Control-Allow-Origin", "*")
        return r
    return wrapper

@allow_cors
async def test(request):
    print(request.query['score'])
    return web.Response(text='ok')

@allow_cors
async def getScore(request):
    with RANK_PATH.open() as f:
        return jsonify(data=[
            *map(json.loads, filter(None, map(str.strip, f.readlines())))
        ])

@allow_cors
async def postScore(request):
    data = await request.post()
    if 'score' not in data or 'name' not in data:
        return web.Response(text='invalid parameter')
    with RANK_PATH.open('a') as f:
        json.dump({'name': data['name'], 'score': int(data['score'])}, f)
        f.write('\n')
    return web.Response(text='OK')

app = web.Application()

app.router.add_get('/', test)
app.router.add_get('/score', getScore)
app.router.add_post('/score', postScore)
web.run_app(app,port=8000)
