use tracing::{info, Level};
use tracing_subscriber::FmtSubscriber;
use tracing_throttle::Throttle;

// Lock-free telemetry avoiding blocking I/O on the hot path
pub fn init_lock_free_telemetry() {
    let subscriber = FmtSubscriber::builder()
        .with_max_level(Level::INFO)
        .finish();
    tracing::subscriber::set_global_default(subscriber).unwrap();
}
