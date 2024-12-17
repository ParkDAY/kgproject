#! /usr/bin/env bash

#ssh key 생성
sshpass -p vagrant ssh -T -o StrictHostKeyChecking=no vagrant@192.168.1.21
sshpass -p vagrant ssh -T -o StrictHostKeyChecking=no vagrant@192.168.1.22
sshpass -p vagrant ssh -T -o StrictHostKeyChecking=no vagrant@192.168.1.23