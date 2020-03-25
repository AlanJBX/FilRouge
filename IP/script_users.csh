#!/bin/bash

python3.7 hash.py -usr admin -mdp promo2019
python3.7 hash.py -usr user -mdp usersio
mv users.txt ../Flask/users.txt
