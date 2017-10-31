#!/usr/bin/env bash
sudo wget http://download.redis.io/releases/redis-3.2.8.tar.gz
sudo tar xzf redis-3.2.8.tar.gz
cd redis-3.2.8
sudo make
sed -i -e "s/daemonize no/daemonize yes/" redis.conf
sed -i -e "s/# maxmemory <bytes>/maxmemory 500MB/" redis.conf
sed -i -e "s/# maxmemory-policy volatile-lru/maxmemory-policy allkeys-lru/" redis.conf
src/redis-server redis.conf