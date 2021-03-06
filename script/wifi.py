from subprocess import Popen, PIPE
from base64 import b64encode
import sys
import re
import time


class Windows():
    LINESEP = "\r\n"
    _RE_ERR = re.compile(r"Error\"\>(.+?)\<\/S\>")

    def _parse_err(self, xml_err):
        return self.LINESEP.join(self._RE_ERR.findall(xml_err))

    def _handle_command(self, stdout, stderr, rtcode, raise_stderr):
        if rtcode and stderr:
            error = OSError(rtcode, "on (%s)" % self._parse_err(stderr))
            if raise_stderr:
                raise error
            else:
                print(error, "DEBUG")
                return stdout
        else:
            return stdout

    def execute_command(self, command, raise_stderr=True, shell=False):
        ps = b64encode(command.replace("\n", "").encode('utf_16_le')).decode('ascii')
        proc = Popen('powershell -encodedCommand %s ' % ps,
                     stdout=PIPE, stderr=PIPE, shell=shell, universal_newlines=True)
        stdout, stderr = proc.communicate("`r`n")
        rtcode = proc.returncode
        return self._handle_command(stdout, stderr, rtcode, raise_stderr)

    def enable_wifi(self, iface_name):
        conn_status = self.check_connection(iface_name)
        if conn_status:
            print(f"{iface_name} already enabled")
        else:
            print(f"Enable '{iface_name}'...")
            cmd = f"Enable-NetAdapter -Name '{iface_name}'-Confirm:$false -AsJob | Wait-Job"
            self.execute_command(cmd)
            wait = 0
            while wait < 30:
                wait += 2
                time.sleep(2)
                if self.check_connection(iface_name):
                    print(f"Network '{iface_name}' enable successfully")
                    break
            else:
                print(f"Network '{iface_name}' enable fail")

    def disable_wifi(self, iface_name):
        conn_status = self.check_connection(iface_name)
        if conn_status:
            print(f"Disable '{iface_name}'...")
            cmd = f"Disable-NetAdapter -Name '{iface_name}'-Confirm:$false -AsJob | Wait-Job"
            self.execute_command(cmd)
            wait = 0
            while wait < 30:
                wait += 2
                time.sleep(2)
                if not self.check_connection(iface_name):
                    print(f"Network '{iface_name}' disable successfully")
                    break
            else:
                print(f"Network '{iface_name}' disable fail")
        else:
            print(f"{iface_name} already disabled")

    def check_connection(self, iface_name):
        cmd = f"(Get-NetAdapter -Name '{iface_name}').Status"
        status = self.execute_command(cmd).strip()
        print(f"{iface_name} connection is {status}")
        enables = ['up', "connected"]
        if status.lower() in enables:
            return True
        else:
            return False


if __name__ == '__main__':
    os = Windows()
    try:
        arg = sys.argv[1]
    except IndexError:
        arg = ''

    if arg == 'disable':
        os.disable_wifi('wi-fi')
    elif arg == 'enable':
        os.enable_wifi('wi-fi')
    else:
        os.check_connection('wi-fi')
        print("please use 'enable' to enable wifi")
        print("please use 'disable' to disable wifi")
