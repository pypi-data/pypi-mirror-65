if [[! $@]]; then 
    python3 -m chimera_cli -h
else
    python3 -m chimera_cli $@