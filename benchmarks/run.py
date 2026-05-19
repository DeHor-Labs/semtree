#!/usr/bin/env python3
"""Benchmark semtree token savings on a small sample codebase.

The benchmark creates a temporary FastAPI-style project, indexes it with semtree,
then compares the token cost of sending the entire codebase versus semtree's
query-specific context output for common AI coding tasks.
"""

from __future__ import annotations

import argparse
import tempfile
import textwrap
from dataclasses import dataclass
from pathlib import Path

from semtree.config import SemtreeConfig, db_path
from semtree.context.budget import count_tokens
from semtree.context.builder import build_context
from semtree.db.schema import init_db
from semtree.indexer.coordinator import run_index
from semtree.indexer.walker import walk_project

DEFAULT_QUERIES = [
    "add JWT authentication middleware to protected API routes",
    "fix SQL injection in user search",
    "add retry with backoff to payment provider calls",
    "find where invoices are generated and emailed",
    "add structured logging around order checkout failures",
]


@dataclass
class BenchmarkRow:
    query: str
    raw_tokens: int
    semtree_tokens: int

    @property
    def saved_tokens(self) -> int:
        return self.raw_tokens - self.semtree_tokens

    @property
    def savings_percent(self) -> float:
        if self.raw_tokens == 0:
            return 0.0
        return (self.saved_tokens / self.raw_tokens) * 100


def write_sample_codebase(root: Path) -> None:
    """Create a realistic sample project with enough structure to retrieve."""
    files = {
        "app/main.py": '''
            from fastapi import FastAPI

            from app.api.orders import router as orders_router
            from app.api.users import router as users_router
            from app.core.auth import require_user

            app = FastAPI(title="Acme Store")
            app.include_router(users_router, prefix="/users", dependencies=[require_user])
            app.include_router(orders_router, prefix="/orders", dependencies=[require_user])
        ''',
        "app/api/users.py": '''
            from fastapi import APIRouter, Query

            from app.db import database

            router = APIRouter()


            @router.get("/search")
            async def search_users(q: str = Query(..., min_length=1)):
                """Search users by name or email."""
                sql = "SELECT id, email, full_name FROM users WHERE email LIKE '%" + q + "%'"
                return await database.fetch_all(sql)


            @router.get("/{user_id}")
            async def get_user(user_id: int):
                """Load a single user profile."""
                return await database.fetch_one(
                    "SELECT id, email, full_name FROM users WHERE id = $1",
                    user_id,
                )
        ''',
        "app/api/orders.py": '''
            from fastapi import APIRouter, HTTPException

            from app.services.invoices import generate_invoice_pdf, send_invoice_email
            from app.services.payments import charge_customer

            router = APIRouter()


            @router.post("/{order_id}/checkout")
            async def checkout_order(order_id: int):
                """Charge the customer, create an invoice, and send the receipt."""
                try:
                    receipt = await charge_customer(order_id)
                    invoice_path = await generate_invoice_pdf(order_id)
                    await send_invoice_email(order_id, invoice_path)
                    return {"receipt": receipt, "invoice": str(invoice_path)}
                except TimeoutError as exc:
                    raise HTTPException(status_code=502, detail="Payment provider timed out") from exc
        ''',
        "app/core/auth.py": '''
            from fastapi import Depends, HTTPException, Request


            async def require_user(request: Request):
                """Validate the bearer token and return the authenticated user."""
                token = request.headers.get("authorization", "").removeprefix("Bearer ")
                if not token:
                    raise HTTPException(status_code=401, detail="Missing token")
                return {"sub": "user_123", "scope": "orders:write"}


            def require_scope(scope: str):
                """Build a dependency that verifies a required authorization scope."""
                async def dependency(user=Depends(require_user)):
                    if scope not in user.get("scope", ""):
                        raise HTTPException(status_code=403, detail="Forbidden")
                    return user

                return dependency
        ''',
        "app/services/payments.py": '''
            import httpx


            async def charge_customer(order_id: int) -> dict:
                """Charge a customer through the external payment provider."""
                async with httpx.AsyncClient(timeout=5.0) as client:
                    response = await client.post(
                        "https://payments.example.test/charges",
                        json={"order_id": order_id},
                    )
                    response.raise_for_status()
                    return response.json()


            async def refund_payment(payment_id: str) -> dict:
                """Refund a captured payment."""
                async with httpx.AsyncClient(timeout=5.0) as client:
                    response = await client.post(
                        f"https://payments.example.test/payments/{payment_id}/refund",
                    )
                    response.raise_for_status()
                    return response.json()
        ''',
        "app/services/invoices.py": '''
            from pathlib import Path

            from app.db import database

            INVOICE_DIR = Path("var/invoices")


            async def generate_invoice_pdf(order_id: int) -> Path:
                """Render an invoice PDF for an order."""
                order = await database.fetch_one(
                    "SELECT id, total_cents, email FROM orders WHERE id = $1",
                    order_id,
                )
                target = INVOICE_DIR / f"invoice-{order['id']}.pdf"
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(b"%PDF sample invoice")
                return target


            async def send_invoice_email(order_id: int, invoice_path: Path) -> None:
                """Send the generated invoice to the customer."""
                order = await database.fetch_one(
                    "SELECT email FROM orders WHERE id = $1",
                    order_id,
                )
                print(f"email invoice {invoice_path} to {order['email']}")
        ''',
        "app/db/database.py": '''
            class Database:
                async def fetch_one(self, query: str, *args):
                    """Run a query that returns one row."""
                    return {"id": args[0] if args else 1, "email": "buyer@example.test", "total_cents": 4999}

                async def fetch_all(self, query: str, *args):
                    """Run a query that returns many rows."""
                    return []


            database = Database()
        ''',
        "README.md": '''
            # Acme Store

            Sample API used to benchmark semtree context retrieval.
        ''',
    }

    for rel_path, content in files.items():
        path = root / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(content).strip() + "\n")


def read_raw_codebase(root: Path, config: SemtreeConfig) -> str:
    """Concatenate indexable source files to simulate naive full-context usage."""
    chunks: list[str] = []
    for path in walk_project(
        root,
        include_extensions=set(config.include_extensions),
        exclude_dirs=set(config.exclude_dirs),
        max_file_size_kb=config.max_file_size_kb,
        use_gitignore=config.use_gitignore,
    ):
        rel_path = path.relative_to(root)
        chunks.append(f"### {rel_path}\n{path.read_text(errors='replace')}")
    return "\n\n".join(chunks)


def run_benchmark(root: Path, queries: list[str], token_budget: int) -> list[BenchmarkRow]:
    config = SemtreeConfig.load(root)
    stats = run_index(root, config=config, force=True)
    if stats.errors:
        joined = "\n".join(stats.errors)
        raise RuntimeError(f"Indexing failed:\n{joined}")

    raw_context = read_raw_codebase(root, config)
    raw_tokens = count_tokens(raw_context)
    conn = init_db(db_path(root))

    rows = []
    for query in queries:
        semtree_context = build_context(conn, query, token_budget=token_budget, root=root)
        rows.append(
            BenchmarkRow(
                query=query,
                raw_tokens=raw_tokens,
                semtree_tokens=count_tokens(semtree_context),
            )
        )
    return rows


def print_report(root: Path, rows: list[BenchmarkRow]) -> None:
    print("# semtree token-savings benchmark")
    print()
    print(f"Sample root: `{root}`")
    print()
    print("| Query | Raw tokens | semtree tokens | Saved | Savings |")
    print("|---|---:|---:|---:|---:|")
    for row in rows:
        print(
            f"| {row.query} | {row.raw_tokens:,} | {row.semtree_tokens:,} | "
            f"{row.saved_tokens:,} | {row.savings_percent:.1f}% |"
        )

    average = sum(row.savings_percent for row in rows) / len(rows)
    print()
    print(f"Average savings: {average:.1f}%")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Measure semtree token savings.")
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Existing codebase to benchmark. Defaults to a generated sample project.",
    )
    parser.add_argument(
        "--budget",
        type=int,
        default=1200,
        help="Token budget for each semtree context query.",
    )
    parser.add_argument(
        "--query",
        action="append",
        dest="queries",
        help="Query to benchmark. Repeat for multiple queries.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    queries = args.queries or DEFAULT_QUERIES

    if args.root is not None:
        root = args.root.resolve()
        rows = run_benchmark(root, queries, args.budget)
        print_report(root, rows)
        return

    with tempfile.TemporaryDirectory(prefix="semtree-benchmark-") as tmp:
        root = Path(tmp) / "sample-api"
        write_sample_codebase(root)
        rows = run_benchmark(root, queries, args.budget)
        print_report(root, rows)


if __name__ == "__main__":
    main()
