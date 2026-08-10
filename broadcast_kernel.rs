use std::fs;
use std::io::{Read, Write};
use std::net::TcpStream;
use std::path::Path;

fn encode_hex(bytes: &[u8]) -> String {
    let hex_chars = b"0123456789abcdef";
    let mut s = String::with_capacity(bytes.len() * 2);
    for &b in bytes {
        s.push(hex_chars[(b >> 4) as usize] as char);
        s.push(hex_chars[(b & 0x0f) as usize] as char);
    }
    s
}

fn encode_base64(input: &[u8]) -> String {
    const TABLE: &[u8] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    let mut result = String::new();
    let mut i = 0;
    while i < input.len() {
        let b0 = input[i];
        let b1 = if i + 1 < input.len() { input[i + 1] } else { 0 };
        let b2 = if i + 2 < input.len() { input[i + 2] } else { 0 };

        let triplet = ((b0 as u32) << 16) + ((b1 as u32) << 8) + (b2 as u32);

        result.push(TABLE[((triplet >> 18) & 0x3F) as usize] as char);
        result.push(TABLE[((triplet >> 12) & 0x3F) as usize] as char);
        if i + 1 < input.len() {
            result.push(TABLE[((triplet >> 6) & 0x3F) as usize] as char);
        } else {
            result.push('=');
        }
        if i + 2 < input.len() {
            result.push(TABLE[(triplet & 0x3F) as usize] as char);
        } else {
            result.push('=');
        }
        i += 3;
    }
    result
}

fn get_credentials() -> String {
    let home = std::env::var("HOME").unwrap_or_else(|_| "/data/data/com.termux/files/home".to_string());
    let cookie_path = format!("{}/.bitcoin/.cookie", home);
    
    if Path::new(&cookie_path).exists() {
        if let Ok(content) = fs::read_to_string(&cookie_path) {
            let content = content.trim();
            println!("[+] Found active Bitcoin Core cookie at {}", cookie_path);
            if content.contains(':') {
                return content.to_string();
            } else {
                return format!("__cookie__:{}", content);
            }
        }
    }
    
    let conf_path = format!("{}/.bitcoin/bitcoin.conf", home);
    let mut user = "Cornbread78".to_string();
    let mut pass = "26a78aea33835e4d74654ce25e3e8b51a0706d8e55353f92b98c73f7ec33f416".to_string();
    
    if Path::new(&conf_path).exists() {
        if let Ok(content) = fs::read_to_string(&conf_path) {
            for line in content.lines() {
                let line = line.trim();
                if line.starts_with("rpcuser=") {
                    user = line.split('=').nth(1).unwrap_or("").trim().to_string();
                } else if line.starts_with("rpcpassword=") {
                    pass = line.split('=').nth(1).unwrap_or("").trim().to_string();
                }
            }
        }
    }
    format!("{}:{}", user, pass)
}

fn main() {
    println!("==================================================");
    println!("   ALPHA ROOT KERNEL - RUST RPC DISPATCHER        ");
    println!("   Path Vector: 04/04/00/00                      ");
    println!("==================================================");

    let payload_file = "kernel_tx.dat";
    if !Path::new(payload_file).exists() {
        eprintln!("[!] Error: {} missing from workspace.", payload_file);
        std::process::exit(1);
    }

    let payload = fs::read(payload_file).expect("Failed to read payload file");
    let tx_hex = encode_hex(&payload);
    println!("[+] Loaded payload size: {} bytes", payload.len());
    println!("[+] Serialized Hex Preview: {}...", &tx_hex[..32.min(tx_hex.len())]);

    let credentials = get_credentials();
    let auth_encoded = encode_base64(credentials.as_bytes());

    let rpc_payload = format!(
        r#"{{"jsonrpc":"1.0","id":"alpha_rust_broadcast","method":"sendrawtransaction","params":["{}"]}}"#,
        tx_hex
    );

    let host = "127.0.0.1";
    let port = 8332;
    let path = "/";

    let http_request = format!(
        "POST {} HTTP/1.1\r\n\
        Host: {}:{}\r\n\
        Authorization: Basic {}\r\n\
        Content-Type: application/json\r\n\
        Content-Length: {}\r\n\
        Connection: close\r\n\
        \r\n\
        {}",
        path, host, port, auth_encoded, rpc_payload.len(), rpc_payload
    );

    println!("[*] Connecting to node daemon at {}:{}...", host, port);
    let mut stream = match TcpStream::connect((host, port)) {
        Ok(s) => s,
        Err(e) => {
            eprintln!("[!] Connection failed: {}", e);
            return;
        }
    };

    stream.write_all(http_request.as_bytes()).expect("Failed to send request");
    
    let mut response = String::new();
    stream.read_to_string(&mut response).expect("Failed to read response");

    println!("[+] Node Daemon Response Received:");
    println!("{}", response);
}
