import React, { useState, useEffect } from "react";
import RevenueLineChart from "./components/RevenueLineChart";
import PopularLevelsChart from "./components/PopularLevelsChart";

function App() {
  const today = new Date().toISOString().slice(0, 10);
  const lastWeek = new Date(Date.now() - 7 * 86400000).toISOString().slice(0, 10);
  const [activeUsers, setActiveUsers] = useState(null);
  const [totalPurchases, setTotalPurchases] = useState(null);
  const [avgSessionLength, setAvgSessionLength] = useState(null);

  const [filters, setFilters] = useState({
    device: "All",
    level: "",
    startDate: lastWeek,
    endDate: today,
  });

  const handleReset = () => {
    setFilters({
      device: "All",
      level: "",
      startDate: lastWeek,
      endDate: today,
    });
  };

  useEffect(() => {
    // Always fetch active users — not filter dependent
    fetch("http://localhost:5000/api/active-users")
      .then((res) => res.json())
      .then((data) => setActiveUsers(data.active_users));
  
    // Fetch filter-dependent total purchases
    const params = new URLSearchParams();
    if (filters.device !== "All") params.append("device", filters.device);
    if (filters.level) params.append("level", filters.level);
    if (filters.startDate) params.append("start", filters.startDate);
    if (filters.endDate) params.append("end", filters.endDate);
  
    fetch(`http://localhost:5000/api/total-purchases?${params.toString()}`)
      .then((res) => res.json())
      .then((data) => setTotalPurchases(data.total_purchases));
  
    fetch(`http://localhost:5000/api/session-lengths?${params.toString()}`)
      .then((res) => res.json())
      .then((data) => setAvgSessionLength(data.average_session_minutes));
  }, [filters]);
  

  return (
    <div style={{ fontFamily: "sans-serif", padding: "2rem" }}>
      <h1>🎮 Game Analytics Dashboard</h1>

      {/* Filters UI */}
      <div style={{ marginBottom: "1rem" }}>
        <label>
          Device:
          <select
            value={filters.device}
            onChange={(e) => setFilters({ ...filters, device: e.target.value })}
            style={{ margin: "0 1rem" }}
          >
            <option>All</option>
            <option>PC</option>
            <option>Mobile</option>
            <option>Tablet</option>
          </select>
        </label>

        <label>
          Level:
          <input
            type="number"
            value={filters.level}
            onChange={(e) => setFilters({ ...filters, level: e.target.value })}
            placeholder="Any"
            style={{ margin: "0 1rem", width: "60px" }}
          />
        </label>

        <label>
          Start:
          <input
            type="date"
            value={filters.startDate}
            onChange={(e) => setFilters({ ...filters, startDate: e.target.value })}
            style={{ margin: "0 1rem" }}
          />
        </label>

        <label>
          End:
          <input
            type="date"
            value={filters.endDate}
            onChange={(e) => setFilters({ ...filters, endDate: e.target.value })}
          />
        </label>

        <button onClick={handleReset} style={{ marginLeft: "1rem" }}>
          Reset Filters
        </button>
      </div>

      <div style={{ display: "flex", gap: "2rem", marginBottom: "2rem" }}>
      <div>
        <h3>👤 Active Users (Last 24h)</h3>
        <p>{activeUsers !== null ? activeUsers : "Loading..."}</p>
      </div>
      <div>
        <h3>💰 Total Purchases</h3>
        <p>{totalPurchases !== null ? `$${totalPurchases.toFixed(2)}` : "Loading..."}</p>
      </div>
      <div>
        <h3>🕒 Avg. Session Length</h3>
        <p>{avgSessionLength !== null ? `${avgSessionLength} min` : "Loading..."}</p>
      </div>
    </div>

      {/* Charts */}
      <div style={{ marginTop: "2rem" }}>
        <RevenueLineChart filters={filters} />
      </div>

      <div style={{ marginTop: "2rem" }}>
        <PopularLevelsChart filters={filters} />
      </div>
    </div>
  );
}

export default App;
