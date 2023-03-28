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
            // A struct represents a component in the ecs. Its stored in a partitioned storage by its storage key. for example, (game_id, (player_id) defines an entity with player_id key in the game_id partition. Note components dont have an id field.
            #[derive(Component)]
            struct Inventory {
                weapon: u32,
                shoes: u32,
            }
        """
    },
    {
        "snippet": """
            #[system]
            mod SpawnInventorySystem {
                use array::ArrayTrait;
                use traits::Into;  
                use dojo::commands::Spawn;

                use rollyourown::components::player::Name;
                use rollyourown::components::player::Location;
                use rollyourown::components::player::Inventory;
                use rollyourown::components::player::Stats;

                fn execute(game_id: felt252, name: felt252) {
                    let player_id: felt252 = starknet::get_caller_address().into();
                    // Spawn a player into game
                    let player_game_id = commands::create((game_id, (player_id)).into(), (
                        Name { name: name },
                        Inventory { weapon: 69_u32, shoes: 1337_u32 },
                    ));

                    // Query the Game component for the game_id entity id
                    let game = commands::<Game>::get(game_id.into());
                    let player = commands::<Location, Cash>::get((game_id, (player_id)).into());

                    return ();
                }
            }
        """
    }
]


# The framework current supports a query system for querying entities by their partition and entity id. Components are selected based on the type. It also supports

# commands:: spawn((game_id, (player_id)).into(), (
#     Name {name: name},
#     Inventory {weapon: 69_u32, shoes: 1337_u32},
# ))

# for spawning new entities with a set of components.

# whats the full commands api interface to manage the ecs framework? be concise
