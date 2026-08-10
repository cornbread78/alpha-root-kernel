use bitcoin_alpha_kernel::AlphaRootKernel;
use std::fs::{self, File};
use std::io::{self, Read};

fn main() -> io::Result<()> {
    println!("Initializing Alpha Root Kernel auto-discovery synchronization engine...");
    let mut kernel = AlphaRootKernel::new("04/04/00/00");
    println!("Kernel path: {}", kernel.path);
    println!("XOR mask loaded: {:02X?}", kernel.xor_mask);

    let mut target_files = vec![];
    let paths = fs::read_dir(".")?;

    for path in paths {
        let path = path?.path();
        if path.is_file() {
            if let Some(name) = path.file_name().and_then(|n| n.to_str()) {
                if name != "Cargo.toml" && name != "Cargo.lock" && !name.starts_with('.') && !name.starts_with("target") {
                    target_files.push(name.to_string());
                }
            }
        }
    }

    if target_files.is_empty() {
        println!("No local block streams found in directory.");
        return Ok(());
    }

    for file_path in target_files {
        println!("Scanning stream file: {}...", file_path);
        let mut file = File::open(&file_path)?;
        let mut buffer = vec![0u8; 80];
        let mut count = 0;
        
        loop {
            let n = file.read(&mut buffer)?;
            if n < 80 {
                break;
            }
            
            match kernel.verify_kernel_consensus(&buffer[..n]) {
                Ok(header) => {
                    count += 1;
                    println!("Synced Header #{}: Hash = {}", count, header.block_hash());
                }
                Err(_) => {
                    // Skip non-header alignments smoothly
                }
            }
        }
        println!("Finished sync pass on {}. Total headers verified: {}", file_path, count);
    }

    Ok(())
}
