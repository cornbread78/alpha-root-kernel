use std::fs;
use std::path::Path;
use sha2::{Sha256, Digest};
use bitcoin::transaction::Transaction;
use bitcoin::absolute::LockTime;
use bitcoin::OutPoint;
use bitcoin::TxIn;
use bitcoin::TxOut;
use bitcoin::ScriptBuf;
use bitcoin::Amount;
use bitcoin::Sequence;
use bitcoin::script::PushBytesBuf;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("==================================================");
    println!("   ALPHA ROOT KERNEL - RUST BITCOIN REPOSITORY    ");
    println!("   Path Vector: 04/04/00/00                       ");
    println!("==================================================\n");

    let payload_file = "kernel_tx.dat";
    if !Path::new(payload_file).exists() {
        fs::write(payload_file, b"ALPHA_ROOT_KERNEL_PAYLOAD_DATA_VECTOR_04_04_00_00")?;
    }

    let payload = fs::read(payload_file)?;
    println!("[+] Loaded kernel payload: {} bytes", payload.len());

    let mut hasher = Sha256::new();
    hasher.update(&payload);
    let hash_result = hasher.finalize();
    let hash_hex = format!("{:x}", hash_result);
    println!("[+] Computed SHA-256 Hash: {}", hash_hex);

    let push_payload = PushBytesBuf::try_from(payload)
        .map_err(|_| "Payload too large for Bitcoin script push limits")?;
    let op_return_script = ScriptBuf::new_op_return(push_payload);
    
    let tx = Transaction {
        version: bitcoin::transaction::Version(1),
        lock_time: LockTime::ZERO,
        input: vec![TxIn {
            previous_output: OutPoint::null(),
            script_sig: ScriptBuf::new(),
            sequence: Sequence::MAX,
            witness: bitcoin::Witness::new(),
        }],
        output: vec![TxOut {
            value: Amount::ZERO,
            script_pubkey: op_return_script,
        }],
    };

    let tx_serialized = bitcoin::consensus::serialize(&tx);
    println!("[+] Native Rust Bitcoin Transaction Serialized: {} bytes", tx_serialized.len());
    println!("[+] Serialized Hex Preview: {}...", &hex::encode(&tx_serialized)[..64]);
    println!("[+] PATH VECTOR 04/04/00/00 RUST REPO BUILD COMMITTED.");

    Ok(())
}
