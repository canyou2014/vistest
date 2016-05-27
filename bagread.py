#!/usr/bin/env python
# -*- coding:utf-8 -*-

import rosbag
import matplotlib.pyplot as plt
x = []
y = []
z = []
f = open("rovio_result.txt", "w")
rbag = rosbag.Bag('/home/lyw/MyDocuments/result.bag')

for topic,msg,t in rbag.read_messages():
    if topic == "/rovio/odometry":

        x.append(msg.pose.pose.position.x)
        y.append(msg.pose.pose.position.y)
        z.append(msg.pose.pose.position.z)
        f.write(str(msg.header.stamp)+"\t"+str(msg.pose.pose.position.x) + "\t" + str(msg.pose.pose.position.y) + "\t" + str(msg.pose.pose.position.z) + "\n")
f.close()
rbag.close()
plt.figure(figsize=(10,10))
plt.plot(x, y)
plt.legend()
plt.show()
