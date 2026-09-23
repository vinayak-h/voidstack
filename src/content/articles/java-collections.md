---
title: 'Java Collections Beyond the Basics'
description: 'A starting point for understanding collection choices, trade-offs, and internal behavior.'
category: 'JAVA'
tags: ['java', 'collections', 'data-structures']
publishedDate: '2026-09-22'
---

# Choosing a collection

The right Java collection depends on access patterns. An `ArrayList` is useful for indexed access, a `HashSet` enforces uniqueness, and a `HashMap` associates keys with values.

Most bugs and performance problems involving collections come from the same root cause: picking a structure based on habit instead of the actual access pattern the code needs. This article walks through the main collection families, their trade-offs, and the details that matter once an application moves past toy examples.

We will use a simple **order processing system** as a running example: orders have line items, customers have order history, and a dashboard needs to summarize totals per product.

## Questions to ask before choosing

- Do I need ordering, and if so, insertion order or sorted order?
- Do I need to reject duplicate values?
- Is lookup more important than insertion speed, or the reverse?
- Will multiple threads read and write the collection at the same time?
- How large will the collection realistically grow?

Collection choice should follow the behavior your application needs, not habit.

## 1. The `List` family

A `List` is an ordered, index-accessible sequence that allows duplicates.

### `ArrayList`

`ArrayList` is backed by a resizable array. Reading by index is O(1) because the array supports direct offset access. Inserting or removing from the middle is O(n) because the remaining elements must shift.

```java
List<OrderItem> items = new ArrayList<>();
items.add(new OrderItem("SKU-1", 2));
items.add(new OrderItem("SKU-2", 1));

OrderItem first = items.get(0); // O(1)
items.remove(0);                // O(n) - shifts every remaining element
```

Use `ArrayList` when the collection is mostly read, appended to at the end, or iterated in order.

### `LinkedList`

`LinkedList` is a doubly linked list. Inserting or removing at a known node is O(1), but there is no direct index access, so `get(index)` is O(n) because it walks the list.

In practice, `ArrayList` outperforms `LinkedList` for most workloads because of CPU cache locality, even for insertions. Reach for `LinkedList` only when you need the `Deque` behavior described below and don't need random access.

### `CopyOnWriteArrayList`

For lists that are read far more often than written, and need thread safety without external locking, `CopyOnWriteArrayList` copies the underlying array on every mutation. Reads never block, but writes become expensive as the list grows. This fits small, rarely updated lists such as a list of registered event listeners.

## 2. The `Set` family

A `Set` rejects duplicates, and the specific implementation determines ordering and performance.

| Implementation | Ordering | Lookup | Notes |
| --- | --- | --- | --- |
| `HashSet` | None | O(1) average | Backed by a `HashMap`; fastest general-purpose set |
| `LinkedHashSet` | Insertion order | O(1) average | Slight overhead to maintain a linked list of entries |
| `TreeSet` | Sorted | O(log n) | Requires elements to be `Comparable` or a `Comparator` |

```java
Set<String> uniqueSkus = new HashSet<>();
uniqueSkus.add("SKU-1");
uniqueSkus.add("SKU-1"); // ignored, set already contains it

Set<String> sortedSkus = new TreeSet<>(uniqueSkus);
```

A `HashSet` relies on `hashCode()` and `equals()` being implemented consistently. If a mutable object is stored in a `HashSet` and its fields used in `hashCode()` change after insertion, the set can silently lose the ability to find that element again. Prefer immutable keys, or values whose identity fields never change after being added.

## 3. The `Map` family

A `Map` associates keys with values. The same trade-offs as `Set` apply, since `HashSet` and `TreeSet` are implemented on top of `HashMap` and `TreeMap`.

```java
Map<String, Integer> productTotals = new HashMap<>();
productTotals.merge("SKU-1", 2, Integer::sum);
productTotals.merge("SKU-1", 3, Integer::sum);
// productTotals.get("SKU-1") == 5
```

`merge` is a useful pattern for running totals: it inserts the value if the key is absent, or combines it with the existing value using the given function if the key is present.

### `HashMap` internals, briefly

A `HashMap` stores entries in buckets determined by the hash of the key. Since Java 8, buckets that grow too large (due to hash collisions) are converted from a linked list to a balanced tree, which keeps worst-case lookup at O(log n) instead of degrading to O(n). This mainly matters when an attacker can control input to force collisions, or when a poor `hashCode()` implementation clusters everything into a few buckets.

### `LinkedHashMap` for simple caches

`LinkedHashMap` maintains insertion order by default, but it can also be configured for access order, which makes it a convenient basis for a least-recently-used cache:

```java
Map<String, Order> cache = new LinkedHashMap<>(16, 0.75f, true) {
    protected boolean removeEldestEntry(Map.Entry<String, Order> eldest) {
        return size() > 100; // evict the least recently accessed entry
    }
};
```

### `TreeMap` for ordered data

`TreeMap` keeps keys sorted and supports range queries such as "all orders placed after a given date" through `headMap`, `tailMap`, and `subMap`. This is useful when the data naturally needs a sorted view, such as a time-ordered ledger, rather than sorting a `HashMap` every time it is read.

## 4. Queues and deques

A `Queue` models first-in-first-out processing; a `Deque` supports adding and removing from both ends and can act as a stack or a queue.

```java
Deque<Order> pendingOrders = new ArrayDeque<>();
pendingOrders.addLast(new Order("A-1001"));
pendingOrders.addLast(new Order("A-1002"));

Order next = pendingOrders.pollFirst(); // process oldest order first
```

`ArrayDeque` is generally preferred over `LinkedList` for both stack and queue use cases because it avoids the per-node allocation overhead of a linked structure.

For producer-consumer scenarios across threads, `BlockingQueue` implementations such as `ArrayBlockingQueue` and `LinkedBlockingQueue` add blocking `put`/`take` operations, which removes the need to write manual wait/notify logic.

## 5. Iteration and fail-fast behavior

Most Java collections use fail-fast iterators: if the collection is structurally modified while being iterated (outside of the iterator's own `remove()`), a `ConcurrentModificationException` is thrown rather than allowing undefined behavior.

```java
for (OrderItem item : items) {
    if (item.quantity() == 0) {
        items.remove(item); // throws ConcurrentModificationException
    }
}
```

The correct approaches are to use the iterator's own removal method, or `removeIf`:

```java
Iterator<OrderItem> it = items.iterator();
while (it.hasNext()) {
    if (it.next().quantity() == 0) {
        it.remove(); // safe
    }
}

items.removeIf(item -> item.quantity() == 0); // equivalent, more concise
```

## 6. Immutability and defensive copies

`List.of(...)`, `Set.of(...)`, and `Map.of(...)` return immutable collections. Passing them where mutation is attempted throws `UnsupportedOperationException` immediately, which surfaces bugs at the point of misuse instead of somewhere downstream.

```java
List<String> statuses = List.of("PENDING", "SHIPPED", "DELIVERED");
statuses.add("CANCELLED"); // throws UnsupportedOperationException
```

When exposing an internal mutable collection through a public method, return an unmodifiable view or a defensive copy so callers cannot mutate internal state:

```java
public List<OrderItem> items() {
    return Collections.unmodifiableList(items);
}
```

## 7. Comparators and sorting

Sorting a custom type requires either implementing `Comparable`, or supplying a `Comparator`. `Comparator` composition keeps multi-field sorting readable:

```java
List<Order> orders = new ArrayList<>(allOrders);
orders.sort(
    Comparator.comparing(Order::customerId)
        .thenComparing(Order::placedAt, Comparator.reverseOrder())
);
```

This sorts by customer first, then by placement date descending within each customer, without writing a manual comparison method.

## 8. Concurrent collections

`HashMap`, `ArrayList`, and friends are not thread-safe. Wrapping them with `Collections.synchronizedMap(...)` adds a single lock around every operation, which is simple but limits throughput under contention.

`ConcurrentHashMap` is almost always the better choice for shared maps: it uses fine-grained locking internally, so unrelated keys can be read and written concurrently without blocking each other.

```java
Map<String, AtomicInteger> stockCounts = new ConcurrentHashMap<>();
stockCounts.computeIfAbsent("SKU-1", k -> new AtomicInteger()).incrementAndGet();
```

`computeIfAbsent` combined with an atomic value is a common pattern for thread-safe counters without a separate external lock.

## Key takeaway

Collection choice is a small decision that compounds. Picking the structure that matches the actual access pattern - ordered vs. unordered, unique vs. duplicate-tolerant, single-threaded vs. concurrent - avoids both subtle bugs and performance cliffs that only appear once the data grows past a handful of test entries.

