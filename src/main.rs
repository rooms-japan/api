#![feature(plugin)]
#![plugin(rocket_codegen)]

extern crate postgres;
extern crate rocket;
use rocket::http::RawStr;


#[get("/")]
fn index() -> &'static str {
    "Hello world"
}

#[get("/test")]
fn test() -> &'static str {
    "This is a test :)"
}

#[get("/hello/<name>")]
fn hello(name: &RawStr) -> String {
    format!("Hi {}", name.as_str())
}

fn main() {
    rocket::ignite().mount("/", routes![index, test, hello]).launch();
}
