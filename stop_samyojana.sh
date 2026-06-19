#!/bin/bash
echo 'Halting SA?YOJANA Sovereign Kernel...'
pkill -f vllm_router
pkill -f core_engine
pkill -f next
