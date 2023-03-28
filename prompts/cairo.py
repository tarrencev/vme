prefix = """
    Cairo is a new programming language for writing smart contracts for the starknet blockchain. It has similar semantics to rust but has a simpler, more limited feature set. Some important differences are:
    - Rust lifetime syntax are not supported.
    - Cairo does not support for loops. For example `for i in 0..10` is not supported.
    - Only recursion is supported. No for loops and no while loops.
    - Functional operators such as map, filter, and iter are not supported.
"""

examples = [
    {
        "snippet": """
            // Supported primitive types
            felt252, u8, u16, u32, u64, u128, u256, usize, bool
        """
    },
    {
        "snippet": """
            // Boolean operators
            true == true;
            !true == false;
            true != false;
            !(false & false);
            true & true;
            !(false | false);
            true | false;
            !(false ^ false);
            true ^ false;
        """
    },
    {
        "snippet": """
            // Arithmetic operators
            1 + 3 == 4
            3 + 6 == 9
            3 - 1 == 2
            1231 - 231 == 1000
            1 * 3 == 3
            3 * 6 == 18
            -3 == 1 - 4
        """
    },
    {
        "snippet": """
            trait Serde<T> {{
                fn serialize(ref serialized: Array<felt252>, input: T);
                fn deserialize(ref serialized: Span<felt252>) -> Option<T>;
            }}
        """
    },
    {
        "snippet": """
            // U256 Serde Implementation
            impl U256Serde of Serde::<u256> {{
                fn serialize(ref serialized: Array<felt252>, input: u256) {{
                    Serde::<u128>::serialize(ref serialized, input.low);
                    Serde::<u128>::serialize(ref serialized, input.high);
                }}
                fn deserialize(ref serialized: Span<felt252>) -> Option<u256> {{
                    Option::Some(
                        u256 {{
                            low: Serde::<u128>::deserialize(ref serialized)?,
                            high: Serde::<u128>::deserialize(ref serialized)?,
                        }}
                    )
                }}
            }}
        """
    },
    {
        "snippet": """
            trait ArrayTrait<T> {{
                fn new() -> Array<T>;
                fn append(ref self: Array<T>, value: T);
                fn pop_front(ref self: Array<T>) -> Option<T>;
                fn get(self: @Array<T>, index: usize) -> Option<Box<@T>>;
                fn at(self: @Array<T>, index: usize) -> @T;
                fn len(self: @Array<T>) -> usize;
                fn is_empty(self: @Array<T>) -> bool;
                fn span(self: @Array<T>) -> Span<T>;
            }}
        """
    },
    {
        "snippet": """
            // Calculates fib...
            fn fib(a: felt252, b: felt252, n: felt252) -> felt252 {{
                match n {{
                    0 => a,
                    _ => fib(b, a + b, n - 1),
                }}
            }}
        """
    },
    {
        "snippet": """
            use array::ArrayTrait;

            // Returns an array of size n with the values of the Fibonacci sequence, the length of the array,
            // and the value of the last element.
            fn fib(n: usize) -> (Array::<felt252>, felt252, usize) {{
                let mut arr = ArrayTrait::new();
                arr.append(1);
                arr.append(1);
                fib_inner(n, ref arr);
                let len = arr.len();
                let last = arr.at(len - 1_usize);
                return (arr, *last, len);
            }}

            fn fib_inner(n: usize, ref arr: Array::<felt252>) {{
                let length = arr.len();
                if n <= length {{
                    return ();
                }}
                arr.append(*arr.at(length - 1_usize) + *arr.at(length - 2_usize));
                fib_inner(n, ref arr)
            }}
        """
    },
    {
        "snippet": """
            // Calculates fib...
            #[derive(Copy, Drop)]
            struct FibResult {{
                value: felt252,
                index: felt252,
                nothing: ()
            }}

            fn fib(a: felt252, b: felt252, n: felt252) -> FibResult {{
                match n {{
                    0 => FibResult {{ nothing: (), value: a, index: 0 }},
                    _ => {{
                        let r = fib(b, a + b, n - 1);
                        FibResult {{ value: r.value, nothing: (), index: r.index + 1 }}
                    }},
                }}
            }}
        """
    },
    {
        "snippet": """
            // Calculates H(...H(H(0, 1), ..., n))...) where H is the Pedersen hash function.
            fn hash_chain(n: felt252) -> felt252 {{
                if n == 0 {{
                    return 0;
                }}

                pedersen(hash_chain(n - 1), n)
            }}
        """
    },
    {
        "snippet": """
            use array::ArrayTrait;

            #[derive(Drop)]
            struct MyStruct {{
                value: felt252,
                arr: Array<felt252>
            }}

            // A test that uses MyStruct above.
            #[test]
            fn main() {{
                let mut my_struct = MyStruct {{ value: 0, arr: ArrayTrait::<felt252>::new() }};
                let result = sub_three(my_struct.value);
                my_struct.value = result;
            }}

            fn sub_three(value: felt252) -> felt252 {{
                value - 3
            }}
            """
    }, {
        "snippet": """
            fn clone_loop<T, impl TClone: Clone::<T>, impl TDrop: Drop::<T>>(
                mut span: Span<T>, ref response: Array<T>
            ) {{
                match span.pop_front() {{
                    Option::Some(v) => {{
                        response.append(TClone::clone(v));
                        clone_loop(span, ref response);
                    }},
                    Option::None(_) => {{}},
                }}
            }}
        """
    }
]
