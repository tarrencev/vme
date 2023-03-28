examples = [
    {
        "snippet": """
            #[view]
            fn read(component: felt252, key: StorageKey, offset: u8, mut length: usize) -> Span<felt252> {
                let mut value = ArrayTrait::<felt252>::new();
                ...
                read_loop(address_domain, base, ref value, offset, length);
                value.span()
            }

            fn read_loop(
                address_domain: u32,
                base: starknet::StorageBaseAddress,
                ref value: Array<felt252>,
                offset: u8,
                length: usize
            ) {
                match gas::withdraw_gas() {
                    Option::Some(_) => {},
                    Option::None(_) => {
                        let mut data = ArrayTrait::new();
                        data.append('Out of gas');
                        panic(data);
                    },
                }

                if length.into() == offset.into() {
                    return ();
                }

                value.append(
                    starknet::storage_read_syscall(
                        address_domain, starknet::storage_address_from_base_and_offset(base, offset)
                    ).unwrap_syscall()
                );

                return read_loop(address_domain, base, ref value, offset + 1_u8, length);
            }
        """
    },
]
