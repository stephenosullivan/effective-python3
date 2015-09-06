__author__ = 'stephenosullivan'

import subprocess, time, os


class item36:
    def __init__(self):
        print('-----------------\n'
              'Item 36\n'
              '-----------------\n')
        proc = subprocess.Popen(['echo', 'Hello from the child!'], stdout=subprocess.PIPE)
        out, err = proc.communicate()
        print(out.decode('utf-8'))

        proc = subprocess.Popen(['sleep', '0.3'])
        # while proc.poll() is None:
        #     print('Working...')
        print('Exit status', proc.poll())

        start = time.time()
        procs = []
        for i in range(10):
            #proc = self.run_sleep(0.1)
            proc = self.run_print(i)
            procs.append(proc)

        for proc in procs:
            proc.communicate()
        end = time.time()
        print('Finished in %.3f seconds' % (end - start))

        # Encrypt data
        procs = []
        for _ in range(3):
            data = os.urandom(10)
            proc = self.run_openssl(data)
            procs.append(proc)

        for proc in procs:
            out, err = proc.communicate()
            #print(out)
            print(out[-10:])

        # Piping
        input_procs = []
        hash_procs = []
        for _ in range(3):
            data = os.urandom(10)
            proc = self.run_openssl(data)
            input_procs.append(proc)
            hash_proc = self.run_md5(proc.stdout)
            hash_procs.append(hash_proc)

        for proc in input_procs:
            proc.communicate()
        for proc in hash_procs:
            out, err = proc.communicate()
            print(out.strip())

        # place time limit on execution
        proc = self.run_sleep(10)
        try:
            proc.communicate(timeout=0.1)
        except subprocess.TimeoutExpired:
            proc.terminate()
            proc.wait()

        print('Exit Status', proc.poll())


    def run_sleep(self, period):
        proc = subprocess.Popen(['sleep', str(period)])
        return proc

    def run_print(self, iteration):
        proc = subprocess.Popen(['echo', 'Process ' + str(iteration)])
        return proc

    def run_openssl(self, data):
        env = os.environ.copy()
        env['password'] = b'\xe24U\n\xd0Q13S\x11'
        proc = subprocess.Popen(['openssl', 'enc', '-des3', '-pass', 'env:password'],
                                env=env,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE)
        proc.stdin.write(data)
        proc.stdin.flush()
        return proc

    def run_md5(self, input_stdin):
        proc = subprocess.Popen(
            ['md5'],
            stdin=input_stdin,
            stdout=subprocess.PIPE
        )
        return proc

if __name__ == '__main__':
    sol = item36()
