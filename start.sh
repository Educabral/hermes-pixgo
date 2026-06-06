#!/bin/bash
echo "Iniciando o T-800 na Nuvem..."

# Inicia a gambiarra do servidor falso em background
python3 /opt/keep_alive.py &

# Inicia o motor principal do Hermes
exec hermes gateway run
