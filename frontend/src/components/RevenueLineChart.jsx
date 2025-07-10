import React, { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(LineElement, PointElement, CategoryScale, LinearScale, Tooltip, Legend);



function RevenueLineChart({ filters }) {
    const [data, setData] = useState(null);
  
    useEffect(() => {
      const params = new URLSearchParams();
  
      if (filters.device !== "All") params.append("device", filters.device);
      if (filters.level) params.append("level", filters.level);
      if (filters.startDate) params.append("start", filters.startDate);
      if (filters.endDate) params.append("end", filters.endDate);
  
      fetch(`http://localhost:5000/api/daily-revenue?${params.toString()}`)
        .then((res) => res.json())
        .then((result) => {
          const labels = result.map((r) => r.date);
          const values = result.map((r) => r.revenue);
  
          setData({
            labels,
            datasets: [
              {
                label: `Revenue`,
                data: values,
                borderColor: "rgba(153, 102, 255, 1)",
                backgroundColor: "rgba(153, 102, 255, 0.2)",
                tension: 0.4,
                fill: true,
              },
            ],
          });
        });
    }, [filters]);
  
    return (
      <div>
        <h3>📈 Daily Revenue</h3>
        {data ? <Line data={data} /> : <p>Loading chart...</p>}
      </div>
    );
  }
  

export default RevenueLineChart;
