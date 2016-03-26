#!/bin/bash
for i in $(ps -aux | grep python | awk '{print $2}'); do kill $i; done
