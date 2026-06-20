use rdkafka::producer::{FutureProducer, FutureRecord};
use rdkafka::ClientConfig;
use std::time::Duration;

pub struct LedgerDecouplingPipeline {
    kafka_producer: FutureProducer,
}

impl LedgerDecouplingPipeline {
    pub fn new(brokers: &str) -> Self {
        let producer: FutureProducer = ClientConfig::new()
            .set("bootstrap.servers", brokers)
            .set("message.timeout.ms", "5000")
            .set("acks", "all")
            .create()
            .expect("Failed to create Kafka producer");
        Self { kafka_producer: producer }
    }

    pub async fn relay_to_ledger(&self, topic: &str, key: &str, payload: &[u8]) -> Result<(), String> {
        let record = FutureRecord::to(topic)
            .key(key)
            .payload(payload);

        self.kafka_producer
            .send(record, Duration::from_secs(5))
            .await
            .map_err(|(e, _)| format!("Kafka send failed: {}", e))?;
        Ok(())
    }
}
