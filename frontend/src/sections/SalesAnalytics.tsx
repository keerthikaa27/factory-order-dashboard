import React, { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";
import apiClient from "../api/client";

const SalesAnalytics: React.FC = () => {
  const [year, setYear] = useState("2024-2025");
  const [summary, setSummary] = useState<any>(null);
  const [productData, setProductData] = useState<any[]>([]);
  const [customerData, setCustomerData] = useState<any[]>([]);

  useEffect(() => {
    const loadAnalytics = async () => {
      try {
        const summaryRes = await apiClient.get("/analytics/financial-year", {
          params: { financial_year: year },
        });

        const productRes = await apiClient.get("/analytics/product-wise", {
          params: { financial_year: year },
        });

        const customerRes = await apiClient.get("/analytics/customer-wise", {
          params: { financial_year: year },
        });

        setSummary(summaryRes.data);
        setProductData(productRes.data);
        setCustomerData(customerRes.data);
      } catch (err) {
        console.error(err);
      }
    };

    loadAnalytics();
  }, [year]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-3">
        <div>
          <h3 className="heading text-lg mb-1">
            Sales & Delivery Analytics
          </h3>
          <p className="text-xs text-slate-500">
            Financial year totals, product and customer level analysis.
          </p>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <label className="text-xs">Financial Year</label>
          <input
            value={year}
            onChange={(e) => setYear(e.target.value)}
            className="input"
          />
        </div>
      </div>

      {summary && (
        <div className="grid gap-4 md:grid-cols-2">
          <div className="card">
            <p className="subheading">Total Sales Amount</p>
            <h2 className="heading text-2xl mt-1">
              ₹ {summary.total_sales_amount}
            </h2>
          </div>
          <div className="card">
            <p className="subheading">Total Quantity Sold</p>
            <h2 className="heading text-2xl mt-1">
              {summary.total_quantity}
            </h2>
          </div>
        </div>
      )}

      <div className="card">
        <h4 className="heading text-sm mb-2">Product-wise Sales</h4>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={productData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="part_number" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="total_amount" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="card">
        <h4 className="heading text-sm mb-2">Customer-wise Sales</h4>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={customerData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="customer_name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="total_amount" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default SalesAnalytics;
