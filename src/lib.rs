pub struct AlphaRootKernel {
    pub path_vector: &'static str,
    pub xor_mask: [u8; 4],
}

impl AlphaRootKernel {
    pub fn new(path_vector: &'static str, xor_mask: [u8; 4]) -> Self {
        Self { path_vector, xor_mask }
    }

    pub fn apply_zero_targeted_xor(&self, payload: &mut [u8]) {
        for (i, byte) in payload.iter_mut().enumerate() {
            *byte ^= self.xor_mask[i % self.xor_mask.len()];
        }
    }
}
