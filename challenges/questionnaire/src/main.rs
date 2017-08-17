extern crate rand;
use rand::Rng;

fn main() {
    loop {
        let mut curline = String::new();
        let (question, answer) = match rand::random::<u32>() % 2 {
            0 => math_question(),
            1 => vuln_question(),
            _ => vuln_question(),
        };
        println!("{}", question);
        std::io::stdin().read_line(&mut curline).expect("read error");
        if curline.trim() != answer {
            break;
        }
    }

    println!("The quiz is over! You lost!");
}

fn math_question<'a>() -> (&'a str, &'a str) {
    let n = rand::random::<u32>() % 10;
    ("math_question", "math_answer")
}

//fn quiz_question<'a>() -> (&'a str, &'a str) {
//    let mut rng = rand::thread_rng();
//    let choices = [("Who can ROP while blindfolded?", "Kokjo")];
//    rng.choose(&choices).unwrap()
//}


fn vuln_question<'a>() -> (&'a str, &'a str) {
    ("vuln_question", "vuln_answer")
}
