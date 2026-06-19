use std::sync::atomic::{AtomicUsize, Ordering};
use std::cell::UnsafeCell;

const BUFFER_SIZE: usize = 65536;
const INDEX_MASK: usize = BUFFER_SIZE - 1;

#[repr(C, align(128))] // Upgraded from 64 to 128 for Zen 5 prefetchers
struct CachePaddedSequence {
    value: AtomicUsize,
}

#[derive(Clone)]
pub struct TransactionEvent {
    pub sequence_id: u64,
    pub customer_token: [u8; 32],
    pub encrypted_payload: [u8; 184], // Zero heap allocation
}
impl Default for TransactionEvent {
    fn default() -> Self {
        Self {
            sequence_id: 0,
            customer_token: [0; 32],
            encrypted_payload: [0; 184]
        }
    }
}

pub struct ZeroAllocationRingBuffer {
    buffer: Vec<UnsafeCell<TransactionEvent>>,
    producer_cursor: CachePaddedSequence,
    consumer_cursor: CachePaddedSequence,
}
unsafe impl Sync for ZeroAllocationRingBuffer {}

impl ZeroAllocationRingBuffer {
    pub fn new() -> Self {
        let mut buffer = Vec::with_capacity(BUFFER_SIZE);
        for _ in 0..BUFFER_SIZE {
            buffer.push(UnsafeCell::new(TransactionEvent::default()));
        }
        Self {
            buffer,
            producer_cursor: CachePaddedSequence { value: AtomicUsize::new(0) },
            consumer_cursor: CachePaddedSequence { value: AtomicUsize::new(0) },
        }
    }
}
