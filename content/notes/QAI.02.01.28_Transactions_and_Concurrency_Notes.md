# Transactions and concurrency

## One business action may need several database changes

Suppose Ada has **100** credits and Ben has **40**. Moving 30 credits requires two updates: subtract 30 from Ada and add 30 to Ben. A receipt should also record the transfer. If the first update succeeds but the second or receipt fails, the database must not be left with a partial transfer.

A **transaction** groups database operations into one unit with a clear **transaction boundary**: it begins, performs work, then either **commits** the whole unit or **rolls back** its uncommitted changes. Here is the intended sequence:

```sql
BEGIN IMMEDIATE;

UPDATE accounts SET balance = balance - 30 WHERE owner = 'Ada';
UPDATE accounts SET balance = balance + 30 WHERE owner = 'Ben';
INSERT INTO transfers (transfer_id, amount) VALUES ('T1', 30);

COMMIT;
```

After the commit, Ada has **70**, Ben has **70**, and the transfer receipt is `('T1', 30)`. The total remains **140**. The lab checks available balance before subtraction, stores only nonnegative balances, and uses a unique transfer ID. These are small but important parts of the business rule; a transaction by itself cannot decide whether an amount or recipient is valid.

`BEGIN IMMEDIATE` asks SQLite to start a write transaction at the beginning. It can report a busy lock immediately if another writer already has the database. A plain `BEGIN` starts a deferred transaction, which may first acquire its write access later. Both define a transaction; the choice changes *when* write contention appears. Keep the protected work short enough that other users are not waiting unnecessarily.

## ACID describes four promises to examine

| Property | Meaning in this example | What to verify |
|---|---|---|
| **Atomicity** | All three transfer changes commit together, or uncommitted changes are undone | Failed receipt insertion leaves both balances unchanged |
| **Consistency** | Stated database rules still hold at the boundary | No negative balance, positive transfer amount, unique transfer ID; application also checks available funds |
| **Isolation** | Concurrent connections do not read this transaction's unfinished changes in the lab's default setup | The other connection sees the prior committed seat count until the writer commits |
| **Durability** | A committed change is intended to persist | The lab closes and reopens the SQLite file and sees the committed balances |

These initials form **ACID**. A successful reopen demonstrates persistence across connections and process-level access, **not** a simulated power-loss test. Real crash durability depends on the database engine, journal mode, sync configuration, filesystem, and hardware. The lab uses a temporary SQLite file in WAL mode with `synchronous=FULL`, and deletes it when the run ends. That deletion is the lab's cleanup, not a database rollback.

Consistency needs a stated rule. The database's `CHECK(balance >= 0)` prevents a negative stored balance. The Python transfer function also checks that Ada has enough funds before updating. Neither check verifies a broader financial policy or an external payment system. When a workflow spans a database plus a network service, a local SQL transaction does not automatically make the entire distributed workflow atomic; plan a separate recovery or reconciliation design.

## Commit and rollback under a failure

Imagine a second transfer of 20 using the *same* receipt ID `T1`. The lab first tries both balance updates. The `INSERT` then fails because `T1` already exists. Its exception handler issues `ROLLBACK`, returning the database to Ada **70**, Ben **70**, with just the original receipt. This is a **transaction failure** with a verified all-or-none result.

```python
try:
    db.execute('BEGIN IMMEDIATE')
    # Validate funds, update both accounts, insert receipt.
    db.execute('COMMIT')
except Exception:
    if db.in_transaction:
        db.execute('ROLLBACK')
    raise
```

This pattern is an outline; the lab contains the runnable statements and bound values. Do not assume every statement error automatically rolls back all earlier statements in an open transaction. Inspect the failure and deliberately end the transaction. The code only runs `ROLLBACK` if a transaction is still active, since `BEGIN IMMEDIATE` itself can fail before a transaction starts. An insufficient-funds check is another failure path: a requested 90-credit transfer after Ada has 70 raises an error before any updates, and the transaction still ends cleanly.

After a **commit**, a later `ROLLBACK` cannot undo that already committed transaction. Corrections after commit need a new, auditable action, such as a reversal or compensating transaction. Keep the intended business boundary around all related database changes, not one statement at a time.

## Auto-commit is a different boundary

SQLite can operate in **auto-commit** mode: outside an explicit transaction, a standalone write statement forms its own transaction. The lab opens Python connections with `isolation_level=None` and uses SQL `BEGIN`, `COMMIT`, and `ROLLBACK` explicitly. In its separate settings example:

```sql
UPDATE settings SET revision = 1;  -- standalone, committed

BEGIN;
UPDATE settings SET revision = 2;
ROLLBACK;
```

Another connection sees revision **1** after the first statement, and it still sees **1** after the explicit rollback. The rollback undoes revision 2 only. If you made Ada's debit and Ben's credit as two standalone auto-committed statements, a later failure would not undo the earlier committed debit; wrap the complete transfer in one transaction.

Python's `sqlite3` has its own transaction-control settings and defaults that can differ by Python version. Do not infer the application's transaction boundary solely from one interactive SQL example. This lab sets explicit behavior so the examples are reproducible. When working with a driver, inspect whether its context manager, `commit()`, and auto-commit configuration change the boundary you intended.

## Two connections: uncommitted data and a competing writer

The lab has one `seats` row: `('workshop', 2)`. Connections A and B open the **same temporary SQLite file**. WAL mode allows B's read to proceed while A holds a write transaction in this example, but SQLite still permits only one writer at a time. The operations occur in a controlled order:

| Step | A sees | B sees or does | Stored result after step |
|---|---:|---|---:|
| Initially | 2 | 2 | 2 |
| A begins and subtracts one, without commit | 1 | Reads **2**, the prior committed value | A has an uncommitted 1 |
| B tries `BEGIN IMMEDIATE` while A writes | 1 | Gets `SQLITE_BUSY` with zero wait timeout | A's change is still uncommitted |
| A commits | 1 | A new read sees **1** | 1 |
| B starts a fresh transaction, checks 1, subtracts one, commits | 0 | 0 | 0 |

This is a **concurrent transaction** situation: two independent connections overlap, and a **lock** protects the single-writer rule. A lock is a database mechanism for coordinating access, not evidence of corruption. The failed busy attempt is a signal to back off and retry at a suitable boundary. The lab retries the **whole seat operation**, including a fresh read of availability; it does not reuse B's earlier observation of 2. If no seats remain at that fresh read, it must not subtract one.

The table also has `CHECK(available >= 0)`. After both seats have been taken, an attempted change to -1 fails and the stored count remains 0. This database constraint complements the application's availability check. For a real booking system, a single conditional `UPDATE ... WHERE available > 0` followed by a check that exactly one row changed is another useful design; use the whole reservation workflow in an appropriate transaction.

SQLite's WAL readers can see a stable earlier snapshot while a writer commits, depending on when their read transaction starts and ends. The lab's B reads are separate short statements in auto-commit mode, so its later read sees the new committed value. A long-lived read transaction might keep its earlier snapshot instead. Do not apply this exact schedule to every database engine or isolation setting; inspect the engine's semantics.

## Contention is not automatically a deadlock

A **deadlock** means two or more transactions each hold a resource the other needs, so neither can advance without intervention. A row-locking database could have A hold resource X and wait for Y while B holds Y and waits for X. Systems detect or time out the cycle and abort a participant; the application must retry safely if appropriate.

The lab's B receives `SQLITE_BUSY` because A is the current SQLite writer. That is **writer contention**, not evidence of a deadlock cycle. SQLite's single-writer model and this small schedule do not reproduce a classic two-row deadlock. To lower deadlock risk in systems that support competing row writers, access resources in a consistent order, keep transactions short, and handle an aborted transaction with a bounded retry of the full operation. A retry must not issue a duplicate external charge or duplicate receipt; use an idempotent request ID and check its outcome.

## Guided lab: predict, run, vary, repair

Download the [transactions and concurrency lab](QAI.02.01.28_Transactions_and_Concurrency_Lab.zip), unzip it, and run from its folder:

```sh
python transactions_concurrency.py
python check_transactions_concurrency.py
```

Use `python3` if needed. Each run creates and cleans up a temporary SQLite file. The first program prints:

```text
After committed transfer: [('Ada', 70), ('Ben', 70)]
After failed transfer: [('Ada', 70), ('Ben', 70)]
Transfer receipts: [('T1', 30)]
After reopen: [('Ada', 70), ('Ben', 70)]
Concurrent writer (own, other before, busy, other after, final): (1, 2, True, 1, 0)
Autocommit then rollback (visible, final): (1, 1)
Independent sold-out variation (before, busy, after, final): (1, True, 0, 0)
```

**Trace before running.** Write the balances and receipt count after each transaction boundary. Then write what A and B see before and after the seat commit. Explain why B's first attempt does not decrement a seat, and why retrying with the old observed value 2 would be wrong.

**Controlled change.** On a fresh database, call `transfer(db, 'T1', 20)` instead of 30 for the first successful transfer. Predict Ada **80**, Ben **60**, receipt `('T1', 20)`. A later attempt with duplicate `T1` must still leave those values unchanged. Restore the supplied value 30 before running the included checker; it verifies the original case.

**Reproduce and repair a failure.** In a copy of `transfer()`, remove the rollback from its exception path, then trigger the duplicate receipt after updating both balances. Observe from the same connection that the transaction remains active; another connection cannot see those uncommitted updates. Explicitly roll back before continuing. Restore the exception handler and rerun the checker. This exercise shows why application code must close failed transaction boundaries. Do this only in the temporary lab database.

## Mini-project: safe two-seat allocation

Build a small reservation operation for a workshop with two available seats. Two requests reach two connections. Each accepted request should take one seat; no request should drive availability below zero. A competing writer may need to retry after the first commits.

**Reference outline:**

```python
db.execute('BEGIN IMMEDIATE')
try:
    available = db.execute(
        "SELECT available FROM seats WHERE resource = 'workshop'"
    ).fetchone()[0]
    if available < 1:
        raise ValueError('sold out')
    db.execute(
        "UPDATE seats SET available = available - 1 WHERE resource = 'workshop'"
    )
    db.execute('COMMIT')
except Exception:
    if db.in_transaction:
        db.execute('ROLLBACK')
    raise
```

Run A first and leave it uncommitted. B's `BEGIN IMMEDIATE` fails with a zero-wait busy setting. After A commits, B starts a **new** transaction and reads 1, then takes the second seat. Final availability is **0**. The lab's `concurrency_demo()` contains the full two-connection schedule. Keep the before/after observations, final count, busy event, and rollback or retry decision. For an application, add a bounded backoff, a request ID for retries, and monitoring of busy errors and transaction duration.

**Independent variation:** start with only **one** seat, then run the same A/B schedule. Predict: A reserves it and commits 0; B initially sees 1 before A commits, but on its fresh retry reads 0 and must report sold out **without** decrementing or creating a booking. A reference check is:

```python
# In a fresh database after setup(path):
db.execute("UPDATE seats SET available=1 WHERE resource='workshop'")
# Run the A/B sequence; after A commits, B must BEGIN IMMEDIATE,
# SELECT available, see 0, and ROLLBACK without an UPDATE.
```

Expected final `SELECT available FROM seats` is `(0,)`. Do not merely change `setup()` and assume the supplied `concurrency_demo()` will return normally: its original demonstration expects B to find another seat and raises if none remains. In your variation, handle that sold-out branch as a successful refusal, not a failed database. The lab's `sold_out_variation()` is a complete runnable reference after your own attempt. It returns `(1, True, 0, 0)` for B's prior read, busy result, fresh read, and final count. Record B's fresh observation, its rollback, and the unchanged final 0.

## Operating decisions and failure handling

| Situation | Immediate response | Evidence to keep |
|---|---|---|
| Business validation fails | Roll back; tell caller the actionable reason | Request ID, validation outcome, no partial rows |
| Constraint or statement fails after earlier writes | Roll back remaining active transaction | Error type, transaction outcome, unchanged invariants |
| SQLite reports busy writer | End or abandon failed attempt; retry whole operation with bounded delay when appropriate | Busy count, wait time, retry count, final result |
| Commit result is uncertain after a connection failure | Reconnect and check a unique request/receipt ID before replaying | ID and observed committed state |
| Long locks or busy spikes | Inspect transaction duration and overlapping workload | Timings, blocked operations, journal mode |
| Durability requirement is strict | Review SQLite journal and sync settings plus storage behavior; test recovery | Configuration and recovery result |

Keep transaction scope narrow, but include every database change needed for one invariant. Use bound SQL values, handle errors explicitly, and ensure resources close. Monitoring should show successful versus rolled-back operations, busy errors, retry exhaustion, and latency. Never log sensitive balances or user details when an ID and status are enough for diagnosis. Do not issue unlimited retries; they can amplify contention.

## Check your understanding

1. Where does the successful transfer begin and end? Which changes belong inside it?
2. What are the balances and receipt count after the duplicate-ID failure?
3. Which ACID property does that rollback demonstrate most directly? Which property does reopening the file help inspect?
4. Why does B see 2 while A sees 1 before A commits?
5. Why does `SQLITE_BUSY` in this lab not prove a deadlock?
6. Why must B read the seat count again after its writer attempt fails?
7. What can a rollback undo after a standalone auto-committed revision-1 update?
8. Why is `CHECK(available >= 0)` useful even though application code reads availability?

**Answers and reasoning**

1. From `BEGIN IMMEDIATE` through `COMMIT`; debit, credit, and receipt must share the boundary.
2. Ada **70**, Ben **70**, one receipt `T1`; the second attempt rolled back both balance changes.
3. Atomicity; reopening checks that committed values remain visible, though it is not a power-loss simulation.
4. B's separate read sees committed data, while A sees its own uncommitted update.
5. Only one writer is holding the write position; no cycle of transactions waiting on each other's held resources is shown.
6. A may have consumed the seat; B must validate current availability within its new transaction.
7. It cannot undo revision 1; the explicit transaction's revision 2 is undone, leaving 1.
8. It prevents a negative stored count even if a caller makes a mistake or races through an unsafe path.

## Remember and retain

- Put all database changes for one business action inside one explicit boundary; commit success or roll back failure.
- ACID describes atomic changes, stated invariants, controlled visibility, and committed persistence. Verify each with appropriate evidence.
- Auto-commit changes the boundary to a statement when no explicit transaction is open.
- Concurrent connections can see different values before commit; a busy writer retries a *fresh operation* after checking state again.
- Keep the transfer receipt and balances, two-connection trace, busy outcome, failed-transfer rollback, and independent sold-out variation for later review.

## Further reading

- [SQLite: transactions](https://www.sqlite.org/lang_transaction.html)
- [SQLite: isolation](https://www.sqlite.org/isolation.html)
- [SQLite: write-ahead logging](https://www.sqlite.org/wal.html)
- [Python: sqlite3 transaction control](https://docs.python.org/3/library/sqlite3.html#transaction-control)
