import aiohttp
import sqlite3
import sys
import asyncio
import json
from . import dbstructure

SETTINGS = {
    'baseURL': 'https://db.ygorganization.com',
    'verbose': False,
}
def DEBUG(s):
    if SETTINGS['verbose']:
        print('[YGOrg DB API debug] '+str(s))

def recursive_flatten(dict, list, prefix):
    for key, value in dict.items():
        if (isinstance(value, int)):
            if key == '.':
                list.append(prefix)
            else:
                list.append(prefix + key)
        else:
            recursive_flatten(value, list, prefix+key+'/')
def flatten(dict):
    list=[]
    recursive_flatten(dict, list, '/')
    return list

async def MainLoop(queue):
    try:
        db = sqlite3.connect('ygorg-db-cache.sqlite')
        DEBUG('setting up db')
        dbstructure.setup(db)
        DEBUG('db setup done')
        
        (cacheRevision,) = db.execute('''SELECT cacheRevision FROM meta''').fetchone()
        cache = dict((key,json.loads(value)) for (key,value) in db.execute('''SELECT key,value FROM data'''))
        needManifest = True
        DEBUG('init done, cache at revision %d, we have %d items in it' % (cacheRevision,len(cache)))
        
        def TryResolveFromCache(job):
            try:
                job[2] = cache[job[0]]
                job[1].set()
                DEBUG('resolved from cache: %s' % job[0])
                return True
            except KeyError:
                DEBUG('cache miss: %s' % job[0])
                return False
        
        # takes [list of [job,event,result]], requests + resolves them, returns x-cache-revision value
        async def ResolveSingleJob(jobs):
            path = jobs[0][0]
            DEBUG('Requesting: %s' % path)
            assert(path[0] == '/')
            async with aiohttp.request(method='GET', url=(SETTINGS['baseURL']+path)) as r:
                r.raise_for_status()
                body = await r.text()
                db.execute('''INSERT INTO data (key,value) VALUES (?,?)''', (path,body))
                parsed = json.loads(body)
                cache[path] = parsed
                
                for job in jobs:
                    job[2] = parsed
                    job[1].set()
                
                return int(r.headers['X-Cache-Revision'])
        
        while True:
            if needManifest:
                DEBUG('need cache upgrade check, querying manifest of changes from rev %d to now' % cacheRevision)
                async with aiohttp.request(method='GET', url=(SETTINGS['baseURL'] + ('/manifest/%d' % cacheRevision))) as r:
                    r.raise_for_status()
                    if 0 < cacheRevision:
                        paths = flatten(json.loads(await r.text()))
                        DEBUG('evicting %d paths from cache' % len(paths))
                        for path in paths:
                            cache.pop(path,None)
                        db.executemany('''DELETE FROM data WHERE key=?''', paths)
                    else:
                        assert(len(cache) == 0)
                    cacheRevision = int(r.headers['X-Cache-Revision'])
                    db.execute('''UPDATE meta SET cacheRevision=?''', (cacheRevision,))
                    db.commit()
                    needManifest = False
                    DEBUG('cache upgrade done, now at rev %d' % cacheRevision)

            while True:
                job = await queue.get()
                if not TryResolveFromCache(job):
                    jobs = { job[0]: [job] }
                    break

            while len(jobs) < 50:
                try:
                    job = queue.get_nowait()
                    if not TryResolveFromCache(job):
                        try:
                            jobs[job[0]].append(job)
                        except KeyError:
                            jobs[job[0]] = [job]
                except asyncio.QueueEmpty:
                    break
            
            DEBUG('now handing off %d urls for querying' % len(jobs))
            topRevision = max(await asyncio.gather(*map(ResolveSingleJob,jobs.values())))
            db.commit()
            DEBUG('done querying')
            
            if cacheRevision < topRevision:
                DEBUG('need cache upgrade, saw revision %d, previous was %d' % (topRevision, cacheRevision))
                needManifest = True
    except asyncio.CancelledError:
        return
    except Exception as e:
        print('The YGOrg DB API module encountered an exception:', file=sys.stderr)
        print(e, file=sys.stderr)
        return

async def Query(url):
    try:
        queue = Query.queue
    except AttributeError:
        queue = asyncio.LifoQueue()
        Query.queue = queue
        asyncio.create_task(MainLoop(queue))

    l = [url, asyncio.Event(), None]
    queue.put_nowait(l)
    await l[1].wait()
    return l[2]
    
def GetCardData(id):
    return Query('/data/card/%d' % id)
    
def GetQAData(id):
    return Query('/data/qa/%d' % id)
