#!/bin/bash
echo 'Starting SA?YOJANA Sovereign Kernel...'
echo '1. Booting AMD SEV-SNP Enclave...'
./hardware_enclave/boot_enclave.sh
echo '2. Starting LMAX Event Loop...'
cargo run --release --manifest-path core_engine/Cargo.toml &
echo '3. Starting 3-Tier Inference Engine...'
python3 inference_orchestrator/src/slm_tier2_3/vllm_router.py &
echo '4. Booting Frontend...'
cd frontend && npm run dev &
wait
