import hashlib
import os

from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_request

EMAIL = "24f1002528@ds.study.iitm.ac.in"

mcp = FastMCP("Exam Challenge Server")


@mcp.tool()
def solve_challenge() -> str:
    """Return the challenge-specific SHA-256 result."""

    request = get_http_request()
    challenge = request.headers.get("X-Exam-Challenge")

    if not challenge:
        raise ValueError("Missing X-Exam-Challenge header")

    message = f"{challenge}:{EMAIL.strip().lower()}"
    digest = hashlib.sha256(message.encode("utf-8")).hexdigest()

    return digest[:16]


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    mcp.run(transport="http", host="0.0.0.0", port=port)