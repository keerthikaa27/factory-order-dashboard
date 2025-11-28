import React from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

const sectionVariant = {
  hidden: { opacity: 0, y: 40 },
  show: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

const LandingPage: React.FC = () => {
  const navigate = useNavigate();

  const goToSearch = () => navigate("/dashboard?tab=search");
  const goToOpen = () => navigate("/dashboard?tab=open");
  const goToAnalytics = () => navigate("/dashboard?tab=analytics");

  const scrollTo = (id: string) => {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <div className="space-y-16 md:space-y-24">

      {/* HERO SECTION */}
      <motion.section
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="min-h-[70vh] flex flex-col items-center justify-center text-center gap-4"
      >
        <p className="subheading">Factory Order Management</p>
        <h2 className="heading text-3xl md:text-4xl max-w-2xl">
          One calm dashboard for orders, dispatches & sales insights.
        </h2>
        <p className="text-sm md:text-base text-slate-600 max-w-xl">
          Upload your factory CSVs, track open orders, and analyse deliveries—
          all in a clean, minimal interface built for daily operations.
        </p>

        <div className="flex flex-wrap gap-3 mt-4 justify-center">
          <button onClick={goToSearch} className="btn-primary">
            Go to Dashboard
          </button>
          <button
            onClick={() => scrollTo("feature-search")}
            className="btn-secondary"
          >
            Explore Features
          </button>
        </div>

        <button
          onClick={() => scrollTo("feature-search")}
          className="mt-10 flex flex-col items-center text-xs text-slate-500 hover:text-[#6f4e37] transition"
        >
          <span>Scroll to learn what you can do</span>
          <span className="text-lg mt-1">↓</span>
        </button>
      </motion.section>

      {/* FEATURE 1: SEARCH */}
      <motion.section
        id="feature-search"
        variants={sectionVariant}
        initial="hidden"
        whileInView="show"
        viewport={{ once: true, amount: 0.3 }}
        className="grid md:grid-cols-2 gap-8 items-center"
      >
        <div className="space-y-3">
          <p className="subheading">Feature 01</p>
          <h3 className="heading text-2xl">Powerful Order Search</h3>
          <p className="text-sm text-slate-600">
            Instantly find any order by PO number, serial number, product/part
            code, or customer name. Combine filters like a pro to answer
            questions in seconds instead of digging through raw Excel files.
          </p>
          <ul className="text-sm text-slate-600 space-y-1 mt-2">
            <li>• Global search across PO / Serial / Part / Customer</li>
            <li>• Filter by dispatch status: Pending vs Dispatched</li>
            <li>• Clean results table with key information only</li>
          </ul>
          <button onClick={goToSearch} className="btn-primary mt-3">
            Try Search Dashboard
          </button>
        </div>

        <div className="card group hover:shadow-md transition transform hover:-translate-y-1">
          <p className="subheading mb-2">Preview</p>
          <p className="text-sm text-slate-600 mb-4">
            Search across thousands of orders without leaving this dashboard.
          </p>
          <div className="space-y-2 text-xs bg-[#f9f0e3] rounded-lg p-3">
            <div className="flex gap-2">
              <span className="badge-amber">PO: 12345</span>
              <span className="badge-green">Customer: Emerson</span>
            </div>
            <p>Result: 18 matching orders across products & dates.</p>
          </div>
        </div>
      </motion.section>

      {/* FEATURE 2: OPEN ORDERS */}
      <motion.section
        id="feature-open"
        variants={sectionVariant}
        initial="hidden"
        whileInView="show"
        viewport={{ once: true, amount: 0.3 }}
        className="grid md:grid-cols-2 gap-8 items-center"
      >
        <div className="order-2 md:order-1 card group hover:shadow-md transition transform hover:-translate-y-1">
          <p className="subheading mb-2">Snapshot</p>
          <p className="text-sm text-slate-600 mb-4">
            Focus only on what&apos;s still pending from the Outstanding
            report.
          </p>
          <div className="text-xs bg-[#f9f0e3] rounded-lg p-3 space-y-1">
            <p>• Today&apos;s open orders</p>
            <p>• Pending quantities by customer</p>
            <p>• Delivery dates coming up soon</p>
          </div>
        </div>

        <div className="order-1 md:order-2 space-y-3">
          <p className="subheading">Feature 02</p>
          <h3 className="heading text-2xl">Open Orders at a Glance</h3>
          <p className="text-sm text-slate-600">
            See all pending orders from your Sales Order Outstanding sheet in
            one focused view. Filter by customer or product to understand what
            still needs to be shipped.
          </p>
          <ul className="text-sm text-slate-600 space-y-1 mt-2">
            <li>• View all pending orders from Outstanding CSV</li>
            <li>• Optional focus on today&apos;s delivery date</li>
            <li>• Quantities, customers, and dates in one place</li>
          </ul>
          <button onClick={goToOpen} className="btn-primary mt-3">
            View Open Orders
          </button>
        </div>
      </motion.section>

      {/* FEATURE 3: ANALYTICS */}
      <motion.section
        id="feature-analytics"
        variants={sectionVariant}
        initial="hidden"
        whileInView="show"
        viewport={{ once: true, amount: 0.3 }}
        className="grid md:grid-cols-2 gap-8 items-center"
      >
        <div className="space-y-3">
          <p className="subheading">Feature 03</p>
          <h3 className="heading text-2xl">Sales & Delivery Analytics</h3>
          <p className="text-sm text-slate-600">
            Turn your Delivery report into quick insights. Track financial year
            totals, see which products move the most, and understand which
            customers drive your revenue.
          </p>
          <ul className="text-sm text-slate-600 space-y-1 mt-2">
            <li>• Financial year sales totals</li>
            <li>• Product-wise & customer-wise breakdown</li>
            <li>• Charts powered directly from your CSV data</li>
          </ul>
          <button onClick={goToAnalytics} className="btn-primary mt-3">
            Open Analytics View
          </button>
        </div>

        <div className="card group hover:shadow-md transition transform hover:-translate-y-1">
          <p className="subheading mb-2">Charts</p>
          <p className="text-sm text-slate-600 mb-4">
            Simple bar charts for product and customer level sales.
          </p>
          <div className="h-24 bg-[#f9f0e3] rounded-lg flex items-center justify-center text-xs text-slate-500">
            (Product-wise sales chart)
          </div>
          <div className="h-24 mt-2 bg-[#f9f0e3] rounded-lg flex items-center justify-center text-xs text-slate-500">
            (Customer-wise sales chart)
          </div>
        </div>
      </motion.section>

      {/* FINAL CTA */}
      <motion.section
        variants={sectionVariant}
        initial="hidden"
        whileInView="show"
        viewport={{ once: true, amount: 0.3 }}
        className="card flex flex-col md:flex-row md:items-center md:justify-between gap-3"
      >
        <div>
          <p className="heading text-sm">Ready to work with real data?</p>
          <p className="text-xs text-slate-600 mt-1">
            Jump into the dashboard to search orders, view open items, or check
            sales analytics using your factory CSVs.
          </p>
        </div>
        <div className="flex gap-2">
          <button onClick={goToSearch} className="btn-primary">
            Go to Search Dashboard
          </button>
          <button onClick={goToAnalytics} className="btn-secondary">
            View Analytics
          </button>
        </div>
      </motion.section>
    </div>
  );
};

export default LandingPage;
