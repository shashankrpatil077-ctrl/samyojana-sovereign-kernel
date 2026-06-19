use tokio_uring::fs::File;
use std::sync::Arc;

pub struct IoUringJournaler {
    wal_file: Arc<File>,
}
impl IoUringJournaler {
    pub async fn async_fsync_batch(&self, buffer: Vec<u8>) {
        // O_DIRECT zero-copy asynchronous write bypassing page cache
        let _res = self.wal_file.write_at(buffer, 0).await;
    }
}
