#! /usr/bin/python3
# James Loye Colley
from subprocess import Popen, PIPE
from utils.read_write import default_values, write_data
from utils.sms import Alert
from utils.log import log


class Compare:
    def __init__(self, new, existing_alerts):
        self.existing = existing_alerts
        self.new = {}
        self.alerts = []
        self.new_users, self.number_users, self.load_avgs = new[:3]
        for i, j in enumerate(range(3, 35, 4)):
            pid, user, cpu, name = new[j:j+4]
            self.new['p' + str(i+1)] = {
                'pid': pid,
                'user': user,
                'cpu': float(cpu),
                'name': name
            }
        d = [v for k, v in default_values().items()]
        self.LOAD_AVG_MAX, self.CPU_LIMIT, self.USER_LIMIT = d[:3]
        self.log = log()

    @staticmethod
    def get_cmd_path(pid):
        cmd = "ps -a | grep %s" % pid
        out = Popen(cmd, stdout=PIPE, shell=True).communicate()[0].decode()
        if out:
            return ' '.join(out.split()[3:])
        return None

    def compare_users(self):
        m = "Number of users: %s\n" % self.number_users
        for user in self.existing['users']:
            if user not in self.new_users:
                m += '%s logged off\n' % user
        for new_user in self.new_users:
            if new_user not in self.existing['users']:
                m += '%s logged on\n' % new_user
        return m

    def compare(self):
        # check users
        if self.new_users != self.existing['users']:
            message = self.compare_users()
            self.existing['users'] = self.new_users[:]
            self.existing['number_of_users'] = int(self.number_users)
            self.alerts.append(message)
        # check load average stat for last 1 minute. If greater than
        # existing load average and threshold then save and alert
        new_load_avg = float(self.load_avgs[0])
        old_load_avg = self.existing['load_averages']
        if new_load_avg > old_load_avg and new_load_avg > self.LOAD_AVG_MAX:
            self.existing['load_averages'] = new_load_avg
            m = "\nNew overall MAX Load Average "
            m += "Reached:\n%s \n" % new_load_avg
            self.alerts.append(m)
        # compare the cpu percentage in each process above CPU LIMIT
        i = 1
        for process, info in self.new.items():
            if info['cpu'] > self.CPU_LIMIT:
                info['name'] = self.get_cmd_path(info['pid'])
                if not info['name'] or len(info['name'].split()) > 8:
                    continue
                if info['name'] not in self.existing['names']:
                    self.existing['names'].append(info['name'])
                    m = "\nPID: %s\n" % info['pid']
                    m += "USER: %s\n" % info['user']
                    m += "CPU: %s\n" % str(info['cpu'])
                    m += "NAME: %s\n\n" % info['name']
                    self.alerts.append(m)
            i += 1
        self.existing['iterations'] += 1
        write_data('utils/memory.json', self.existing)
        if self.alerts:
            alert = Alert(self.alerts)
            alert.read_credentials()
            alert.send_sms()
            m = "Alert sent: "
            self.log.log_info(m + ' '.join(self.alerts))
            exit(0)
        self.log.log_info("No message sent")
        exit(0)
