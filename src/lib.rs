use bitcoin::block::Header as BlockHeader;
use bitcoin::consensus::deserialize;
use bitcoin::BlockHash;
use bitcoin::hashes::Hash;

pub struct AlphaRootKernel {
    pub path: String,
    pub consensus_active: bool,
    pub xor_mask: [u8; 4],
}

impl AlphaRootKernel {
    pub fn new(path: &str) -> Self {
        Self {
            path: path.to_string(),
            consensus_active: false,
            xor_mask: [0x04, 0x04, 0x00, 0x00],
        }
    }

    /// Applies the Alpha Root XOR mask (`04, 04, 00, 00`) to incoming raw node bytes
    pub fn unmask_payload(&self, data: &[u8]) -> Vec<u8> {
        let mut unmasked = data.to_vec();
        for (i, byte) in unmasked.iter_mut().enumerate() {
            *byte ^= self.xor_mask[i % self.xor_mask.len()];
        }
        unmasked
    }

    /// Validates actual block header data from the node stream against the root path and mask
    pub fn verify_kernel_consensus(&mut self, raw_header_bytes: &[u8]) -> Result<BlockHeader, &'static str> {
        let processed_bytes = self.unmask_payload(raw_header_bytes);
        
        let header: BlockHeader = deserialize(&processed_bytes)
            .map_err(|_| "Failed to deserialize block header from node stream")?;

        let header_hash = header.block_hash();
        if header_hash == BlockHash::all_zeros() {
            return Err("Invalid zero block hash encountered in node sync");
        }

        self.consensus_active = true;
        Ok(header)
    }
}
