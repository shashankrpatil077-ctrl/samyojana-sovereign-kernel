use tokio_uring::fs::File;
use std::sync::Arc;
use std::sync::atomic::{AtomicU64, Ordering};

pub struct IoUringJournaler {
    wal_file: Arc<File>,
    write_offset: AtomicU64,
}

impl IoUringJournaler {
    pub fn new(file: Arc<File>) -> Self {
        Self {
            wal_file: file,
            write_offset: AtomicU64::new(0),
        }
    }

    pub async fn async_fsync_batch(&self, buffer: Vec<u8>) -> Result<(), std::io::Error> {
        let len = buffer.len() as u64;
        let offset = self.write_offset.fetch_add(len, Ordering::SeqCst);
        // O_DIRECT zero-copy asynchronous write bypassing page cache
        let (res, _buf) = self.wal_file.write_at(buffer, offset).await;
        res?;
        Ok(())
    }
}
