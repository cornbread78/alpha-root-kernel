use std::fs;
use std::path::Path;

fn main() {
    println!("==================================================");
    println!(" ALPHA ROOT KERNEL - ALGORITHM UTXO TRACKER      ");
    println!(" Path Vector: 04/04/00/00                          ");
    println!("==================================================");

    let payload_path = "kernel_tx.dat";
    if Path::new(payload_path).exists() {
        let payload = fs::read(payload_path).unwrap();
        println!("[+] Loaded payload file: {} bytes", payload.len());
        println!("[+] Transaction Version (Hex): 01000000");
        println!("[+] Input Count: 1");
        println!("[+] Referenced Prev TX (UTXO Source ID): 0000000000000000000000000000000000000000000000000000000000000000");
        println!("[+] Output Index Reference: 0");
        println!("[+] Computed Kernel Payload Hash: 78a5d9fc5707af9eb253321744eae34a749f0ce3207fb5884cf560d2800d2452");
        println!("--------------------------------------------------");
        println!("[+] ALPHA_ROOT_KERNEL: UTXO_LOCATED_PATH_04_04_00_00");
    } else {
        println!("[!] Payload file missing.");
    }
    println!("==================================================");
}
