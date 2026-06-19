pub async fn verify_enclave_integrity(report: sev::attestation::Report) -> Result<bool, &'static str> {
    if !report.verify_signature(AMD_ARK_PUBKEY) {
        return Err("HARDWARE_FORGERY_DETECTED");
    }
    Ok(true)
}
