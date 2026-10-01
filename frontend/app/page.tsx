const menuItems = [
  { id: 1, name: "Classic Burger", price: 12.5 },
  { id: 2, name: "Chicken Wrap", price: 10.5 },
  { id: 3, name: "Fries", price: 4.5 },
  { id: 4, name: "Soft Drink", price: 2.75 },
  { id: 5, name: "Cheese Burger", price: 13.5 },
  { id: 6, name: "Family Meal", price: 19.99 },
];

export default function HomePage() {
  const subtotal = menuItems.reduce((sum, item) => sum + item.price, 0);
  const tax = subtotal * 0.1;
  const total = subtotal + tax;

  return (
    <main style={{ display: "grid", gridTemplateColumns: "1.3fr 0.7fr", gap: 24, padding: 24 }}>
      <section>
        <h1 style={{ marginBottom: 20 }}>FastFood POS</h1>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, minmax(180px, 1fr))", gap: 16 }}>
          {menuItems.map((item) => (
            <div key={item.id} style={{ border: "1px solid #ddd", borderRadius: 12, padding: 16 }}>
              <h3>{item.name}</h3>
              <p>${item.price.toFixed(2)}</p>
              <button style={{ width: "100%", padding: 10 }}>Add to cart</button>
            </div>
          ))}
        </div>
      </section>

      <aside style={{ border: "1px solid #ddd", borderRadius: 12, padding: 16, background: "#fafafa" }}>
        <h2>Current Order</h2>
        <div style={{ paddingTop: 12 }}>
          {menuItems.slice(0, 3).map((item) => (
            <div key={item.id} style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
              <span>{item.name}</span>
              <span>${item.price.toFixed(2)}</span>
            </div>
          ))}
        </div>
        <hr />
        <div style={{ display: "grid", gap: 8 }}>
          <div style={{ display: "flex", justifyContent: "space-between" }}><span>Subtotal</span><span>${subtotal.toFixed(2)}</span></div>
          <div style={{ display: "flex", justifyContent: "space-between" }}><span>Tax</span><span>${tax.toFixed(2)}</span></div>
          <div style={{ display: "flex", justifyContent: "space-between", fontWeight: 700 }}><span>Total</span><span>${total.toFixed(2)}</span></div>
        </div>
        <button style={{ width: "100%", marginTop: 20, padding: 12, background: "#111827", color: "white", borderRadius: 8 }}>
          Pay Now
        </button>
      </aside>
    </main>
  );
}
