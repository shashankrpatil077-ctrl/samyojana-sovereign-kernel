use std::sync::atomic::{AtomicUsize, Ordering};
use std::cell::UnsafeCell;
use std::time::{SystemTime, UNIX_EPOCH};

const BUFFER_SIZE: usize = 65536; // Strict power of 2 for bitwise masking
const INDEX_MASK: usize = BUFFER_SIZE - 1;

#[repr(C, align(64))]
struct CachePaddedSequence {
    value: AtomicUsize,
}

#[derive(Clone, Default)]
pub struct TransactionEvent {
    pub sequence_id: u64,
    pub timestamp_ns: u64,
    pub customer_token: [u8; 32],
    pub encrypted_payload: [u8; 184], // Packed to exact 256 byte boundary
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

    pub fn try_publish(&self, mut event: TransactionEvent) -> Result<(), &'static str> {
        let current_prod = self.producer_cursor.value.load(Ordering::Relaxed);
        let current_cons = self.consumer_cursor.value.load(Ordering::Acquire);
        if current_prod.wrapping_sub(current_cons) >= BUFFER_SIZE {
            return Err("BACKPRESSURE_THRESHOLD_EXCEEDED");
        }
        let slot_index = current_prod & INDEX_MASK;
        event.sequence_id = current_prod as u64;
        unsafe { *self.buffer[slot_index].get() = event; }
        self.producer_cursor.value.store(current_prod.wrapping_add(1), Ordering::Release);
        Ok(())
    }
}
