# Access Log Summary

There is an Apache-style access log at `/app/access.log`. Each non-empty line is
one request and begins with the client's IP address, for example:

    192.168.0.1 - - [16/Jun/2026:10:00:01 +0000] "GET /index.html HTTP/1.1" 200 1024

Analyze the log and write a JSON summary to `/app/report.json` containing exactly
these three fields:

- `total_requests` (integer): the number of requests in the log — one per
  non-empty line.
- `unique_ips` (integer): the number of distinct client IP addresses, where the
  client IP is the first whitespace-separated field on each line.
- `top_path` (string): the request path that was requested most often, taken from
  the request target in the quoted request line (e.g. `/index.html`). The provided
  log has a single most-requested path, so there is no tie to resolve.

Save the result as `/app/report.json` in valid JSON so it can be reviewed.
