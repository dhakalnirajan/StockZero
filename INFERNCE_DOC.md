# StockZero RL Chess Engine - Inference Documentation

This document provides guidelines for production-grade inference with the StockZero RL chess engine, focusing on performance, scalability, and reliability in a web application context.

## 1. Optimized Inference Engine (`inference/inference_engine.py`)

The `inference/inference_engine.py` module provides the `get_optimized_ai_move` function, engineered for speed and efficiency in production.

* **`get_optimized_ai_move(board_fen, num_simulations=100, use_cache=True)` Function (Production Ready):**
  * **Caching (Redis):** Implements a critical performance optimization using Redis for caching AI move results based on board FEN strings. This dramatically reduces latency for repeated positions and significantly decreases server load. Ensure Redis is properly configured and running in your production environment.
  * **GPU Acceleration (CUDA):**  Leverages GPU acceleration for neural network inference using `tf.device('/GPU:0'...)` for maximum speed if a CUDA-enabled GPU is available. Ensure TensorFlow and CUDA are correctly set up on your production servers with GPUs.
  * **`num_simulations` Parameter:** Allows dynamic adjustment of MCTS `num_simulations` to fine-tune the trade-off between AI move strength and inference latency in production. You can monitor server load and adjust this parameter accordingly.
  * **`use_cache` Parameter:** Provides control over whether to use Redis caching (enabled by default). You might disable caching for specific testing scenarios or if you implement more advanced cache invalidation strategies.
  * **Robust Error Handling and Logging (Implicit):**  Incorporate robust error handling and logging within the engine code (especially in `MCTSNode.evaluate`, `run_mcts`, and `choose_best_move_from_mcts`) to gracefully handle potential exceptions during inference and aid in debugging production issues. (This is implied - you need to ensure your engine code has adequate error handling).

## 2. Production Inference Pipeline

1. **Pre-load Model at Startup (`engine/__init__.py`):**  The StockZero engine and trained `PolicyValueNetwork` model are loaded only once when the Django application starts up (in `engine/__init__.py`). This avoids model loading overhead for every API request, significantly improving performance.

2. **REST API Endpoint (`webapp/chessgame/views.py`):** The `make_move_api` Django REST Framework view in `webapp/chessgame/views.py` uses `get_optimized_ai_move` to efficiently retrieve AI moves in response to user requests via the API endpoint `/api/chess/make_move/`.

3. **JSON Communication (RESTful API):** The API uses JSON for requests and responses, ensuring efficient and standardized data exchange between the frontend and backend.

4. **Rate Limiting (API Throttling):** Django REST Framework's throttling classes (`AnonRateThrottle`, `UserRateThrottle` in `settings.py` and `webapp/chessgame/views.py`) are implemented to protect the API from abuse and ensure fair resource usage by limiting the number of requests from anonymous and authenticated users. Adjust throttle rates based on your expected traffic and server capacity.

5. **Logging (Production Monitoring):** Comprehensive logging is implemented within the Django web application and the engine code (to `engine.log` and `webapp.log` files). Monitor these logs in production to track performance, identify errors, and analyze user behavior.

6. **GPU Utilization (CUDA):** Ensure your production servers utilize CUDA-enabled NVIDIA GPUs and TensorFlow is configured to use them.  `get_optimized_ai_move` automatically leverages GPUs for faster inference if available.  Monitor GPU utilization to verify that your GPU resources are being effectively used under load.

7. **Caching Strategy (Redis):**
    * **Persistent Redis:** Use a persistent Redis server for production caching to ensure cache data survives server restarts. Configure Redis persistence settings (RDB or AOF).
    * **Cache Size and Eviction:** Monitor Redis memory usage and configure appropriate cache eviction policies (LRU, etc.) to manage cache size and ensure that frequently accessed, valuable positions are retained in the cache while less used entries are evicted to make room.
    * **Cache Invalidation (Advanced):**  For more sophisticated caching strategies, you might consider implementing cache invalidation mechanisms if your AI engine or evaluation function is updated over time. However, for a chess engine with a fixed trained model, basic time-based expiry caching is often sufficient.

## 3. API Usage (REST API Endpoint - Production Context)

The REST API endpoint `/api/chess/make_move/` (POST) is the primary entry point for inference in a production context.

* **Request Format (JSON):**  Same as documented in `INFERENCE_DOC.md`, but in a production setting, ensure you are sending valid JSON requests from your frontend and handling responses correctly.

* **Response Format (JSON):** Same as documented in `INFERENCE_DOC.md`.  Handle all possible response fields (`ai_move`, `next_fen`, `game_over`, `result`, `error`) robustly in your frontend JavaScript to provide a smooth and informative user experience.

* **Rate Limits:** Be aware of the rate limits you have configured in `settings.py` and `webapp/chessgame/views.py`.  Design your frontend JavaScript to respect these rate limits to avoid being throttled or blocked by the server, especially under high usage scenarios.  Implement appropriate delays or request queuing mechanisms in the frontend if needed.

* **Error Handling:** Implement comprehensive error handling in both the frontend and backend. Gracefully handle API errors (HTTP status codes, `error` field in JSON responses) and provide informative error messages to the user in the frontend. Log errors on the server-side for debugging and monitoring.

* **Security:** Ensure HTTPS is enabled for all communication between the frontend and backend to protect user data and API requests/responses in transit. Follow other security best practices for your Django web application as outlined in `DEPLOYMENT_DOC.md`.

## 4. Monitoring and Performance Tuning

* **Server Monitoring:** Monitor server CPU, RAM, GPU utilization, network traffic, and disk I/O to assess server load and identify potential bottlenecks during production usage.
* **API Response Time Monitoring:** Track API response times (especially for `/api/chess/make_move/`). Monitor average response times, percentiles (p50, p90, p99), and identify slow requests or periods of high latency. Tools like Django Debug Toolbar (for development/testing) or production-grade monitoring tools (Prometheus, Grafana, New Relic, etc.) can be helpful.
* **Cache Hit Rate Monitoring (Redis):** Monitor Redis cache hit rates to assess the effectiveness of caching. Low cache hit rates might indicate that caching is not as effective as expected or that your cache size is too small for your typical workload.
* **Log Analysis:** Regularly analyze your application logs (`engine.log`, `webapp.log`) to identify errors, performance issues, security events, and user behavior patterns. Log aggregation and analysis tools (ELK stack, Graylog) can be invaluable for production log management at scale.
* **Performance Tuning Iteration:** Based on monitoring data and performance analysis, iterate on your StockZero engine and web application to further optimize performance. Consider:
  * Adjusting `num_simulations` in `get_optimized_ai_move` to fine-tune strength vs. speed trade-off.
  * Optimizing neural network architecture (if needed, for a faster but potentially slightly weaker model).
  * Improving MCTS implementation efficiency (if performance bottlenecks are found in search).
  * Optimizing database queries (if database performance becomes a bottleneck for PGN logging or other operations).
  * Scaling horizontally by deploying multiple StockZero application instances behind a load balancer to handle increased traffic.
  * Implementing more advanced caching strategies or using more powerful caching infrastructure.

This production-grade inference documentation provides guidelines for building a robust, scalable, and high-performance StockZero chess engine web application capable of handling real-world user traffic. Remember to continuously monitor, tune, and optimize your deployment to maintain responsiveness and reliability under production conditions.
