import jpype
import json
import os
import re
import sys
from jpype import java
from jpype import javax


class JmxMetric(object):
    def __init__(self, host=None, port=None):
        jvmpath = jpype.getDefaultJVMPath()
        if not jpype.isJVMStarted():
            jpype.startJVM(jvmpath)
        #if not jpype.isThreadAttachedToJVM():
        #    jpype.attachThreadToJVM()
        self.mbeanConnection = self._mbean_connection(host, port)

    def _mbean_connection(self, host, port):
        self.jmxurl = javax.management.remote.JMXServiceURL('service:jmx:rmi:///jndi/rmi://%s:%d/jmxrmi' % (host, port))
        self.jhash = java.util.HashMap()
        self.jarray = jpype.JArray(java.lang.String)([])
        self.jhash.put(javax.management.remote.JMXConnector.CREDENTIALS, self.jarray)
        self.jmxsoc = javax.management.remote.JMXConnectorFactory.connect(self.jmxurl, self.jhash)
        return self.jmxsoc.getMBeanServerConnection()

    def fetchAttr(self, rawName, attrName):
        name = javax.management.ObjectName(rawName)
        return self.mbeanConnection.getAttribute(name, attrName).value

    def get_jmx_metrics(self):
        jmx_metrics = {}

        targets_file = os.environ["JMX_TARGETS"]
        if not targets_file:
            sys.stderr.write("No JMX targets file specified.\n")
            return

        with open(targets_file, "r") as f:
            target = json.loads(f.read())
            for t in target:
                for qry, metrics in t.items():
                    for metric in metrics:
                        for m in metric['metrics']:
                            attribute = metric['attributes']
                            obj = qry+",name="+m
                            metric_name = re.sub('[^A-Za-z0-9]+', '', m)
                            metric_value = self.fetchAttr(obj, attribute)
                            jmx_metrics[metric_name] = metric_value
        self.jmxsoc.close()
        return jmx_metrics
