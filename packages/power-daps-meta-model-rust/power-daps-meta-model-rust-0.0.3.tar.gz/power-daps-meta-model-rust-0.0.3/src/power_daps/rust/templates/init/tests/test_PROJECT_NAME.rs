extern crate PROJECT_NAME;

// This is how you write integration tests in Rust.
#[test]
fn it_echoes() {
  assert_eq!(2, PROJECT_NAME::PROJECT_NAME::echo(2));
}