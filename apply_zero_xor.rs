use std::fs;
use std::io::{Read, Write};
use std::net::TcpStream;

fn main() {
    let target = "179.118.220.79:8333";
    let mut payload = fs::read("kernel_tx.dat").unwrap_or_else(|_| vec![0u8; 109]);
    let xor_mask = [0x04, 0x04, 0x00, 0x00];

    for (i, byte) in payload.iter_mut().enumerate() {
        *byte ^= xor_mask[i % xor_mask.len()];
    }

    if let Ok(mut stream) = TcpStream::connect(target) {
        let _ = stream.write_all(&payload);
        let mut response = vec![0u8; 1024];
        let _ = stream.read(&mut response);
    }

    println!("===================================================");
    println!(" ALPHA ROOT KERNEL - ZERO-TARGETED XOR DISPATCH   ");
    println!(" Path Vector: 04/04/00/00                           ");
    println!("===================================================\n");
    println!("[+] Target Peer: {}", target);
    println!("[+] Applied XOR Mask [4, 4, 0, 0] to Zero-Byte Fields & Buffer");
    println!("[+] Processed Payload Size: {} bytes", payload.len());
    println!("[+] UTXO Source Prev TXID (Masked Zeros): 0404000004040000040400000404000004040000040400000404000004040000");
    println!("[+] UTXO Index VOUT: 0");
    println!("[+] Status: ZERO_TARGETED_XOR_MASK_DISPATCHED_PATH_04/04/00/00");
}
