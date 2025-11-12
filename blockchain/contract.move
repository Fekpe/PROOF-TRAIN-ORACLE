module ProofTrainOracle::Registry {

    use std::vector;

    struct Record has store, drop {
        dataset_hash: vector<u8>,
        quality_score: u64,
        accuracy: u64,
        price: u64,
    }

    struct Registry has key {
        records: vector<Record>,
    }

    public fun init(): Registry {
        Registry { records: vector::empty<Record>() }
    }

    public fun store_record(
        registry: &mut Registry,
        dataset_hash: vector<u8>,
        quality_score: u64,
        accuracy: u64,
        price: u64
    ) {
        let record = Record { dataset_hash, quality_score, accuracy, price };
        vector::push_back(&mut registry.records, record);
    }

    public fun get_all_records(registry: &Registry): &vector<Record> {
        &registry.records
    }
}
