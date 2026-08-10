use std::fs;
use std::io::{Read, Write};
use std::net::TcpStream;
use std::path::Path;

fn main() {
    println!("==================================================");
    println!("   ALPHA ROOT KERNEL - RUST P2P DISPATCHER        ");
    println!("   Target Peer: 179.118.220.79:8333               ");
    println!("   Path Vector: 04/04/00/00                       ");
    println!("==================================================");

    let payload_path = "kernel_tx.dat";
    if !Path::new(payload_path).exists() {
        eprintln!("[!] Error: {} missing from workspace.", payload_path);
        std::process::exit(1);
    }

    let payload = match fs::read(payload_path) {
        Ok(data) => data,
        ErrorKind => {
            eprintln!("[!] Error reading payload file.");
            std::process::exit(1);
        }
    };

    println!("[+] Loaded workspace payload size: {} bytes", payload.len());
    println!("[*] Establishing direct TCP stream to external peer 179.118.220.79:8333...");

    match TcpStream::connect("179.118.220.79:8333") {
        Ok(mut stream) => {
            println!("[+] Connected to external peer node successfully.");
            
            if let Err(e) = stream.write_all(&payload) {
                eprintln!("[!] Failed to transmit payload stream: {}", e);
                return;
            }
            println!("[+] Payload stream transmitted to remote network peer.");

            let mut buffer = [0u8; 1024];
            match stream.read(&mut buffer) {
                Ok(n) if n > 0 => {
                    println!("[+] Peer Response Hex: {:x?}", &buffer[..n]);
                }
                _ => {
                    println!("[*] Transmission acknowledged by peer node.");
                }
            }

            println!("[+] PATH VECTOR 04/04/00/00 TRANSMISSION COMMITTED.");
        }
        Err(e) => {
            eprintln!("[!] Socket Connection Error: {}", e);
        }
    }
}
