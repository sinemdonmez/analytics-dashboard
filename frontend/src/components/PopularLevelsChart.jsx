import React, { useEffect, useState } from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

function PopularLevelsChart({ filters }) {
  const [data, setData] = useState(null);

  useEffect(() => {
    const params = new URLSearchParams();

    if (filters.device !== "All") params.append("device", filters.device);
    if (filters.level) params.append("level", filters.level);
    if (filters.startDate) params.append("start", filters.startDate);
    if (filters.endDate) params.append("end", filters.endDate);

    fetch(`http://localhost:5000/api/popular-levels?${params.toString()}`)
      .then((res) => res.json())
      .then((result) => {
        const labels = result.map((r) => `Level ${r.level}`);
        const values = result.map((r) => r.play_count);

        setData({
          labels,
          datasets: [
            {
              label: "Top 5 Levels",
              data: values,
              backgroundColor: "rgba(75, 192, 192, 0.6)",
            },
          ],
        });
      });
  }, [filters]);

  return (
    <div>
      <h3>📊 Most Played Levels</h3>
      {data ? <Bar data={data} /> : <p>Loading chart...</p>}
    </div>
  );
}


export default PopularLevelsChart;
