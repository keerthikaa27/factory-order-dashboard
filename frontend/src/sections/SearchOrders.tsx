import React, { useState, useEffect } from "react";
import apiClient from "../api/client";


const SearchOrders: React.FC = () => {
  console.log("🔍 SearchOrders rendered");

  const [filters, setFilters] = useState({
    global: "",
    po_number: "",
    serial_number: "",
    part_number: "",
    customer_name: "",
    status: "",
  });

  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  useEffect(() => {
    if (!filters.global.trim()) return;
    const handle = setTimeout(() => {
      handleSearch();
    }, 500); 

    return () => clearTimeout(handle);
  }, [filters.global]);


  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    setFilters({ ...filters, [e.target.name]: e.target.value });
  };

  const handleSearch = async () => {
    setLoading(true);
    try {
      const res = await apiClient.get("/orders/search", {
        params: {
          po_number: filters.po_number || filters.global,
          serial_number: filters.serial_number || filters.global,
          part_number: filters.part_number || filters.global,
          customer_name: filters.customer_name || filters.global,
          status: filters.status || undefined,
        },
      });
      setResults(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const resetFilters = () => {
    setFilters({
      global: "",
      po_number: "",
      serial_number: "",
      part_number: "",
      customer_name: "",
      status: "",
    });
    setResults([]);
  };

  return (
    <div className="space-y-5">
      <div>
        <h3 className="heading text-lg mb-1">Order Search & Filters</h3>
        <p className="text-xs text-slate-500">
          Search by PO, serial, part, customer and dispatch status.
        </p>
      </div>

      {/* Filters */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <input
          name="global"
          value={filters.global}
          onChange={handleChange}
          onKeyDown={(e) => e.key === "Enter" && handleSearch()}
          placeholder="Global search (PO / Serial / Part / Customer)"
          className="input w-full"
        />
        <input
          name="po_number"
          value={filters.po_number}
          onChange={handleChange}
          onKeyDown={(e) => e.key === "Enter" && handleSearch()}
          placeholder="PO Number"
          className="input w-full"
        />
        <input
          name="serial_number"
          value={filters.serial_number}
          onChange={handleChange}
          onKeyDown={(e) => e.key === "Enter" && handleSearch()}
          placeholder="Serial Number"
          className="input w-full"
        />
        <input
          name="part_number"
          value={filters.part_number}
          onChange={handleChange}
          onKeyDown={(e) => e.key === "Enter" && handleSearch()}
          placeholder="Part Number"
          className="input w-full"
        />
        <input
          name="customer_name"
          value={filters.customer_name}
          onChange={handleChange}
          onKeyDown={(e) => e.key === "Enter" && handleSearch()}
          placeholder="Customer Name"
          className="input w-full"
        />
        <select
          name="status"
          value={filters.status}
          onChange={handleChange}
          className="select w-full"
        >
          <option value="">All Status</option>
          <option value="DISPATCHED">Dispatched</option>
          <option value="PENDING">Pending</option>
        </select>
      </div>

      {/* Actions */}
      <div className="flex gap-2">
        <button onClick={handleSearch} className="btn-primary">
          Apply Filters
        </button>
        <button onClick={resetFilters} className="btn-secondary">
          Reset
        </button>
      </div>

      {loading && (
        <p className="text-xs text-slate-500">Searching orders...</p>
      )}

      {/* Results */}
      {!loading && results.length > 0 && (
        <div className="table-shell mt-2">
            <div className="text-[10px] text-slate-400 mb-1 md:hidden">
            Swipe horizontally to see all columns →
            </div>
            <table className="table-base">
            <thead className="table-header">
              <tr>
                <th className="table-header-cell">SO No</th>
                <th className="table-header-cell">Customer</th>
                <th className="table-header-cell">Part</th>
                <th className="table-header-cell">Status</th>
                <th className="table-header-cell">Delivery Date</th>
              </tr>
            </thead>
            <tbody>
              {results.map((row) => (
                <tr key={row.id}>
                  <td className="table-cell">{row.so_number}</td>
                  <td className="table-cell">{row.customer_name}</td>
                  <td className="table-cell">{row.part_number}</td>
                  <td className="table-cell">
                    {row.status === "DISPATCHED" ? (
                      <span className="badge-green">Dispatched</span>
                    ) : (
                      <span className="badge-amber">Pending</span>
                    )}
                  </td>
                  <td className="table-cell">{row.delivery_date}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {!loading && results.length === 0 && (
        <p className="text-xs text-slate-500">
          No orders matched your filters yet.
        </p>
      )}
    </div>
  );
};

export default SearchOrders;
