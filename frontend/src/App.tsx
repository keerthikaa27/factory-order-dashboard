import React from "react";
import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { isLoggedIn, logout } from "./auth";

const App: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = React.useState(false);

  React.useEffect(() => {
    if (!isLoggedIn()) {
      navigate("/login");
    }
  }, [navigate]);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const goToTab = (tab: string) => {
    setSidebarOpen(false);
    navigate(`/dashboard?tab=${tab}`);
  };

  const goHome = () => {
    setSidebarOpen(false);
    navigate("/");
  };

  const onDashboard = location.pathname.startsWith("/dashboard");

  return (
    <div className="min-h-screen bg-[#f6efe6] text-[#3e2f24]">
      
      {/* ✅ BROWN HEADER BAR */}
      <header className="bg-[#6f4e37] text-[#f3e6d8] shadow-md px-6 py-4 flex items-center justify-between">
        
        <div className="flex items-center gap-3">
          {/* Menu button for sidebar */}
          <button
            onClick={() => setSidebarOpen(true)}
            className="md:hidden inline-flex items-center justify-center w-9 h-9 rounded-full border border-[#c8ad90] bg-[#7a5a44] hover:bg-[#5c3f2f] transition"
            aria-label="Open navigation"
          >
            <span className="text-lg text-white">☰</span>
          </button>

          <div className="cursor-pointer" onClick={goHome}>
            <span className="text-xs tracking-[0.18em] uppercase text-[#e7d6c5] block">
              Factory Order Management
            </span>

            <h1 className="text-lg font-semibold text-white">
              {onDashboard ? "Operations Dashboard" : "Overview"}
            </h1>
          </div>
        </div>

        <button
          onClick={handleLogout}
          className="px-4 py-2 rounded-full border border-[#e7d6c5] text-[#e7d6c5] hover:bg-[#5c3f2f] hover:text-white transition text-sm"
        >
          Logout
        </button>
      </header>

      {/* Slide-in sidebar (drawer) */}
      {sidebarOpen && (
        <div className="fixed inset-0 z-40 flex">
          <div className="w-64 bg-[#fffaf5] shadow-xl p-6 flex flex-col">
            <h2 className="text-2xl heading mb-6">Factory Panel</h2>

            <nav className="space-y-2 text-sm">
              <button
                onClick={goHome}
                className="w-full text-left px-3 py-2 rounded-lg hover:bg-[#f3e6da]"
              >
                Landing Overview
              </button>
              <button
                onClick={() => goToTab("search")}
                className="w-full text-left px-3 py-2 rounded-lg hover:bg-[#f3e6da]"
              >
                Search Orders
              </button>
              <button
                onClick={() => goToTab("open")}
                className="w-full text-left px-3 py-2 rounded-lg hover:bg-[#f3e6da]"
              >
                Open Orders
              </button>
              <button
                onClick={() => goToTab("analytics")}
                className="w-full text-left px-3 py-2 rounded-lg hover:bg-[#f3e6da]"
              >
                Sales Analytics
              </button>
            </nav>

            <div className="mt-auto pt-4 border-t border-[#e0d3c2] text-xs text-slate-500">
              <p>Factory Order Management</p>
              <p className="mt-1">Internal Use Only</p>
            </div>
          </div>

          {/* Backdrop */}
          <div
            className="flex-1 bg-black/20"
            onClick={() => setSidebarOpen(false)}
          />
        </div>
      )}

      {/* Content */}
      <main className="p-4 md:p-6 space-y-6">
        <Outlet />
      </main>
    </div>
  );
};

export default App;
