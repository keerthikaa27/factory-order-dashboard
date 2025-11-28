import React, { useEffect, useState } from "react";
import apiClient from "../api/client";

interface Order {
  id: number;
  so_number: string | null;
  customer_name: string | null;
  part_number: string | null;
  order_qty: number | null;
  os_order_qty: number | null;
  delivery_date: string | null;
}

const OpenOrders: React.FC = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [customer, setCustomer] = useState("");
  const [part, setPart] = useState("");
  const [todayOnly, setTodayOnly] = useState(false);
  const [loading, setLoading] = useState(false);

  const fetchOpenOrders = async () => {
    setLoading(true);
    try {
      const params: any = {};

      if (customer.trim()) params.customer_name = customer.trim();
      if (part.trim()) params.part_number = part.trim();
      if (todayOnly) params.today_only = true;

      const response = await apiClient.get("/orders/open", { params });
      console.log("Open orders response:", response.data);
      setOrders(response.data);
    } catch (err) {
      console.error("Error loading open orders:", err);
      setOrders([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOpenOrders();
  }, []);

  const totalPendingOrders = orders.length;
  const totalOpenQty = orders.reduce(
    (sum, o) => sum + (o.os_order_qty ?? 0),
    0
  );
  const uniqueCustomers = new Set(
    orders.map((o) => o.customer_name || "")
  ).size;

  return (
    <div className="space-y-6">
      {/* Summary cards */}
      <div className="grid gap-4 md:grid-cols-3">
        <div className="card">
          <p className="subheading">Pending Orders</p>
          <p className="heading text-2xl mt-1">
            {totalPendingOrders}
          </p>
        </div>
        <div className="card">
          <p className="subheading">Total Open Quantity</p>
          <p className="heading text-2xl mt-1">
            {totalOpenQty}
          </p>
        </div>
        <div className="card">
          <p className="subheading">Customers with Open Orders</p>
          <p className="heading text-2xl mt-1">
            {uniqueCustomers}
          </p>
        </div>
      </div>

      {/* Filter panel */}
      <div className="card">
        <h3 className="heading mb-2">Open Orders Management</h3>
        <p className="text-sm text-slate-600 mb-4">
          View and filter all pending orders from the Outstanding report.
        </p>

        <div className="grid md:grid-cols-3 gap-4">
          <input
            className="input"
            placeholder="Filter by Customer"
            value={customer}
            onChange={(e) => setCustomer(e.target.value)}
          />

          <input
            className="input"
            placeholder="Filter by Part Number"
            value={part}
            onChange={(e) => setPart(e.target.value)}
          />

          <label className="flex items-center gap-2 text-sm cursor-pointer">
            <input
              type="checkbox"
              checked={todayOnly}
              onChange={(e) => setTodayOnly(e.target.checked)}
            />
            Show Today&apos;s Open Orders Only
          </label>
        </div>

        <div className="flex gap-2 mt-4">
          <button onClick={fetchOpenOrders} className="btn-primary">
            Apply Filters
          </button>
          <button
            onClick={() => {
              setCustomer("");
              setPart("");
              setTodayOnly(false);
              fetchOpenOrders();
            }}
            className="btn-secondary"
          >
            Reset
          </button>
        </div>
      </div>

      {/* Results */}
      <div className="card">
        <p className="subheading mb-2">Pending Orders</p>

        {loading ? (
          <p className="text-sm text-slate-600">Loading open orders…</p>
        ) : orders.length === 0 ? (
          <p className="text-sm text-slate-500">
            No open orders match your filters.
          </p>
        ) : (
          <div className="table-shell mt-2">
            <table className="table-base">
              <thead className="table-header">
                <tr>
                  <th className="table-header-cell">SO No</th>
                  <th className="table-header-cell">Customer</th>
                  <th className="table-header-cell">Part</th>
                  <th className="table-header-cell">Order Qty</th>
                  <th className="table-header-cell">Open Qty</th>
                  <th className="table-header-cell">Delivery Date</th>
                </tr>
              </thead>
              <tbody>
                {orders.map((order) => (
                  <tr key={order.id} className="hover:bg-[#f9f0e3]">
                    <td className="table-cell">{order.so_number}</td>
                    <td className="table-cell">{order.customer_name}</td>
                    <td className="table-cell">{order.part_number}</td>
                    <td className="table-cell">
                      {order.order_qty ?? "-"}
                    </td>
                    <td className="table-cell heading">
                      {order.os_order_qty ?? "-"}
                    </td>
                    <td className="table-cell">
                      {order.delivery_date ?? "-"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default OpenOrders;
