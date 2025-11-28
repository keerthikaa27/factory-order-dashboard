import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import SearchOrders from "../sections/SearchOrders";
import OpenOrders from "../sections/OpenOrders";
import SalesAnalytics from "../sections/SalesAnalytics";

type Tab = "search" | "open" | "analytics";

const DashboardPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<Tab>("search");
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const tab = params.get("tab") as Tab | null;

    if (tab && ["search", "open", "analytics"].includes(tab)) {
      setActiveTab(tab);
    } else {
      setActiveTab("search");
    }
  }, [location.search]);

  const changeTab = (tab: Tab) => {
    setActiveTab(tab);
    navigate(`/dashboard?tab=${tab}`, { replace: true });
  };

  return (
    <div className="space-y-4">
     
      <div className="flex gap-2 border-b border-[#e0d3c2]">
        <button
          onClick={() => changeTab("search")}
          className={`px-4 py-2 text-sm rounded-t-lg ${
            activeTab === "search"
              ? "bg-[#fffaf5] border border-b-0 border-[#e0d3c2] heading"
              : "text-slate-600 hover:text-[#6f4e37]"
          }`}
        >
          Search Orders
        </button>
        <button
          onClick={() => changeTab("open")}
          className={`px-4 py-2 text-sm rounded-t-lg ${
            activeTab === "open"
              ? "bg-[#fffaf5] border border-b-0 border-[#e0d3c2] heading"
              : "text-slate-600 hover:text-[#6f4e37]"
          }`}
        >
          Open Orders
        </button>
        <button
          onClick={() => changeTab("analytics")}
          className={`px-4 py-2 text-sm rounded-t-lg ${
            activeTab === "analytics"
              ? "bg-[#fffaf5] border border-b-0 border-[#e0d3c2] heading"
              : "text-slate-600 hover:text-[#6f4e37]"
          }`}
        >
          Sales Analytics
        </button>
      </div>

      <div className="card">
        {activeTab === "search" && <SearchOrders />}
        {activeTab === "open" && <OpenOrders />}
        {activeTab === "analytics" && <SalesAnalytics />}
      </div>
    </div>
  );
};

export default DashboardPage;
