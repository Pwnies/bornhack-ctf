#[macro_use]
extern crate maplit;
extern crate typed_arena;

use typed_arena::Arena;
use std::io::{self, BufRead};

use std::cell::Cell;
use std::collections::HashMap;

struct Node<'a> {
    accepting: bool,
    edges: Cell<HashMap<char, &'a Node<'a>>>,
}

impl<'a> Node<'a> {
    fn new(arena: &'a Arena<Node<'a>>, accepting: bool) -> &'a Node<'a> {
        arena.alloc(Node {
            accepting: accepting,
            edges: Cell::new(HashMap::new()),
        })
    }

    fn follow(&self, c: char) -> Option<&'a Node<'a>> {
        let edges = self.edges.replace(HashMap::new());
        let res = edges.get(&c).map(|v| *v);
        self.edges.set(edges);
        res
    }

    fn accepts(&self, s: &str) -> bool {
        let mut cur = self;
        for c in s.chars() {
            match cur.follow(c) {
                Some(node) => cur = node,
                None => return false,
            }
        }
        cur.accepting
    }

    fn edges(&self, map: HashMap<char, &'a Node<'a>>) {
        self.edges.set(map)
    }
}

// FLAG{N0_cR4Cx_pH0UNd_h3r3}

fn dfa0<'a>(arena: &'a Arena<Node<'a>>) -> &'a Node<'a> {
    let node0 = Node::new(arena, false);
    let node1 = Node::new(arena, false);
    let node2 = Node::new(arena, false);
    let node3 = Node::new(arena, false);
    let node4 = Node::new(arena, false);
    let node5 = Node::new(arena, false);
    let node6 = Node::new(arena, false);
    let node7 = Node::new(arena, false);
    let node8 = Node::new(arena, false);
    let node9 = Node::new(arena, false);
    let node10 = Node::new(arena, false);
    let node11 = Node::new(arena, false);
    let node12 = Node::new(arena, false);
    let node13 = Node::new(arena, false);
    let node14 = Node::new(arena, false);
    let node15 = Node::new(arena, false);
    let node16 = Node::new(arena, false);
    let node17 = Node::new(arena, false);
    let node18 = Node::new(arena, false);
    let node19 = Node::new(arena, false);
    let node20 = Node::new(arena, false);
    let node21 = Node::new(arena, false);
    let node22 = Node::new(arena, false);
    let node23 = Node::new(arena, false);
    let node24 = Node::new(arena, false);
    let node25 = Node::new(arena, false);
    let node26 = Node::new(arena, true);
    node0.edges(hashmap!{ 'F' => node1 });
    node1.edges(hashmap!{ 'L' => node2 });
    node2.edges(hashmap!{ 'A' => node3 });
    node3.edges(hashmap!{ 'G' => node4 });
    node4.edges(hashmap!{ '{' => node5 });
    node5.edges(hashmap!{ 'N' => node6 });
    node6.edges(hashmap!{ '0' => node7 });
    node7.edges(hashmap!{ '_' => node8 });
    node8.edges(hashmap!{ 'c' => node9 });
    node9.edges(hashmap!{ 'R' => node10 });
    node10.edges(hashmap!{ '4' => node11 });
    node11.edges(hashmap!{ 'C' => node12 });
    node12.edges(hashmap!{ 'x' => node13 });
    node13.edges(hashmap!{ '_' => node14 });
    node14.edges(hashmap!{ 'p' => node15 });
    node15.edges(hashmap!{ 'H' => node16 });
    node16.edges(hashmap!{ '0' => node17 });
    node17.edges(hashmap!{ 'U' => node18 });
    node18.edges(hashmap!{ 'N' => node19 });
    node19.edges(hashmap!{ 'd' => node20 });
    node20.edges(hashmap!{ '_' => node21 });
    node21.edges(hashmap!{ 'h' => node22 });
    node22.edges(hashmap!{ '3' => node23 });
    node23.edges(hashmap!{ 'r' => node24 });
    node24.edges(hashmap!{ '3' => node25 });
    node25.edges(hashmap!{ '}' => node26 });
    node0
}

fn main() {
    let arena = Arena::new();
    let node = dfa0(&arena);
    println!("Give me teh flag, and I'll ver1fy: ");
    let stdin = io::stdin();
    let mut stdin = stdin.lock();
    let mut s = String::new();
    stdin.read_line(&mut s).unwrap();
    if node.accepts(s.trim()) {
        println!("Correct!");
    } else {
        println!("Wrong!");
    }
}
