import multiprocessing
import subprocess
import cx_Oracle


def pinger(job_q, results_q, badresults_q):
    y = "ping -c 1 "
    while True:
        ip = job_q.get()
        if ip is None:
            break

        try:
            subprocess.check_output(str(y) + ip)
            results_q.put(ip)

        except:
            badresults_q.put(ip)


if __name__ == '__main__':
    ipaddress =[]
    jobs = multiprocessing.Queue()
    results = multiprocessing.Queue()
    badresults = multiprocessing.Queue()
    con = cx_Oracle.connect('///')
    cur = con.cursor()
    cur.execute("Select IP from IP_CHECK_TAB  Order By Ip")
    output = {}
    for a in cur:
        ipaddress.append(a[0])
    pool_size = len(ipaddress) - 1
    pool = [multiprocessing.Process(target=pinger, args=(jobs, results, badresults))
             for i in range(pool_size)]
    for p in pool:
        p.start()
    for i in ipaddress:
        jobs.put(i)
    for p in pool:
        jobs.put(None)
    for p in pool:
        p.join()
    while not results.empty():
        ip = results.get()
        print(ip + " : Connected")
        cur.execute("Update IP_CHECK_TAB SET STATUS='ok',STATUS_INFO = sysdate Where IP = '" + ip + "'")
        output[ip] = "host appears to be up"
    while not badresults.empty():
        ip = badresults.get()
        print(ip + " : Not connected")
        cur.execute("Update IP_CHECK_TAB SET STATUS='nok',STATUS_INFO = sysdate Where IP = '" + ip + "'")
        output[ip] = "host is not connected"
    con.commit()
    cur.close()
    con.close()
