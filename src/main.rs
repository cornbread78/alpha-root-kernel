use std::fs;
use sha2::{Sha256, Digest};

fn main() {
    let mut payload = fs::read("kernel_tx.dat").unwrap_or_else(|_| vec![0u8; 109]);
    let xor_mask = [0x04, 0x04, 0x00, 0x00];

    for (i, byte) in payload.iter_mut().enumerate() {
        *byte ^= xor_mask[i % xor_mask.len()];
    }

    let mut hasher = Sha256::new();
    hasher.update(&payload);
    let hash = hasher.finalize();

    println!("==================================================");
    println!(" ALPHA ROOT KERNEL - XOR MASK MAINNET REPOSITORY ");
    println!(" Path Vector: 04/04/00/00                          ");
    println!("==================================================");
    println!("[+] Loaded kernel payload: {} bytes", payload.len());
    println!("[+] Applied XOR mask: [4, 4, 0, 0]");
    println!("[+] Computed Masked SHA-256 Hash: {:x}", hash);
    println!("[+] PATH VECTOR 04/04/00/00 XOR MASK REPO BUILD COMMITTED.");
}
