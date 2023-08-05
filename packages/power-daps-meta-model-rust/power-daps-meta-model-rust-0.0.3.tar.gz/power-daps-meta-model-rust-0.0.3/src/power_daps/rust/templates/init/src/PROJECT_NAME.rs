pub fn echo(a: i32) -> i32 {
    a
}


// This is how you write unit tests in Rust.
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_echoes() {
        assert_eq!(2, echo(2));
    }
}