#!/usr/local/bin/python

import os
import time
import collections
import subprocess

def cmdOut(cmd):
  return subprocess.check_output(cmd, shell=True).strip()

def poll():
  creating = "ContainerCreating"
  while creating.find("ContainerCreating") != -1:
    creating = cmdOut("kubectl get pods --all-namespaces")
    os.system("clear")
    print creating
    print "\nwaiting for pods to start..."
    time.sleep(2)

def o(cmd):
  print "Running: " + cmd
  os.system(cmd)
  time.sleep(2)

def k(cmd):
  o("kubectl " + cmd + " --namespace spinnaker")
  time.sleep(2)

def c(cmd):
  o("kubectl create -f " + cmd + " --namespace spinnaker")
  time.sleep(2)

o("kubectl create namespace spinnaker")

c("applications/kubedash/bundle.yaml")

c("applications/tectonic/pull.yml")
c("applications/tectonic/tectonic-console.yaml")
c("applications/tectonic/tectonic.json")

components = ('jenkins', 'registry', 'registryui', 'debweb')
for component in components:
  c("applications/" + component + "/deployment.yml")
  c("applications/" + component + "/service.json")

c("applications/kubeproxy/pod.yml")

components = ('cassandra', 'redis')
for component in components:
  c("applications/spinnaker/" + component + "/deployment.yml")
  c("applications/spinnaker/" + component + "/service.json")

poll()

os.system("kubectl create secret generic spinnaker-config --from-file=./config/echo.yml --from-file=./config/igor.yml --from-file=./config/gate.yml --from-file=./config/orca.yml --from-file=./config/rosco.yml --from-file=./config/front50.yml --from-file=./config/clouddriver.yml --namespace spinnaker")

components = ('front50', 'clouddriver', 'rosco', 'orca', 'igor', 'gate', 'deck')
for component in components:
  c("applications/spinnaker/" + component + "/controller.yml")
  c("applications/spinnaker/" + component + "/service.json")

poll()

time.sleep(2)

os.system("rm -f applications/start/services.json")

with open("applications/start/services.json", "w") as text_file:
  text_file.write(services)

os.system("kubectl create secret generic start-config --from-file=./applications/start/index.html --from-file=./applications/start/services.json --namespace spinnaker")

c("applications/start/deployment.yml")
c("applications/start/service.json")

poll()