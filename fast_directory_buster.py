import requests, queue, threading, sys, time

host = sys.argv[1]
threads = int(sys.argv[2])
try:
    ext = sys.argv[3]
except:
    ext = False
    pass


try:
    requests.get(host)
except Exception as e:
    print(e)
    exit(0)

start = time.time()

print("[+] Scanning for directories..")

directory_list = open('wordlists/common.txt', 'r')

q = queue.Queue()

count = 0

result = f'Directory Buster results for: {host}\n\n'

with open(f"recon/{host.split('/')[2]}/directory_buster_output", 'w') as file:
    file.write(result)

def dirbuster(thread_no, q):
    global count, result
    while not q.empty():
        url = q.get()
        try:
            response = requests.get(url, allow_redirects=True, timeout=2)
            count += 1
            #print("Tried {} directories..".format(count))
            if response.status_code == 200:
                print("[+] Directory found: {}".format(str(response.url)))
                result = f'{str(response.url)}\n'
                with open(f"recon/{host.split('/')[2]}/directory_buster_output",'a') as file:
                    file.write(result)
        except:
            pass
        q.task_done()


for directory in directory_list.read().splitlines():
    if not ext:
        url = host + '/' + directory
    else:
        url = host + '/' + directory + ext
    q.put(url)


for i in range(threads):
    t = threading.Thread(target = dirbuster, args=(i,q))
    t.daemon = True
    t.start()

q.join()

print("Time taken: {}".format(time.time() - start))
