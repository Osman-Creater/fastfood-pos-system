import { useMemo, useState } from "react";

const defaultItems = [
  { id: 1, name: "Classic Burger", price: 12.5 },
  { id: 2, name: "Chicken Wrap", price: 10.5 },
  { id: 3, name: "Fries", price: 4.5 },
  { id: 4, name: "Soft Drink", price: 2.75 },
  { id: 5, name: "Cheese Burger", price: 13.5 },
  { id: 6, name: "Family Meal", price: 19.99 },
];

export default function HomePage() {
  const [cart, setCart] = useState<{ id: number; name: string; price: number; qty: number }[]>([]);

  const addToCart = (item: { id: number; name: string; price: number }) => {
    setCart((prev) => {
      const existing = prev.find((p) => p.id === item.id);
      if (existing) {
        return prev.map((p) =>
          p.id === item.id ? { ...p, qty: p.qty + 1 } : p
        );
      }
      return [...prev, { ...item, qty: 1 }];
    });
  };

  const totals = useMemo(() => {
    const subtotal = cart.reduce((sum, item) => sum + item.price * item.qty, 0);
    const tax = subtotal * 0.1;
    const total = subtotal + tax;
    return { subtotal, tax, total };
  }, [cart]);

  return (
    <main style={{ display: "grid", gridTemplateColumns: "1.2fr 0.8fr", gap: 20, padding: 20 }}>
      <section>
        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 20, alignItems: "center" }}>
          <h1 style={{ margin: 0 }}>FastFood POS</h1>
          <div style={{ fontSize: 13, color: "#374151" }}>Store: loc-001 • Shift: 104</div>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, minmax(180px, 1fr))", gap: 16 }}>
          {defaultItems.map((item) => (
            <div key={item.id} style={{ border: "1px solid #d1d5db", borderRadius: 12, padding: 16, background: "#fff" }}>
              <h3 style={{ marginTop: 0 }}>{item.name}</h3>
              <p>${item.price.toFixed(2)}</p>
              <button onClick={() => addToCart(item)} style={{ width: "100%", padding: 10, borderRadius: 8, border: "none", background: "#111827", color: "#fff" }}>
                Add to cart
              </button>
            </div>
          ))}
        </div>

        <div style={{ marginTop: 24, display: "grid", gridTemplateColumns: "repeat(4, minmax(120px, 1fr))", gap: 12 }}>
          {[
            { label: "Gross Sales", value: "$2,450" },
            { label: "Orders", value: "87" },
            { label: "Refunds", value: "$120" },
            { label: "Low Stock", value: "4 items" },
          ].map((kpi) => (
            <div key={kpi.label} style={{ border: "1px solid #d1d5db", borderRadius: 10, padding: 12, background: "#fff" }}>
              <div style={{ color: "#6b7280", fontSize: 12 }}>{kpi.label}</div>
              <strong style={{ fontSize: 20 }}>{kpi.value}</strong>
            </div>
          ))}
        </div>
      </section>

      <aside style={{ border: "1px solid #d1d5db", borderRadius: 12, padding: 16, background: "#fafafa" }}>
        <h2 style={{ marginTop: 0 }}>Current Order</h2>

        <div style={{ paddingTop: 12 }}>
          {cart.length === 0 ? (
            <p>No items selected</p>
          ) : (
            cart.map((item) => (
              <div key={item.id} style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
                <span>{item.name} x {item.qty}</span>
                <span>${(item.price * item.qty).toFixed(2)}</span>
              </div>
            ))
          )}
        </div>

        <hr />

        <div style={{ display: "grid", gap: 8 }}>
          <div style={{ display: "flex", justifyContent: "space-between" }}><span>Subtotal</span><span>${totals.subtotal.toFixed(2)}</span></div>
          <div style={{ display: "flex", justifyContent: "space-between" }}><span>Tax</span><span>${totals.tax.toFixed(2)}</span></div>
          <div style={{ display: "flex", justifyContent: "space-between", fontWeight: 700 }}><span>Total</span><span>${totals.total.toFixed(2)}</span></div>
        </div>

        <button style={{ width: "100%", marginTop: 20, padding: 12, background: "#111827", color: "white", borderRadius: 8, border: "none" }}>
          Pay Now
        </button>
      </aside>
    </main>
  );
}
