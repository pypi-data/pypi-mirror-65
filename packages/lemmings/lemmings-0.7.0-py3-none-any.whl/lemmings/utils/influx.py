import httpx
import math

from prometheus_client.registry import REGISTRY

INF = float("inf")
MINUS_INF = float("-inf")

class Influx:
    def __init__(self, registry=REGISTRY):
        self.url = "http://localhost:8086"
        self.db = "mydb"
        self.registry = registry

    def send(self):
        r = httpx.post(f'{self.url}/write?db={self.db}', data={'key': 'value'})
    # 'cpu_load_short,host=server02 value=0.67
    # cpu_load_short,host=server02,region=us-west value=0.55
    # cpu_load_short,direction=in,host=server01,region=us-west value=2.0

    def save(self, *grep):
        output = []
        def is_filter(s):
            for f in grep:
                if f in s:
                    return True
            return False
        for metric in self.registry.collect():
            try:
                om_samples = {}
                for s in metric.samples:
                    if not is_filter(s.name):
                        continue
                    for suffix in ['_created', '_gsum', '_gcount']:
                        if s.name == metric.name + suffix:
                            om_samples.setdefault(suffix, []).append(self.sample_line(s))
                            break
                    else:
                        output.append(self.sample_line(s))
            except Exception as exception:
                exception.args = (exception.args or ('',)) + (metric,)
                raise
            for suffix, lines in sorted(om_samples.items()):
                # output.append('# TYPE {0}{1} gauge\n'.format(metric.name, suffix))
                output.extend(lines)
        return ''.join(output)

    def escape(self, v):
        return v.replace(',', r'\,').replace('=', r'\=').replace(' ', r'\ ')\
                .replace('\\', r'\\').replace('\n', r'\n').replace('"', r'\"')

    def sample_line(self, line):
        items = []
        if line.labels:
            items = ['{0}={1}'.format(k, self.escape(v)) for k, v in sorted(line.labels.items())]
        labels = ','.join(items)
        timestamp = ''
        if line.timestamp is not None:
            timestamp = ' {0:d}'.format(int(float(line.timestamp) * 1000)) # Convert to milliseconds.
        return '{0},{1} value={2} {3}\n'.format(line.name, labels, floatToGoString(line.value), timestamp)

def floatToGoString(d):
    d = float(d)
    if d == INF:
        return '+Inf'
    elif d == MINUS_INF:
        return '-Inf'
    elif math.isnan(d):
        return 'NaN'
    else:
        s = repr(d)
        dot = s.find('.')
        if d > 0 and dot > 6:
            mantissa = '{0}.{1}{2}'.format(s[0], s[1:dot], s[dot + 1:]).rstrip('0.')
            return '{0}e+0{1}'.format(mantissa, dot - 1)
        return s
