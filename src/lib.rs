pub struct AlphaRootKernel {
    pub path: String,
    pub consensus_active: bool,
    pub xor_mask: [u8; 4],
}

impl AlphaRootKernel {
    pub fn new(path: &str, xor_mask: [u8; 4]) -> Self {
        Self {
            path: path.to_string(),
            consensus_active: false,
            xor_mask,
        }
    }

    pub fn verify_consensus(&mut self, payload: &[u8]) -> bool {
        if payload.is_empty() {
            return false;
        }
        self.consensus_active = true;
        true
    }
}
