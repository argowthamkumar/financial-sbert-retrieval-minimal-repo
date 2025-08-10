use axum::{routing::post, Router, Json};
use serde::{Deserialize};
use reqwest::Client;

#[derive(Deserialize)]
struct Query { query: String, top_k: Option<usize> }

#[tokio::main]
async fn main() {
    let app = Router::new().route("/search", post(handle_search));
    axum::Server::bind(&"0.0.0.0:8080".parse().unwrap())
        .serve(app.into_make_service())
        .await
        .unwrap();
}

async fn handle_search(Json(payload): Json<Query>) -> Json<serde_json::Value> {
    let client = Client::new();
    let body = serde_json::json!({"query": payload.query, "top_k": payload.top_k.unwrap_or(5)});
    let resp = client.post("http://localhost:8001/similarity")
        .json(&body)
        .send()
        .await
        .unwrap()
        .json::<serde_json::Value>()
        .await
        .unwrap();
    Json(resp)
}
