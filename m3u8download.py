from requests import get
import asyncio
from aiohttp import ClientSession
from aiofiles import open as aopen





def m3u8load(url,name):
	res=get(url,verify = False)
	with open(name,"wb") as f:
		f.write(res.content)
	print("下载完毕")


async def downloadts(url,name,session):
	for i in range(4):
		try:
			async with session.get(url) as resp:
				async with aopen(f"data/{name}.ts","wb") as f:
					await f.write(await resp.content.read())
			print(f"{name}下载完毕")
			break
		except:
			print(f"{name}下载失败")


async def load():
	n=1
	tasks=[]
	async with ClientSession() as session:
		async with aopen("ta.txt","r",encoding="utf-8") as f:
			async for line in f:
				if line.startswith('#'):
					continue
				line=line.strip()
				c=str(n).zfill(4)
				task=asyncio.create_task(downloadts(line,c,session))
				n+=1
				tasks.append(task)
			await asyncio.wait(tasks)

def main(url):
	m3u8load(url,"ta.txt")
	event_loop = asyncio.get_event_loop()
	event_loop.run_until_complete(load())
# 	asyncio.run(load())

if __name__ == '__main__':
	url=input("请输入m3u8地址：")#视频m3u8地址
	main(url)
# 	"https://sod.bunediy.com/20211220/h3b4TR73/index.m3u8"
# 	m3u8load(url,"ta.txt")
